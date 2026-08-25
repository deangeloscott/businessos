#!/usr/bin/env python3
"""Persist bounded research evidence without requiring agents to hand-author canonical schemas."""
from _common import *
from jsonschema import Draft202012Validator
from validate_research_evidence import evidence_errors, DIRECT_ACQUISITION_METHODS, DISCOVERY_ONLY_METHODS, KNOWN_ACQUISITION_METHODS, AUTHORITATIVE_POINTER_METHODS
import argparse, json, hashlib, shutil, secrets, re

SYSTEMS_ALLOWED=SYSTEMS

PREVALENCE_RE=re.compile(r'\b(single\s+most|most\s+common|top\s+(?:driver|reason|theme|factor|issue|complaint|priority)|dominant|#1|number\s+one|majority|overwhelmingly)\b',re.I)
SAMPLE_SCOPE_RE=re.compile(r'\b(sample|sampled|sampling|reviewed evidence|preserved evidence|bounded evidence|reviewed sources|sources reviewed|observed evidence|evidence reviewed)\b',re.I)
MEASURED_FREQUENCY_BASES={'representative_measurement','measured_population','complete_population'}

def _check_frequency_claim(item,n):
    statement=str(item.get('statement') or '')
    if not PREVALENCE_RE.search(statement): return
    ext=item.get('extensions') if isinstance(item.get('extensions'),dict) else {}
    scope=item.get('scope') if isinstance(item.get('scope'),dict) else {}
    basis=ext.get('frequency_basis') or scope.get('frequency_basis')
    if SAMPLE_SCOPE_RE.search(statement) or basis in MEASURED_FREQUENCY_BASES: return
    raise ValueError(f'insight {n} uses a prevalence/superlative claim without sample scope or measured frequency_basis; phrase it as "in the sampled evidence..." or provide a measured population basis')


def _load_schema(title):
    reg=json.loads((ROOT/'generated/schema-registry.json').read_text())
    row=next((x for x in reg if x.get('title')==title),None)
    if not row: raise ValueError(f'Unknown schema title: {title}')
    return json.loads((ROOT/row['path']).read_text())


def _validate(title,obj):
    errs=sorted(Draft202012Validator(_load_schema(title)).iter_errors(obj),key=lambda e:list(e.path))
    if errs: raise ValueError(f'{title} invalid: '+'; '.join(f'{list(e.path)} {e.message}' for e in errs))


def _id(prefix,seed):
    return f'{prefix}_{hashlib.sha256(seed.encode()).hexdigest()[:16]}'


def _base(typ,oid,bid,run_id,ts):
    d={'id':oid,'object_type':typ,'schema_version':'1.0.0','business_id':bid,'created_at':ts,'updated_at':ts,'lineage':[]}
    if run_id: d['lineage']=[run_id]
    return d


def _copy_snapshot(bid, source_id, snapshot_path):
    src=Path(snapshot_path)
    if not src.is_absolute(): src=ROOT/src
    if not src.exists() or not src.is_file(): raise ValueError(f'snapshot_path does not exist: {snapshot_path}')
    ext=src.suffix.lower() or '.bin'; aid=_id('ast',f'{source_id}:{src.name}:{src.stat().st_size}')
    dest=ROOT/'instances'/bid/'assets'/'evidence'/f'{aid}{ext}'; dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists(): shutil.copy2(src,dest)
    return aid,str(dest.relative_to(ROOT))


