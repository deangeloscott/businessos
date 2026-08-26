#!/usr/bin/env python3
"""Reusable contract-completion evidence profiles for AURA Runs.

The deterministic layer does not judge business quality. It does prevent a Run from being
marked complete merely because some file exists. Contracts are mapped to a small set of
reusable evidence profiles and the supplied evidence must satisfy that profile before the
Run/subcontract may be recorded complete.
"""
from pathlib import Path
import json, re
from _common import *

CUSTOMER_FACING_ROLE='customer_facing_production_root'
TEXT_EXTS={'.md','.txt','.html','.htm','.rst','.csv','.json'}
MEDIA_EXTS={
    'image':{'.png','.jpg','.jpeg','.webp','.svg'},
    'gif':{'.gif','.webp','.mp4'},
    'audio':{'.mp3','.wav','.m4a','.aac','.ogg','.flac'},
    'video':{'.mp4','.mov','.webm','.m4v'},
    'presentation':{'.pptx','.pdf','.html'},
    'infographic':{'.png','.jpg','.jpeg','.webp','.svg','.pdf'},
}
TEXT_MIN_WORDS={
    'captions':12,'linkedin':35,'faq':70,'article':180,'case-study':180,
    'newsletter':120,'bullet-script':60,'landing-page':100,'advertorial':160,
    'comparison':100,'lead-magnet':140,'nurture':80,'email':50,
}


def _selector_types(items):
    out=set()
    for item in items or []:
        typ=item.get('type') if isinstance(item,dict) else item
        if isinstance(typ,str) and typ.strip(): out.add(typ.strip())
    return out


def contract_index():
    return {c['id']:c for c in load_registry().get('contracts',[]) if c.get('id')}


def completion_spec(contract):
    """Return the stable evidence profile for a contract.

    Explicit frontmatter `completion_evidence` overrides inference. Inference exists so the
    installed catalog gets useful protection without hundreds of bespoke validators.
    """
    explicit=contract.get('completion_evidence')
    if isinstance(explicit,str): explicit={'profile':explicit}
    explicit=explicit if isinstance(explicit,dict) else {}
    cid=str(contract.get('id','')).lower(); last=cid.split('.')[-1] if cid else ''
    writes=_selector_types(contract.get('writes'))
    if explicit.get('profile'):
        profile=str(explicit['profile'])
    elif '.qa.' in cid or cid.startswith('content.qa.') or cid.endswith('.qa'):
        profile='qa'
    elif contract.get('artifact_role')==CUSTOMER_FACING_ROLE:
        profile='production'
    elif contract.get('type')=='detector':
        profile='detector'
    elif '.publishing.' in cid or last in {'publish','publish-asset','schedule','distribution'}:
        profile='publishing'
    elif '.measurement.' in cid or 'OutcomeEvaluation' in writes or 'MetricObservation' in writes:
        profile='measurement'
    elif '.research.' in cid or 'SourceRecord' in writes:
        profile='research'
    elif '.strategy.' in cid or last.endswith('plan') or last.endswith('brief'):
        profile='planning'
    elif writes:
        profile='canonical_state'
    else:
        profile='generic'
    medium=explicit.get('medium')
    if not medium and profile=='production': medium=last
    return {
        'version':'1.0','profile':profile,'medium':medium,
        'declared_write_types':sorted(writes),'artifact_role':contract.get('artifact_role'),
        'allow_specification_fallback':bool(explicit.get('allow_specification_fallback', medium=='animation')),
        'require_subcontract_write_evidence':bool(explicit.get('require_subcontract_write_evidence',False)),
    }


def _paths(refs):
    out=[]
    for ref in refs or []:
        try:p=resolve_storage_ref(ref)
        except Exception:continue
        if p.exists() and p.is_file() and p.stat().st_size>0: out.append(p)
    return out


def _json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return None


def _objects_in_paths(paths,business_id=None):
    out=[]
    for p in paths:
        data=_json(p); vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if not isinstance(obj,dict) or not obj.get('object_type'): continue
            if business_id and obj.get('business_id')!=business_id: continue
            out.append((obj,p))
    return out


def _run_bound_objects(business_id,run_id):
    rel=f'runtime/runs/{business_id}/{run_id}'; out=[]
    for obj,path in iter_instance_objects(business_id):
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {}
        if bos.get('run_ref')==rel or bos.get('run_id')==run_id: out.append((obj,path))
    return out


