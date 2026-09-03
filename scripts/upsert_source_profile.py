#!/usr/bin/env python3
"""Create or update an organization-scoped external SourceProfile."""
from _common import *
from jsonschema import Draft202012Validator
from urllib.parse import urlsplit,urlunsplit
import argparse,hashlib,json,os

KINDS={"official","regulator","primary_researcher","academic","publication","practitioner","vendor","data_provider","community","social_account","other"}
WATCH={"seed","candidate","active","paused","deprioritized","blocked","unavailable"}
PRIORITIES={"low","medium","high"};OUTCOMES={"original","supported","contradicted"};METHOD_QUALITY={"unknown","weak","mixed","strong"};QUALITY_RANK={"unknown":0,"weak":1,"mixed":2,"strong":3}
SUBJECT_KINDS={"organization","person","brand","product","creator","publication","channel","platform","regulator","community","other"}
SUBJECT_RELATIONSHIPS={"own_organization","competitor","substitute","partner","creator","thought_leader","publication","regulator","platform","vendor","benchmark","ecosystem_actor","monitored_subject","other"}
SOURCE_MODALITIES={"text","image","audio","video","document","structured","mixed"};CADENCE_MODES={"recurring","event_driven","manual"};CADENCE_SOURCES={"user","inferred","policy"};NOTIFICATION_MODES={"material_changes_only","due_and_material_changes","all_checks","silent"}


def _normalized_reference(value):
    value=" ".join(str(value or "").strip().split())
    if not value:raise ValueError("source_reference is required")
    parts=urlsplit(value)
    if parts.scheme.lower() in {"http","https"} and parts.netloc:
        if parts.username or parts.password:raise ValueError("source_reference URL must not contain embedded credentials")
        scheme=parts.scheme.lower();hostname=(parts.hostname or "").lower()
        try:port=parts.port
        except ValueError as e:raise ValueError(f"invalid source_reference URL: {e}") from e
        host=f"[{hostname}]" if ":" in hostname and not hostname.startswith("[") else hostname
        if port and not ((scheme=="http" and port==80) or (scheme=="https" and port==443)):host=f"{host}:{port}"
        return urlunsplit((scheme,host,parts.path.rstrip("/"),parts.query,parts.fragment))
    return value

def _profile_id(business_id,source_reference):return "sprof_"+hashlib.sha256(f"{business_id}:{_normalized_reference(source_reference)}".encode()).hexdigest()[:16]
def _schema():return json.loads((ROOT/"core/schemas/intelligence/source-profile.schema.json").read_text())
def _validate(obj):
    errors=sorted(Draft202012Validator(_schema()).iter_errors(obj),key=lambda e:list(e.path))
    if errors:raise ValueError("SourceProfile invalid: "+"; ".join(f"{list(e.path)} {e.message}" for e in errors))
def _path(business_id,profile_id):return ROOT/"instances"/business_id/"intelligence"/"source-profiles"/f"{profile_id}.json"
def _merge_unique(old,new):return list(dict.fromkeys([*(old or []),*(new or [])]))

def _rebuild_assessments(events,previous):
    prior={x.get("fact_type"):dict(x) for x in previous or [] if isinstance(x,dict) and x.get("fact_type")};grouped={}
    for event in events:grouped.setdefault(event["fact_type"],[]).append(event)
    out=[]
    for fact in sorted(set(prior)|set(grouped)):
        base=prior.get(fact,{});evs=grouped.get(fact,[]);quality=base.get("method_quality","unknown")
        for event in evs:
            q=event.get("method_quality","unknown")
            if QUALITY_RANK[q]>QUALITY_RANK.get(quality,0):quality=q
        original=sum(1 for e in evs if e["outcome"]=="original");supported=sum(1 for e in evs if e["outcome"]=="supported");contradicted=sum(1 for e in evs if e["outcome"]=="contradicted")
        if not evs:original=int(base.get("original_source_count",0));supported=int(base.get("later_supported_count",0));contradicted=int(base.get("later_contradicted_count",0))
        out.append({"fact_type":fact,"sample_count":original+supported+contradicted,"original_source_count":original,"later_supported_count":supported,"later_contradicted_count":contradicted,"method_quality":quality,"last_evaluated_at":max([e.get("recorded_at") for e in evs if e.get("recorded_at")],default=base.get("last_evaluated_at")),"notes":base.get("notes")})
    return out