def _source(bid,item,run_id,contract_id,ts):
    ref=str(item.get('source_reference') or '').strip()
    if not ref: raise ValueError('each source requires source_reference')
    text=item.get('captured_text')
    payload=item.get('record_payload')
    snap=item.get('snapshot_path')
    pointer=item.get('evidence_pointer')
    acquisition=str(item.get('acquisition_method') or item.get('retrieval_method') or 'unknown').strip()
    if acquisition not in KNOWN_ACQUISITION_METHODS:
        raise ValueError(f'unknown acquisition_method {acquisition!r}; use one of: {", ".join(sorted(KNOWN_ACQUISITION_METHODS))}')
    content_basis=text if isinstance(text,str) and text else (json.dumps(payload,sort_keys=True,ensure_ascii=False) if payload is not None else None)
    ch='sha256:'+hashlib.sha256(content_basis.encode('utf-8')).hexdigest() if content_basis else None
    sid=item.get('id') or _id('src',f'{ref}:{ch or pointer or "pointer"}')
    asset_refs=[]; asset_objs=[]
    if snap:
        aid,loc=_copy_snapshot(bid,sid,snap); asset_refs.append(aid)
        a=_base('Asset',aid,bid,run_id,ts); a.update({'asset_type':'evidence_snapshot','owner_system':item.get('owner_system') or 'core','business_role':'source evidence preservation','location_reference':loc,'version':'1','status':'active','extensions':{'source_ref':sid,'contract_id':contract_id}})
        _validate('Asset',a); asset_objs.append(a)
    if text or payload is not None or asset_refs:
        status='captured'; method='mixed' if sum(bool(x) for x in [text,payload is not None,asset_refs])>1 else ('text_excerpt' if text else ('api_record' if payload is not None else 'snapshot'))
    elif pointer:
        status='external_pointer'; method='external_pointer'
    else:
        status='pointer_only'; method='reference_only'
    ev={
        'capture_status':status,'capture_method':item.get('capture_method') or method,
        'acquisition_method':acquisition,'acquisition_reference':item.get('acquisition_reference'),
        'captured_text':text,'title':item.get('title'),'author_label':item.get('author_label'),
        'rating':item.get('rating'),'context':item.get('context'),'asset_refs':asset_refs,
        'evidence_pointer':pointer,'record_payload':payload,'capture_notes':item.get('capture_notes')
    }
    ev={k:v for k,v in ev.items() if v is not None and v!=[]}
    s=_base('SourceRecord',sid,bid,run_id,ts); s.update({
        'source_type':item.get('source_type') or 'webpage','source_reference':ref,'origin':item.get('origin') or 'public web',
        'retrieved_at':item.get('retrieved_at') or ts,'published_at':item.get('published_at'),'content_hash':ch,
        'access_scope':item.get('access_scope') or 'public','extensions':{'businessos_evidence':ev,'contract_id':contract_id}
    })
    _validate('SourceRecord',s)
    return s,asset_objs


def _path_for(bid,obj):
    base=ROOT/'instances'/bid; typ=obj['object_type']; oid=obj['id']
    mapping={
        'SourceRecord':base/'intelligence/sources'/f'{oid}.json',
        'Observation':base/'intelligence/observations'/f'{oid}.json',
        'Insight':base/'intelligence/insights'/f'{oid}.json',
        'Asset':base/'assets'/f'{oid}.json',
        'Competitor':base/'context/competitors'/f'{oid}.json',
    }
    if typ not in mapping: raise ValueError(f'Unsupported research bundle object type: {typ}')
    return mapping[typ]


def _write(obj):
    p=_path_for(obj['business_id'],obj); p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        old=json.loads(p.read_text())
        if old==obj: return p
        raise FileExistsError(f'Refusing to overwrite existing canonical object: {p.relative_to(ROOT)}')
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
    return p


