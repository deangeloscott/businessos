#!/usr/bin/env python3
"""Persist bounded research evidence without requiring an AURA playbook or Run."""
from _common import *
from canonical_store import schema_entry, validate_canonical, canonical_path, write_canonical
from validate_research_evidence import evidence_errors, public_source_locator_error, is_public_source, PUBLIC_NARRATIVE_TYPES, DIRECT_ACQUISITION_METHODS, DISCOVERY_ONLY_METHODS, KNOWN_ACQUISITION_METHODS, AUTHORITATIVE_POINTER_METHODS
import argparse, json, hashlib, shutil, re

SYSTEMS_ALLOWED=SYSTEMS
PREVALENCE_RE=re.compile(r'\b(single\s+most|most\s+common|top\s+(?:driver|reason|theme|factor|issue|complaint|priority)|dominant|#1|number\s+one|majority|overwhelmingly)\b',re.I)
SAMPLE_SCOPE_RE=re.compile(r'\b(sample|sampled|sampling|reviewed evidence|preserved evidence|bounded evidence|reviewed sources|sources reviewed|observed evidence|evidence reviewed)\b',re.I)
MEASURED_FREQUENCY_BASES={'representative_measurement','measured_population','complete_population'}
STATE_NAMESPACES={'instances','runtime','knowledge','attachments'}

def _check_frequency_claim(item,n):
    statement=str(item.get('statement') or '')
    if not PREVALENCE_RE.search(statement): return
    ext=item.get('extensions') if isinstance(item.get('extensions'),dict) else {}
    scope=item.get('scope') if isinstance(item.get('scope'),dict) else {}
    basis=ext.get('frequency_basis') or scope.get('frequency_basis')
    if SAMPLE_SCOPE_RE.search(statement) or basis in MEASURED_FREQUENCY_BASES: return
    raise ValueError(f'insight {n} uses a prevalence/superlative claim without sample scope or measured frequency_basis; phrase it as "in the sampled evidence..." or provide a measured population basis')

def _load_schema(title): return schema_entry(title)[1]
def _validate(title,obj): validate_canonical(title,obj)
def _id(prefix,seed): return f'{prefix}_{hashlib.sha256(seed.encode()).hexdigest()[:16]}'

def _base(typ,oid,bid,run_id,ts):
    d={'id':oid,'object_type':typ,'schema_version':'1.0.0','business_id':bid,'created_at':ts,'updated_at':ts,'lineage':[]}
    if run_id:d['lineage']=[run_id]
    return d

def _subject_refs(obj):
    values=obj.get('subject_refs') if isinstance(obj,dict) else []
    if not isinstance(values,list): return set()
    return {str(x).strip() for x in values if isinstance(x,str) and x.strip()}

def _require_subject_overlap(left,left_label,right,right_label):
    a=_subject_refs(left); b=_subject_refs(right)
    if a and b and not (a & b):raise ValueError(f'{left_label} subject_refs ({", ".join(sorted(a))}) do not overlap {right_label} subject_refs ({", ".join(sorted(b))}); do not attach evidence about one resolved subject to another')

def _copy_snapshot(bid,source_id,snapshot_path):
    src=resolve_storage_ref(snapshot_path)
    if not src.exists() or not src.is_file(): raise ValueError(f'snapshot_path does not exist: {snapshot_path}')
    ext=src.suffix.lower() or '.bin'; aid=_id('ast',f'{source_id}:{src.name}:{src.stat().st_size}')
    dest=ROOT/'instances'/bid/'assets'/'evidence'/f'{aid}{ext}';dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():shutil.copy2(src,dest)
    return aid,storage_ref(dest)

def _workspace_evidence_path(raw):
    if not isinstance(raw,str) or not raw.strip():return False
    try:path=resolve_storage_ref(raw).resolve();workspace=workspace_root().resolve()
    except Exception:return False
    if not path.exists() or not path.is_file() or not path.is_relative_to(workspace):return False
    rel=path.relative_to(workspace)
    return workspace_is_external() or (bool(rel.parts) and rel.parts[0] in STATE_NAMESPACES)