def _cadence_from_args(args,existing):
    requested=any(x is not None for x in [args.cadence_mode,args.cadence_expression,args.cadence_timezone,args.cadence_source,args.cadence_notes])
    if not requested:return existing
    mode=args.cadence_mode or (existing or {}).get("mode")
    if not mode:raise ValueError("cadence updates require --cadence-mode on a profile without an existing cadence")
    source=args.cadence_source or (existing or {}).get("source") or "inferred";previous_source=(existing or {}).get("source")
    if previous_source=="user" and source!="user" and not args.replace_user_cadence:raise ValueError("existing monitoring cadence is user-specified; preserve it unless the current explicit user instruction authorizes replacement")
    expression=args.cadence_expression if args.cadence_expression is not None else (existing or {}).get("expression");timezone=args.cadence_timezone if args.cadence_timezone is not None else (existing or {}).get("timezone");notes=args.cadence_notes if args.cadence_notes is not None else (existing or {}).get("notes")
    if mode=="recurring" and not expression:raise ValueError("recurring cadence requires --cadence-expression")
    return {"mode":mode,"expression":expression,"timezone":timezone,"source":source,"notes":notes}

def _notification_from_args(args,existing):
    requested=any(x is not None for x in [args.notification_mode,args.notification_source,args.notification_notes])
    if not requested:return existing
    source=args.notification_source or (existing or {}).get('source') or 'inferred';previous_source=(existing or {}).get('source')
    if previous_source=='user' and source!='user' and not args.replace_user_notification:raise ValueError("existing monitoring notification preference is user-specified; preserve it unless the current explicit user instruction authorizes replacement")
    return {'mode':args.notification_mode or (existing or {}).get('mode') or 'material_changes_only','source':source,'notes':args.notification_notes if args.notification_notes is not None else (existing or {}).get('notes')}

def _signal_key(value):return " ".join(str(value or '').strip().split()).casefold()
def _parse_signal_cadences(values,existing,replace_user=False):
    rows={_signal_key(x.get('signal')):dict(x) for x in existing or [] if isinstance(x,dict) and x.get('signal')}
    for raw in values or []:
        try:new=json.loads(raw)
        except json.JSONDecodeError as e:raise ValueError(f'--signal-cadence-json must be valid JSON: {e}') from e
        if not isinstance(new,dict):raise ValueError('--signal-cadence-json must decode to an object')
        signal=" ".join(str(new.get('signal') or '').strip().split())
        if not signal:raise ValueError('--signal-cadence-json requires signal')
        key=_signal_key(signal);old=rows.get(key,{});source=new.get('source') or old.get('source') or 'inferred'
        if source not in CADENCE_SOURCES:raise ValueError(f'invalid signal cadence source: {source}')
        if old.get('source')=='user' and source!='user' and not replace_user:raise ValueError(f"signal cadence for '{old.get('signal')}' is user-specified and cannot be silently replaced")
        mode=new.get('mode') or old.get('mode')
        if mode not in CADENCE_MODES:raise ValueError(f"signal cadence for '{signal}' requires mode in {sorted(CADENCE_MODES)}")
        expression=new.get('expression') if 'expression' in new else old.get('expression')
        if mode=='recurring' and not expression:raise ValueError(f"recurring signal cadence for '{signal}' requires expression")
        notification_mode=new.get('notification_mode') or old.get('notification_mode') or 'material_changes_only'
        if notification_mode not in NOTIFICATION_MODES:raise ValueError(f'invalid signal notification_mode: {notification_mode}')
        rows[key]={'signal':signal,'mode':mode,'expression':expression,'timezone':new.get('timezone') if 'timezone' in new else old.get('timezone'),'source':source,'next_check_at':new.get('next_check_at') if 'next_check_at' in new else old.get('next_check_at'),'notification_mode':notification_mode,'notes':new.get('notes') if 'notes' in new else old.get('notes')}
    return [rows[k] for k in sorted(rows)]