def persist(bid,bundle):
    base=ROOT/'instances'/bid
    if not base.exists(): raise ValueError(f'Unknown business: {bid}; initialize/bootstrap it before research persistence')
    contract_id=str(bundle.get('contract_id') or '').strip()
    if not contract_id: raise ValueError('bundle requires contract_id')
    reg=load_registry(); match=next((c for c in reg['contracts'] if c.get('id')==contract_id),None)
    if not match: raise ValueError(f'Unknown contract_id: {contract_id}')
    owner=bundle.get('owner_system') or match.get('owner_system') or 'core'
    if owner not in SYSTEMS_ALLOWED: raise ValueError(f'Unknown owner_system: {owner}')
    run_id=bundle.get('run_id'); ts=now(); written=[]

    src_objs=[]; asset_objs=[]
    for item in bundle.get('sources',[]):
        item=dict(item); item.setdefault('owner_system',owner)
        s,assets=_source(bid,item,run_id,contract_id,ts); src_objs.append(s); asset_objs.extend(assets)
    src_ids=[s['id'] for s in src_objs]

    obs_objs=[]
    for n,item in enumerate(bundle.get('observations',[])):
        refs=[]
        for i in item.get('source_indexes',[]):
            if not isinstance(i,int) or i<0 or i>=len(src_ids): raise ValueError(f'observation {n} source_indexes contains invalid index {i!r}')
            refs.append(src_ids[i])
        refs += [r for r in item.get('source_refs',[]) if r not in refs]
        if not refs: raise ValueError(f'observation {n} requires source_indexes/source_refs')
        oid=item.get('id') or _id('obs',f'{bid}:{contract_id}:{item.get("statement")}:{"|".join(refs)}')
        o=_base('Observation',oid,bid,run_id,ts); o.update({
            'producer_system':item.get('producer_system') or owner,'observation_type':item.get('observation_type') or 'research_observation',
            'subject_refs':item.get('subject_refs',[]),'statement':item.get('statement'),'source_refs':refs,
            'observed_at':item.get('observed_at') or ts,'method':item.get('method') or 'source_inspection',
            'extraction_confidence':item.get('extraction_confidence'),'extensions':item.get('extensions',{})
        })
        _validate('Observation',o); obs_objs.append(o)
    obs_ids=[o['id'] for o in obs_objs]

    ins_objs=[]
    for n,item in enumerate(bundle.get('insights',[])):
        links=[]
        for i in item.get('observation_indexes',[]):
            if not isinstance(i,int) or i<0 or i>=len(obs_ids): raise ValueError(f'insight {n} observation_indexes contains invalid index {i!r}')
            links.append({'ref':obs_ids[i],'relationship':'supports'})
        links += item.get('evidence_links',[])
        status=item.get('status') or 'candidate'
        if status in {'supported','active'} and not links: raise ValueError(f'insight {n} status={status} requires supporting observations/evidence')
        if status in {'supported','active'}: _check_frequency_claim(item,n)
        iid=item.get('id') or _id('ins',f'{bid}:{contract_id}:{item.get("statement")}')
        ins=_base('Insight',iid,bid,run_id,ts); ins.update({
            'owner_system':item.get('owner_system') or owner,'insight_type':item.get('insight_type') or 'research_insight',
            'statement':item.get('statement'),'subject_refs':item.get('subject_refs',[]),'evidence_links':links,
            'confidence':item.get('confidence',0.5),'scope':item.get('scope',{}),'status':status,'reviewed_at':item.get('reviewed_at'),
            'extensions':item.get('extensions',{})
        })
        _validate('Insight',ins); ins_objs.append(ins)
    ins_ids=[i['id'] for i in ins_objs]

    cmp_objs=[]
    for n,item in enumerate(bundle.get('competitors',[])):
        name=str(item.get('name') or '').strip()
        if not name: raise ValueError(f'competitor {n} requires name')
        obsrefs=[obs_ids[i] for i in item.get('observation_indexes',[]) if isinstance(i,int) and 0<=i<len(obs_ids)]
        insrefs=[ins_ids[i] for i in item.get('insight_indexes',[]) if isinstance(i,int) and 0<=i<len(ins_ids)]
        cid=item.get('id') or _id('cmp',f'{bid}:{name.lower()}')
        if any(item.get(k) for k in ['positioning_summary','strategic_summary','strengths','weaknesses']) and not (obsrefs or insrefs):
            raise ValueError(f'competitor {n} interpretation/strengths/weaknesses require observation_indexes or insight_indexes; preserve evidence before strategic interpretation')
        c=_base('Competitor',cid,bid,run_id,ts); c.update({
            'name':name,
            'identities':{'official_domains':item.get('official_domains',[]),'aliases':item.get('aliases',[]),'profiles':item.get('profiles',[])},
            'competitor_type':item.get('competitor_type') or 'observed competitor','markets':item.get('markets',[]),'audiences':item.get('audiences',[]),
            'categories':item.get('categories',[]),'products_services':item.get('products_services',[]),'known_offers':item.get('known_offers',[]),'known_pricing':item.get('known_pricing',[]),
            'positioning_summary':item.get('positioning_summary'),'strategic_summary':item.get('strategic_summary'),'strengths':item.get('strengths',[]),'weaknesses':item.get('weaknesses',[]),
            'active_insight_refs':insrefs,'observation_refs':obsrefs,'last_reviewed':item.get('last_reviewed') or ts,'confidence':item.get('confidence',0.5),
            'extensions':item.get('extensions',{})
        })
        _validate('Competitor',c); cmp_objs.append(c)

    all_objs=asset_objs+src_objs+obs_objs+ins_objs+cmp_objs
    # Validate semantic support in-memory before writes where possible.
    public_sources={s['id']:s for s in src_objs}
    for o in obs_objs:
        for ref in o['source_refs']:
            s=public_sources.get(ref)
            if s and s.get('access_scope')=='public':
                ev=s.get('extensions',{}).get('businessos_evidence',{})
                acquisition=ev.get('acquisition_method') or 'unknown'
                status=ev.get('capture_status')
                adequate=(status=='captured' and acquisition in DIRECT_ACQUISITION_METHODS and (ev.get('captured_text') or ev.get('asset_refs') or ev.get('record_payload') is not None)) or (status=='external_pointer' and ev.get('evidence_pointer') and acquisition in AUTHORITATIVE_POINTER_METHODS)
                if not adequate:
                    raise ValueError(f'Observation {o["id"]} cannot rely on public source {ref} acquired as {acquisition!r} with capture_status={status!r}; search/snippet discovery is not support. Open/retrieve the underlying source or use an authoritative reproducible record.')

    for obj in all_objs:
        written.append((obj,_write(obj)))

    # Full post-write validation includes cross-object evidence semantics.
    errs,warns=evidence_errors(bid)
    if errs:
        raise ValueError('research evidence validation failed after write: '+'; '.join(errs))
    return written,warns