def _source_provenance(item,ref,acquisition,snapshot_path):
    supplied={key:item.get(key) for key in ('source_type','origin','access_scope') if isinstance(item.get(key),str) and item.get(key).strip()}
    if len(supplied)==3:return {**supplied,'resolution':'caller_declared'}
    workspace_supplied=_workspace_evidence_path(ref) or _workspace_evidence_path(snapshot_path)
    ref_is_http=ref.lower().startswith(('http://','https://'))
    organization_supplied=workspace_supplied or acquisition in {'uploaded_document','first_party_export'} or (acquisition=='user_provided' and not ref_is_http)
    declared_public_type=supplied.get('source_type') in PUBLIC_NARRATIVE_TYPES and ref.lower().startswith(('http://','https://'))
    if declared_public_type:
        if any(key in supplied for key in ('origin','access_scope')):
            missing=sorted({'source_type','origin','access_scope'}-set(supplied));raise ValueError(f'public source provenance is only partially declared for {ref!r}; specify {", ".join(missing)}')
        return {'source_type':supplied['source_type'],'origin':'public web','access_scope':'public','resolution':'declared_public_source_type'}
    if organization_supplied:
        if any(key in supplied for key in ('origin','access_scope')):
            missing=sorted({'source_type','origin','access_scope'}-set(supplied));raise ValueError(f'source provenance is only partially declared for organization-supplied evidence {ref!r}; specify {", ".join(missing)} or omit all provenance fields so the exact workspace/acquisition metadata can be preserved')
        source_type=supplied.get('source_type') or ('first_party_export' if acquisition=='first_party_export' else 'organization_supplied_file')
        return {'source_type':source_type,'origin':'organization supplied','access_scope':'business_internal','resolution':'exact_workspace_reference' if workspace_supplied else f'acquisition_method:{acquisition}'}
    missing=sorted({'source_type','origin','access_scope'}-set(supplied))
    raise ValueError(f'cannot determine source provenance mechanically for {ref!r}; specify {", ".join(missing)}. AURA will not default ambiguous evidence to public web.')

def _method_extensions(workflow_id,method_type,method_ref):
    ext={}
    if workflow_id:ext['workflow_id']=workflow_id
    if method_type or method_ref:ext['businessos_method']={k:v for k,v in {'method_type':method_type,'method_ref':method_ref}.items() if v}
    return ext

def _source(bid,item,run_id,workflow_id,method_type,method_ref,ts):
    ref=str(item.get('source_reference') or '').strip()
    if not ref: raise ValueError('each source requires source_reference')
    text=item.get('captured_text');payload=item.get('record_payload');snap=item.get('snapshot_path');pointer=item.get('evidence_pointer')
    acquisition=str(item.get('acquisition_method') or item.get('retrieval_method') or 'unknown').strip()
    if acquisition not in KNOWN_ACQUISITION_METHODS:raise ValueError(f'unknown acquisition_method {acquisition!r}; use one of: {", ".join(sorted(KNOWN_ACQUISITION_METHODS))}')
    provenance=_source_provenance(item,ref,acquisition,snap)
    content_basis=text if isinstance(text,str) and text else (json.dumps(payload,sort_keys=True,ensure_ascii=False) if payload is not None else None)
    ch='sha256:'+hashlib.sha256(content_basis.encode('utf-8')).hexdigest() if content_basis else None
    sid=item.get('id') or _id('src',f'{ref}:{ch or pointer or "pointer"}')
    asset_refs=[];asset_objs=[]
    if snap:
        aid,loc=_copy_snapshot(bid,sid,snap);asset_refs.append(aid)
        a=_base('Asset',aid,bid,run_id,ts);ext=_method_extensions(workflow_id,method_type,method_ref);ext['source_ref']=sid
        a.update({'asset_type':'evidence_snapshot','owner_system':item.get('owner_system') or 'core','business_role':'source evidence preservation','location_reference':loc,'version':'1','status':'active','extensions':ext})
        _validate('Asset',a);asset_objs.append(a)
    if text or payload is not None or asset_refs:
        status='captured';method='mixed' if sum(bool(x) for x in [text,payload is not None,asset_refs])>1 else ('text_excerpt' if text else ('api_record' if payload is not None else 'snapshot'))
    elif pointer:status='external_pointer';method='external_pointer'
    else:status='pointer_only';method='reference_only'
    ev={'capture_status':status,'capture_method':item.get('capture_method') or method,'acquisition_method':acquisition,'acquisition_reference':item.get('acquisition_reference'),'captured_text':text,'title':item.get('title'),'author_label':item.get('author_label'),'rating':item.get('rating'),'context':item.get('context'),'asset_refs':asset_refs,'evidence_pointer':pointer,'record_payload':payload,'capture_notes':item.get('capture_notes'),'provenance_resolution':provenance['resolution']}
    ev={k:v for k,v in ev.items() if v is not None and v!=[]}
    extensions={'businessos_evidence':ev,**_method_extensions(workflow_id,method_type,method_ref)}
    s=_base('SourceRecord',sid,bid,run_id,ts);s.update({'source_type':provenance['source_type'],'source_reference':ref,'subject_refs':item.get('subject_refs',[]),'origin':provenance['origin'],'retrieved_at':item.get('retrieved_at') or ts,'published_at':item.get('published_at'),'content_hash':ch,'access_scope':provenance['access_scope'],'extensions':extensions})
    _validate('SourceRecord',s);return s,asset_objs