def upsert(args):
    base=ROOT/"instances"/args.business_id
    if not base.exists():raise ValueError(f"Unknown business: {args.business_id}")
    ref=_normalized_reference(args.source_reference);profile_id=_profile_id(args.business_id,ref);path=_path(args.business_id,profile_id);ts=now()
    if path.exists():
        obj=json.loads(path.read_text())
        if _normalized_reference(obj.get("source_reference"))!=ref:raise ValueError("existing SourceProfile reference mismatch")
        obj["source_reference"]=ref;obj.pop('owner_systems',None)
    else:
        obj={"id":profile_id,"object_type":"SourceProfile","schema_version":"1.3.0","business_id":args.business_id,"created_at":ts,"updated_at":ts,"lineage":[],"source_reference":ref,"display_name":None,"source_kind":"other","domains":[],"topic_tags":[],"watch_status":"candidate","attention_priority":"medium","discovery_reason":None,"commercial_context":None,"subject_key":None,"subject_name":None,"subject_kind":None,"subject_aliases":[],"subject_relationships":[],"source_modalities":[],"monitoring_questions":[],"material_change_signals":[],"monitoring_cadence":None,"monitoring_signal_cadences":[],"monitoring_notification":None,"last_material_change_at":None,"fact_type_assessments":[],"last_checked_at":None,"next_check_at":None,"extensions":{"external_learning":{"outcome_events":[]}}}
    for key,default in {"domains":[],"subject_key":None,"subject_name":None,"subject_kind":None,"subject_aliases":[],"subject_relationships":[],"source_modalities":[],"monitoring_questions":[],"material_change_signals":[],"monitoring_cadence":None,"monitoring_signal_cadences":[],"monitoring_notification":None,"last_material_change_at":None}.items():obj.setdefault(key,default)
    for arg,key in [('display_name','display_name'),('source_kind','source_kind'),('watch_status','watch_status'),('attention_priority','attention_priority'),('discovery_reason','discovery_reason'),('commercial_context','commercial_context'),('subject_key','subject_key'),('subject_name','subject_name'),('subject_kind','subject_kind')]:
        value=getattr(args,arg)
        if value is not None:obj[key]=value
    if args.domain:obj['domains']=_merge_unique(obj.get('domains'),args.domain)
    if args.topic_tag:obj['topic_tags']=_merge_unique(obj.get('topic_tags'),args.topic_tag)
    if args.subject_alias:obj['subject_aliases']=_merge_unique(obj.get('subject_aliases'),args.subject_alias)
    if args.subject_relationship:obj['subject_relationships']=_merge_unique(obj.get('subject_relationships'),args.subject_relationship)
    if args.source_modality:obj['source_modalities']=_merge_unique(obj.get('source_modalities'),args.source_modality)
    if args.monitoring_question:obj['monitoring_questions']=_merge_unique(obj.get('monitoring_questions'),args.monitoring_question)
    if args.material_change_signal:obj['material_change_signals']=_merge_unique(obj.get('material_change_signals'),args.material_change_signal)
    obj['monitoring_cadence']=_cadence_from_args(args,obj.get('monitoring_cadence'));obj['monitoring_notification']=_notification_from_args(args,obj.get('monitoring_notification'));obj['monitoring_signal_cadences']=_parse_signal_cadences(args.signal_cadence_json,obj.get('monitoring_signal_cadences'),args.replace_user_cadence)
    for row in obj['monitoring_signal_cadences']:obj['material_change_signals']=_merge_unique(obj.get('material_change_signals'),[row['signal']])
    if args.last_material_change_at is not None:obj['last_material_change_at']=args.last_material_change_at
    if args.last_checked_at is not None:obj['last_checked_at']=args.last_checked_at
    if args.next_check_at is not None:obj['next_check_at']=args.next_check_at
    ext=obj.setdefault('extensions',{}).setdefault('external_learning',{});events=ext.setdefault('outcome_events',[])
    if args.outcome:
        if not args.fact_type or not args.evidence_ref:raise ValueError('--outcome requires --fact-type and --evidence-ref')
        key=f'{args.fact_type}|{args.outcome}|{args.evidence_ref}'
        if not any(e.get('event_key')==key for e in events):events.append({'event_key':key,'fact_type':args.fact_type,'outcome':args.outcome,'evidence_ref':args.evidence_ref,'method_quality':args.method_quality or 'unknown','recorded_at':ts})
    obj['fact_type_assessments']=_rebuild_assessments(events,obj.get('fact_type_assessments'));obj['updated_at']=ts;_validate(obj)
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n');os.replace(tmp,path);return path,obj