def _declared_write_errors(contract,paths,business_id,run_id,phase):
    declared=_selector_types(contract.get('writes'))
    if not declared:return []
    candidates=_objects_in_paths(paths,business_id)
    if phase=='root': candidates += _run_bound_objects(business_id,run_id)
    seen={obj.get('object_type') for obj,_ in candidates}
    if declared & seen:return []
    return [f"completion evidence for {contract.get('id')} must include or bind at least one declared canonical write type ({', '.join(sorted(declared))}); observed {', '.join(sorted(x for x in seen if x)) or 'none'}"]


def detector_evidence_errors(contract,paths,business_id,run_id):
    # A detector may legitimately find nothing. A declared write proves a finding; otherwise
    # require a structured no-finding record tied to actual evidence/checks.
    if not _declared_write_errors(contract,paths,business_id,run_id,'root'):return []
    cid=contract.get('id')
    for p in paths:
        d=_json(p)
        if not isinstance(d,dict) or d.get('contract_id')!=cid:continue
        if str(d.get('status','')).lower() not in {'completed','complete','no_finding'}:continue
        if str(d.get('result','')).lower() not in {'no_finding','no_material_finding','no_opportunity','no_material_opportunity'}:continue
        checks=d.get('checks_performed',d.get('checks'))
        refs=d.get('evidence_refs') or []
        if not isinstance(checks,(list,dict)) or not checks or not refs:continue
        if len(_paths(refs))!=len(refs):continue
        return []
    return [f'{cid} detector completion requires either a declared canonical finding or a structured no-finding JSON record with checks_performed and existing evidence_refs']


def _qa_records(contract_id,paths):
    out=[]
    for p in paths:
        data=_json(p)
        if not isinstance(data,dict) or data.get('contract_id')!=contract_id:continue
        if str(data.get('status','')).lower() not in {'pass','passed'}:continue
        checks=data.get('checks_performed',data.get('checks')); blockers=data.get('blockers',None)
        target=next((data.get(k) for k in ('tested_asset','target_asset','asset_ref','target_ref','target_refs') if data.get(k)),None)
        if not isinstance(checks,(list,dict)) or not checks or blockers is None or not target:continue
        out.append((data,p))
    return out


def qa_evidence_errors(contract,paths):
    cid=contract.get('id'); records=_qa_records(cid,paths)
    if not records:return [f'{cid} completion requires a structured JSON QA pass record with matching contract_id, substantive checks_performed/checks, blockers, and tested/target Asset reference']
    if cid=='content.qa.pre-publish' and not any(any(d.get(k) is not None for k in ('tested_version','asset_version','version')) for d,_ in records):
        return ['content.qa.pre-publish completion requires the tested Asset version in its structured pass record']
    return []


def _media_family(medium):
    m=str(medium or '').lower()
    if m in {'image','graphic','thumbnail'}:return 'image'
    if m=='gif':return 'gif'
    if m in {'audio','voiceover'}:return 'audio'
    if m in {'video','avatar-video','demo','clip-extraction'}:return 'video'
    if m=='animation':return 'animation'
    if m in {'presentation','slides','carousel'}:return 'presentation'
    if m=='infographic':return 'infographic'
    return 'text'


def _animation_spec_ok(path):
    if Path(path).suffix.lower() not in TEXT_EXTS:return False
    try:text=Path(path).read_text(encoding='utf-8',errors='ignore').lower()
    except Exception:return False
    return len(text.split())>=80 and all(x in text for x in ('scene','timing','transition')) and ('keyframe' in text or 'narration' in text or 'visual state' in text)


def _text_substance_error(path,medium):
    try:text=Path(path).read_text(encoding='utf-8',errors='ignore')
    except Exception:return f'production artifact is not readable text: {path}'
    words=re.findall(r"\b[\w'-]+\b",text); minimum=TEXT_MIN_WORDS.get(str(medium or '').lower(),40)
    if len(words)<minimum:return f'production artifact is too small for {medium or "text"} completion ({len(words)} words; minimum {minimum})'
    return None


def _asset_lineage_ok(asset,contract,business_id):
    lineage=asset.get('lineage') or []
    if not isinstance(lineage,list) or not lineage:return False
    idx=object_index(business_id); acceptable=_selector_types(contract.get('reads'))-{'Asset'}
    if not acceptable:return bool(lineage)
    for ref in lineage:
        pair=idx.get(ref)
        if pair and pair[0].get('object_type') in acceptable:return True
    return False