def _path_for(bid,obj):return canonical_path(bid,obj)
def _write(obj):
    p=_path_for(obj['business_id'],obj)
    if p.exists():
        old=json.loads(p.read_text())
        if old==obj:return p
    return write_canonical(obj,p)

def persist(bid,bundle):
    base=ROOT/'instances'/bid
    if not base.exists():raise ValueError(f'Unknown business: {bid}; initialize it before research persistence')
    workflow_id=str(bundle.get('workflow_id') or '').strip() or None
    reg=load_registry();match=next((c for c in reg['workflows'] if c.get('id')==workflow_id),None) if workflow_id else None
    if workflow_id and not match:raise ValueError(f'Unknown workflow_id: {workflow_id}')
    method_type=str(bundle.get('method_type') or '').strip() or ('aura_playbook' if workflow_id else None)
    method_ref=str(bundle.get('method_ref') or '').strip() or workflow_id
    if method_type and method_type not in {'aura_playbook','external_skill','model_created','ad_hoc'}:raise ValueError(f'Unknown method_type: {method_type}')
    owner=bundle.get('owner_system') or (match.get('owner_system') if match else None) or 'core'
    if owner not in SYSTEMS_ALLOWED:raise ValueError(f'Unknown owner_system: {owner}')
    seed=workflow_id or method_ref or method_type or 'research';run_id=bundle.get('run_id');ts=now();written=[]

    src_objs=[];asset_objs=[]
    for item in bundle.get('sources',[]):
        item=dict(item);item.setdefault('owner_system',owner)
        s,assets=_source(bid,item,run_id,workflow_id,method_type,method_ref,ts);src_objs.append(s);asset_objs.extend(assets)
    src_ids=[s['id'] for s in src_objs]

    obs_objs=[]
    for n,item in enumerate(bundle.get('observations',[])):
        refs=[]
        for i in item.get('source_indexes',[]):
            if not isinstance(i,int) or i<0 or i>=len(src_ids):raise ValueError(f'observation {n} source_indexes contains invalid index {i!r}')
            refs.append(src_ids[i])
        refs += [r for r in item.get('source_refs',[]) if r not in refs]
        if not refs:raise ValueError(f'observation {n} requires source_indexes/source_refs')
        oid=item.get('id') or _id('obs',f'{bid}:{seed}:{item.get("statement")}:{"|".join(refs)}')
        ext=dict(item.get('extensions',{}));ext.update({k:v for k,v in _method_extensions(workflow_id,method_type,method_ref).items() if k not in ext})
        o=_base('Observation',oid,bid,run_id,ts);o.update({'producer_system':item.get('producer_system') or owner,'observation_type':item.get('observation_type') or 'research_observation','subject_refs':item.get('subject_refs',[]),'statement':item.get('statement'),'source_refs':refs,'observed_at':item.get('observed_at') or ts,'method':item.get('method') or 'source_inspection','extraction_confidence':item.get('extraction_confidence'),'extensions':ext})
        _validate('Observation',o);obs_objs.append(o)
    obs_ids=[o['id'] for o in obs_objs]

    ins_objs=[]
    for n,item in enumerate(bundle.get('insights',[])):
        links=[]
        for i in item.get('observation_indexes',[]):
            if not isinstance(i,int) or i<0 or i>=len(obs_ids):raise ValueError(f'insight {n} observation_indexes contains invalid index {i!r}')
            links.append({'ref':obs_ids[i],'relationship':'supports'})
        links += item.get('evidence_links',[]);status=item.get('status') or 'candidate'
        if status in {'supported','active'} and not links:raise ValueError(f'insight {n} status={status} requires supporting observations/evidence')
        if status in {'supported','active'}:_check_frequency_claim(item,n)
        iid=item.get('id') or _id('ins',f'{bid}:{seed}:{item.get("statement")}')
        ext=dict(item.get('extensions',{}));ext.update({k:v for k,v in _method_extensions(workflow_id,method_type,method_ref).items() if k not in ext})
        ins=_base('Insight',iid,bid,run_id,ts);ins.update({'owner_system':item.get('owner_system') or owner,'insight_type':item.get('insight_type') or 'research_insight','statement':item.get('statement'),'subject_refs':item.get('subject_refs',[]),'evidence_links':links,'confidence':item.get('confidence',0.5),'scope':item.get('scope',{}),'status':status,'reviewed_at':item.get('reviewed_at'),'extensions':ext})
        _validate('Insight',ins);ins_objs.append(ins)
    ins_ids=[i['id'] for i in ins_objs]

    cmp_objs=[]
    for n,item in enumerate(bundle.get('competitors',[])):
        name=str(item.get('name') or '').strip()
        if not name:raise ValueError(f'competitor {n} requires name')
        obsrefs=[obs_ids[i] for i in item.get('observation_indexes',[]) if isinstance(i,int) and 0<=i<len(obs_ids)]
        insrefs=[ins_ids[i] for i in item.get('insight_indexes',[]) if isinstance(i,int) and 0<=i<len(ins_ids)]
        cid=item.get('id') or _id('cmp',f'{bid}:{name.lower()}')
        if any(item.get(k) for k in ['positioning_summary','strategic_summary','strengths','weaknesses']) and not (obsrefs or insrefs):raise ValueError(f'competitor {n} interpretation/strengths/weaknesses require observation_indexes or insight_indexes; preserve evidence before strategic interpretation')
        ext=dict(item.get('extensions',{}));ext.update({k:v for k,v in _method_extensions(workflow_id,method_type,method_ref).items() if k not in ext})
        c=_base('Competitor',cid,bid,run_id,ts);c.update({'name':name,'identities':{'official_domains':item.get('official_domains',[]),'aliases':item.get('aliases',[]),'profiles':item.get('profiles',[])},'competitor_type':item.get('competitor_type') or 'observed competitor','markets':item.get('markets',[]),'audiences':item.get('audiences',[]),'categories':item.get('categories',[]),'products_services':item.get('products_services',[]),'known_offers':item.get('known_offers',[]),'known_pricing':item.get('known_pricing',[]),'positioning_summary':item.get('positioning_summary'),'strategic_summary':item.get('strategic_summary'),'strengths':item.get('strengths',[]),'weaknesses':item.get('weaknesses',[]),'active_insight_refs':insrefs,'observation_refs':obsrefs,'last_reviewed':item.get('last_reviewed') or ts,'confidence':item.get('confidence',0.5),'extensions':ext})
        _validate('Competitor',c);cmp_objs.append(c)

    all_objs=asset_objs+src_objs+obs_objs+ins_objs+cmp_objs
    public_sources={s['id']:s for s in src_objs};observation_map={o['id']:o for o in obs_objs};insight_map={i['id']:i for i in ins_objs}
    for o in obs_objs:
        for ref in o['source_refs']:
            s=public_sources.get(ref)
            if s:_require_subject_overlap(o,o['id'],s,ref)
            if s and is_public_source(s):
                ev=s.get('extensions',{}).get('businessos_evidence',{});acquisition=ev.get('acquisition_method') or 'unknown';status=ev.get('capture_status')
                adequate=(status=='captured' and acquisition in DIRECT_ACQUISITION_METHODS and (ev.get('captured_text') or ev.get('asset_refs') or ev.get('record_payload') is not None)) or (status=='external_pointer' and ev.get('evidence_pointer') and acquisition in AUTHORITATIVE_POINTER_METHODS)
                if not adequate:raise ValueError(f'Observation {o["id"]} cannot rely on public source {ref} acquired as {acquisition!r} with capture_status={status!r}; search/snippet discovery is not support. Open/retrieve the underlying source or use an authoritative reproducible record.')
    for ins in ins_objs:
        if ins.get('status') not in {'supported','active'}:continue
        for link in ins.get('evidence_links') or []:
            if not isinstance(link,dict) or link.get('relationship') not in {'supports','derived_from'}:continue
            ref=link.get('ref');evidence=observation_map.get(ref) or public_sources.get(ref)
            if evidence:_require_subject_overlap(ins,ins['id'],evidence,ref)
    for c in cmp_objs:
        for ref in c.get('observation_refs',[]):
            evidence=observation_map.get(ref)
            if evidence and _subject_refs(evidence) and c['id'] not in _subject_refs(evidence):raise ValueError(f'Competitor {c["id"]} cannot attach Observation {ref} scoped to {", ".join(sorted(_subject_refs(evidence)))}; preserve subject-relevant evidence for this competitor')
        for ref in c.get('active_insight_refs',[]):
            evidence=insight_map.get(ref)
            if evidence and _subject_refs(evidence) and c['id'] not in _subject_refs(evidence):raise ValueError(f'Competitor {c["id"]} cannot attach Insight {ref} scoped to {", ".join(sorted(_subject_refs(evidence)))}; preserve subject-relevant evidence for this competitor')
    for source in src_objs:
        locator_error=public_source_locator_error(source)
        if locator_error:raise ValueError(locator_error)
    for obj in all_objs:written.append((obj,_write(obj)))
    errs,warns=evidence_errors(bid)
    if errs:raise ValueError('research evidence validation failed after write: '+'; '.join(errs))
    return written,warns