def main():
    p=argparse.ArgumentParser(description='Create/update a SourceProfile. Domains are optional semantic relevance, not owners. Cadence/next-check fields are monitoring intent, never proof of an active scheduler binding.')
    p.add_argument('business_id');p.add_argument('--source-reference',required=True);p.add_argument('--display-name');p.add_argument('--source-kind',choices=sorted(KINDS));p.add_argument('--domain',action='append',choices=sorted(SYSTEMS));p.add_argument('--topic-tag',action='append');p.add_argument('--watch-status',choices=sorted(WATCH));p.add_argument('--attention-priority',choices=sorted(PRIORITIES));p.add_argument('--discovery-reason');p.add_argument('--commercial-context');p.add_argument('--subject-key');p.add_argument('--subject-name');p.add_argument('--subject-kind',choices=sorted(SUBJECT_KINDS));p.add_argument('--subject-alias',action='append');p.add_argument('--subject-relationship',action='append',choices=sorted(SUBJECT_RELATIONSHIPS));p.add_argument('--source-modality',action='append',choices=sorted(SOURCE_MODALITIES));p.add_argument('--monitoring-question',action='append');p.add_argument('--material-change-signal',action='append');p.add_argument('--cadence-mode',choices=sorted(CADENCE_MODES));p.add_argument('--cadence-expression');p.add_argument('--cadence-timezone');p.add_argument('--cadence-source',choices=sorted(CADENCE_SOURCES));p.add_argument('--cadence-notes');p.add_argument('--signal-cadence-json',action='append');p.add_argument('--replace-user-cadence',action='store_true');p.add_argument('--notification-mode',choices=sorted(NOTIFICATION_MODES));p.add_argument('--notification-source',choices=sorted(CADENCE_SOURCES));p.add_argument('--notification-notes');p.add_argument('--replace-user-notification',action='store_true');p.add_argument('--last-material-change-at');p.add_argument('--last-checked-at');p.add_argument('--next-check-at');p.add_argument('--fact-type');p.add_argument('--outcome',choices=sorted(OUTCOMES));p.add_argument('--evidence-ref');p.add_argument('--method-quality',choices=sorted(METHOD_QUALITY));args=p.parse_args()
    try:path,obj=upsert(args)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'path':storage_ref(path),'id':obj['id'],'watch_status':obj['watch_status'],'attention_priority':obj['attention_priority'],'domains':obj.get('domains',[]),'subject_key':obj.get('subject_key'),'monitoring_cadence':obj.get('monitoring_cadence'),'monitoring_signal_cadences':obj.get('monitoring_signal_cadences'),'monitoring_notification':obj.get('monitoring_notification'),'next_check_at':obj.get('next_check_at'),'schedule_execution':'not represented here; verify environment scheduler binding separately'},indent=2))

if __name__=='__main__':main()