def main():
    epilog='''Bundle shape (small example):
{
  "contract_id": "competitor.analysis.customer-sentiment",
  "run_id": "run_...",
  "sources": [
    {"source_type":"review_platform","source_reference":"https://...","acquisition_method":"direct_page_read","captured_text":"Exact review text...","rating":1}
  ],
  "observations": [
    {"statement":"Reviewer reported surprise charges.","source_indexes":[0],"observation_type":"customer_complaint"}
  ],
  "insights": [
    {"statement":"Unexpected charges are a recurring concern in the sampled evidence.","observation_indexes":[0],"status":"supported","confidence":0.7}
  ]
}

Declare acquisition_method separately from capture_method. Strong examples: direct_page_read, browser_read, browser_capture, api_response, downloaded_document, uploaded_document, user_provided, first_party_export, authoritative_record. Discovery-only methods such as search_result, search_snippet, directory_preview, ai_summary, unvisited_url, or unknown may be saved, but cannot support an Observation even if captured_text is present. Screenshots are useful when they add value; they are not required for every review. Supported/active superlative or prevalence claims (for example top, dominant, #1, most common) must be explicitly scoped to the sampled evidence unless a measured population basis is supplied.'''
    p=argparse.ArgumentParser(description='Persist SourceRecords, optional evidence Assets, Observations, Insights, and basic Competitor objects from a structured research bundle.',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=epilog)
    p.add_argument('business_id'); p.add_argument('--bundle-file',required=True); a=p.parse_args()
    try:
        bundle=json.loads(Path(a.bundle_file).read_text()); written,warns=persist(a.business_id,bundle)
    except (ValueError,FileExistsError,json.JSONDecodeError) as e:
        raise SystemExit(str(e)+'\nSupported path: run `python3 scripts/persist_research_bundle.py --help`; do not create a replacement canonical writer.')
    print(json.dumps({'business_id':a.business_id,'objects_written':[{'id':o['id'],'object_type':o['object_type'],'path':str(p.relative_to(ROOT))} for o,p in written],'warnings':warns,'next_validation':f'python3 scripts/validate_business.py {a.business_id} --require-context'},indent=2))

if __name__=='__main__': main()