def main():
    epilog='''Bundle shape (small example):
{
  "method_type": "external_skill",
  "method_ref": "competitor-research-skill",
  "sources": [
    {"source_type":"review_platform","source_reference":"https://...","subject_refs":["cmp_..."],"acquisition_method":"direct_page_read","captured_text":"Exact review text...","rating":1}
  ],
  "observations": [
    {"statement":"Reviewer reported surprise charges.","subject_refs":["cmp_..."],"source_indexes":[0],"observation_type":"customer_complaint"}
  ],
  "insights": [
    {"statement":"Unexpected charges are a recurring concern in the sampled evidence.","subject_refs":["cmp_..."],"observation_indexes":[0],"status":"supported","confidence":0.7}
  ]
}

`workflow_id` is optional and should be supplied only when an AURA playbook was actually selected. External Skill, model-created, and ad-hoc research may instead use method_type/method_ref or omit method provenance when it is not materially useful. `run_id` is optional.

Declare acquisition_method separately from capture_method. Discovery-only methods such as search_result, search_snippet, directory_preview, ai_summary, unvisited_url, or unknown may be saved, but cannot support an Observation even if captured_text is present. For any source whose provenance is not mechanically determined, specify source_type, origin, and access_scope; AURA will not guess public provenance. Preserve subject_refs when a source/observation/insight concerns a resolved material subject.'''
    p=argparse.ArgumentParser(description='Persist bounded SourceRecords/evidence/Observations/Insights/Competitors from any truthful research method; an AURA contract is optional.',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
    p.add_argument('business_id');p.add_argument('--bundle-file',required=True);a=p.parse_args()
    try:bundle=json.loads(Path(a.bundle_file).read_text());written,warns=persist(a.business_id,bundle)
    except (ValueError,FileExistsError,json.JSONDecodeError) as e:raise SystemExit(str(e)+'\nSupported path: run `python3 scripts/persist_research_bundle.py --help`; do not create a replacement canonical writer.')
    print(json.dumps({'business_id':a.business_id,'objects_written':[{'id':o['id'],'object_type':o['object_type'],'path':storage_ref(p)} for o,p in written],'warnings':warns,'next_validation':f'python3 scripts/validate_business.py {a.business_id} --require-context'},indent=2))

if __name__=='__main__':main()