def production_evidence_errors(contract,paths,business_id,run_id,manifest=None):
    cid=contract.get('id'); spec=completion_spec(contract); medium=spec.get('medium'); family=_media_family(medium)
    bound=_run_bound_objects(business_id,run_id)
    assets=[obj for obj,_ in bound if obj.get('object_type')=='Asset' and obj.get('owner_system')==contract.get('owner_system')]
    chain_assets=[]
    for asset in assets:
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        chain=bos.get('contract_chain') or []
        if cid in chain or bos.get('run_contract_id')==cid:chain_assets.append(asset)
    if chain_assets:assets=chain_assets
    if not assets:return [f'{cid} production completion requires a canonical Asset bound to this Run']
    supplied={str(p.resolve()) for p in paths}; usable=[]; errors=[]
    for asset in assets:
        loc=asset.get('location_reference')
        if not loc:continue
        p=resolve_storage_ref(loc)
        if not p.exists() or not p.is_file() or p.stat().st_size<200 or str(p.resolve()) not in supplied:continue
        if not _asset_lineage_ok(asset,contract,business_id):
            errors.append(f'{asset.get("id")} lacks canonical lineage to an input type declared by {cid}');continue
        ext=p.suffix.lower()
        if family=='animation':
            if ext in MEDIA_EXTS['video']|MEDIA_EXTS['gif'] or (spec.get('allow_specification_fallback') and _animation_spec_ok(p)):
                usable.append(asset);continue
            errors.append(f'{asset.get("id")} animation evidence must be rendered motion media or a complete scene/keyframe/timing/transition production specification');continue
        if family in MEDIA_EXTS:
            if ext not in MEDIA_EXTS[family]:
                errors.append(f'{asset.get("id")} evidence file type {ext or "<none>"} does not satisfy expected {family} medium for {cid}');continue
            usable.append(asset);continue
        err=_text_substance_error(p,medium)
        if err:errors.append(f'{asset.get("id")}: {err}');continue
        usable.append(asset)
    if not usable:return errors or [f'{cid} has no substantive root artifact matching its canonical Asset and expected medium']

    if manifest:
        byid=contract_index(); produced={a.get('id'):str(a.get('version')) for a in usable if a.get('id')}
        for qid in manifest.get('required_subcontracts') or []:
            qc=byid.get(qid,{})
            if completion_spec(qc).get('profile')!='qa':continue
            refs=((manifest.get('contracts') or {}).get(qid) or {}).get('evidence_refs') or []
            records=_qa_records(qid,_paths(refs)); targeted=False
            for data,_ in records:
                raw=next((data.get(k) for k in ('tested_asset','target_asset','asset_ref','target_ref','target_refs') if data.get(k)),None)
                vals=raw if isinstance(raw,list) else [raw]; vals={str(x) for x in vals if x is not None}
                for aid,ver in produced.items():
                    if aid in vals:
                        if qid=='content.qa.pre-publish':
                            qver=next((data.get(k) for k in ('tested_version','asset_version','version') if data.get(k) is not None),None)
                            if qver is not None and str(qver)!=ver:continue
                        targeted=True;break
                if targeted:break
            if not targeted:errors.append(f'{qid} pass evidence does not target the produced Asset/version for {cid}')
    return errors


def validate_evidence(contract,refs,business_id,run_id,phase='root',manifest=None):
    paths=_paths(refs); errors=[]
    if not paths:return [f'{contract.get("id")} completion requires at least one existing non-empty evidence file']
    spec=completion_spec(contract); profile=spec['profile']
    if profile=='qa':errors.extend(qa_evidence_errors(contract,paths))
    elif profile=='production' and phase=='root':errors.extend(production_evidence_errors(contract,paths,business_id,run_id,manifest))
    elif profile=='detector' and phase=='root':errors.extend(detector_evidence_errors(contract,paths,business_id,run_id))
    elif profile in {'publishing','measurement','research','planning','canonical_state'}:
        if phase=='root' or spec.get('require_subcontract_write_evidence'):
            errors.extend(_declared_write_errors(contract,paths,business_id,run_id,phase))
    return errors


def qa_record_ok(contract_id,refs):
    c=contract_index().get(contract_id,{'id':contract_id})
    return not qa_evidence_errors(c,_paths(refs))
