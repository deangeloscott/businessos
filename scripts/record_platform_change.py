#!/usr/bin/env python3
from _common import *
import argparse,json,hashlib


def norm(s): return ' '.join(s.split()).strip()
def fingerprint(s): return 'sha256:'+hashlib.sha256(norm(s).encode()).hexdigest()
def semantic(platform,topic): return f'{slug(platform)}:{slug(topic)}'
def pid(bid,key,fp):
    digest=hashlib.sha256((key+'\0'+fp).encode()).hexdigest()[:16]
    return f'plc_{bid}_{digest}'
def records(bid,key):
    return [(o,p) for o,p in iter_instance_objects(bid) if o.get('object_type')=='PlatformChange' and o.get('semantic_key')==key]


def record(bid,platform,topic,state_summary,authority='unknown',materiality='unknown',change_summary=None,effective_at=None,source_refs=None,evidence_refs=None,affected_workflow_refs=None,affected_object_refs=None,verified_at=None,reverify_current=False):
    verified_at=verified_at or now();source_refs=source_refs or [];evidence_refs=evidence_refs or [];affected_workflow_refs=affected_workflow_refs or [];affected_object_refs=affected_object_refs or []
    if authority=='unknown': raise ValueError('verified PlatformChange requires a non-unknown authority classification')
    if not (source_refs or evidence_refs): raise ValueError('verified PlatformChange requires --source-ref and/or --evidence-ref provenance')
    key=semantic(platform,topic);fp=fingerprint(state_summary);found=records(bid,key);current=[x for x in found if x[0].get('status')=='current']
    if len(current)>1: raise ValueError(f'multiple current PlatformChange objects exist for {key}; validate/repair before recording')

    # Semantic equivalence is a reasoning judgment, not a string-equality problem.
    # When authoritative evidence restates the same material state in different words,
    # the caller explicitly requests re-verification. AURA keeps the durable state and
    # provenance without trying to decide semantic equivalence deterministically.
    if reverify_current:
        if not current:raise ValueError(f'--reverify-current requires an existing current PlatformChange for {key}')
        obj,p=current[0]
        obj['updated_at']=verified_at;obj['last_verified_at']=verified_at;obj['verification_count']=int(obj.get('verification_count',0))+1
        for field,new_refs in [('source_refs',source_refs),('evidence_refs',evidence_refs),('affected_workflow_refs',affected_workflow_refs),('affected_object_refs',affected_object_refs)]:obj[field]=sorted(set(obj.get(field,[])+new_refs))
        obj['lineage']=sorted(set((obj.get('lineage') or [])+source_refs+evidence_refs))
        hist=obj.setdefault('extensions',{}).setdefault('verification_history',[])
        hist.append({'verified_at':verified_at,'classification':'reverified_no_material_change','observed_state_summary':norm(state_summary),'observed_state_fingerprint':fp,'source_refs':sorted(set(source_refs)),'evidence_refs':sorted(set(evidence_refs)),'note':change_summary})
        if obj.get('authority')=='unknown' and authority!='unknown':obj['authority']=authority
        if obj.get('materiality')=='unknown' and materiality!='unknown':obj['materiality']=materiality
        p.write_text(json.dumps(obj,indent=2)+'\n');return obj,p,'reverified'

    if current and current[0][0].get('state_fingerprint')==fp:
        obj,p=current[0];obj['updated_at']=verified_at;obj['last_verified_at']=verified_at;obj['verification_count']=int(obj.get('verification_count',0))+1
        for field,new_refs in [('source_refs',source_refs),('evidence_refs',evidence_refs),('affected_workflow_refs',affected_workflow_refs),('affected_object_refs',affected_object_refs)]:obj[field]=sorted(set(obj.get(field,[])+new_refs))
        obj['lineage']=sorted(set((obj.get('lineage') or [])+source_refs+evidence_refs))
        if change_summary:obj['change_summary']=change_summary
        if effective_at:obj['effective_at']=effective_at
        if obj.get('authority')=='unknown' and authority!='unknown':obj['authority']=authority
        if obj.get('materiality')=='unknown' and materiality!='unknown':obj['materiality']=materiality
        p.write_text(json.dumps(obj,indent=2)+'\n');return obj,p,'refreshed'

    prior=current[0] if current else None
    new_id=pid(bid,key,fp);p=ROOT/'instances'/bid/'intelligence'/'platform-changes'/f'{new_id}.json';p.parent.mkdir(parents=True,exist_ok=True)
    obj={
        'id':new_id,'object_type':'PlatformChange','schema_version':'1.0.0','business_id':bid,
        'created_at':verified_at,'updated_at':verified_at,
        'lineage':sorted(set(source_refs+evidence_refs+([prior[0]['id']] if prior else []))),
        'platform':platform,'topic':topic,'semantic_key':key,'state_summary':norm(state_summary),'state_fingerprint':fp,'change_summary':change_summary,
        'status':'current','authority':authority,'materiality':materiality,'effective_at':effective_at,
        'first_verified_at':verified_at,'last_verified_at':verified_at,'verification_count':1,
        'source_refs':sorted(set(source_refs)),'evidence_refs':sorted(set(evidence_refs)),
        'affected_workflow_refs':sorted(set(affected_workflow_refs)),'affected_object_refs':sorted(set(affected_object_refs)),
        'supersedes':prior[0]['id'] if prior else None,'superseded_by':None,'extensions':{}
    }
    if prior:
        old,op=prior;old['status']='superseded';old['superseded_by']=new_id;old['updated_at']=verified_at;op.write_text(json.dumps(old,indent=2)+'\n')
    p.write_text(json.dumps(obj,indent=2)+'\n');return obj,p,'changed' if prior else 'created'


def main():
    ap=argparse.ArgumentParser(description='Record/reverify organization-owned external platform state without modifying AURA software.')
    ap.add_argument('business_id');ap.add_argument('--platform',required=True);ap.add_argument('--topic',required=True);ap.add_argument('--state',dest='state_summary',required=True)
    ap.add_argument('--authority',choices=['official_platform','formal_standard','first_party_platform','high_quality_research','corroborated_external','community_signal','unknown'],default='unknown')
    ap.add_argument('--materiality',choices=['not_material','low','medium','high','critical','unknown'],default='unknown')
    ap.add_argument('--change-summary');ap.add_argument('--effective-at');ap.add_argument('--source-ref',action='append',default=[]);ap.add_argument('--evidence-ref',action='append',default=[])
    ap.add_argument('--affected-workflow-ref',action='append',default=[]);ap.add_argument('--affected-object-ref',action='append',default=[]);ap.add_argument('--verified-at')
    ap.add_argument('--reverify-current',action='store_true',help='Authoritative evidence semantically re-verifies the existing current state despite different wording; refresh current identity and retain observed wording/provenance in verification history.')
    a=ap.parse_args()
    if not (ROOT/'instances'/a.business_id).exists():raise SystemExit(f'Unknown business: {a.business_id}')
    try:o,p,result=record(a.business_id,a.platform,a.topic,a.state_summary,a.authority,a.materiality,a.change_summary,a.effective_at,a.source_ref,a.evidence_ref,a.affected_workflow_ref,a.affected_object_ref,a.verified_at,a.reverify_current)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps({'platform_change_id':o['id'],'semantic_key':o['semantic_key'],'status':o['status'],'result':result,'verification_count':o['verification_count'],'path':storage_ref(p)},indent=2))

if __name__=='__main__':main()
