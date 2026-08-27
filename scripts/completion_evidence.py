#!/usr/bin/env python3
"""Reusable contract-completion evidence profiles for AURA Runs.

The deterministic layer does not judge business quality. It prevents a Run from being
marked complete merely because some arbitrary file exists. Contracts map to a small set
of reusable evidence profiles; qualitative strength remains the responsibility of the
contract process, QA, and downstream qualification/review.
"""
from pathlib import Path
import hashlib, json, re, struct
import xml.etree.ElementTree as ET
from _common import *

CUSTOMER_FACING_ROLE='customer_facing_production_root'
TEXT_EXTS={'.md','.txt','.html','.htm','.rst','.csv','.json'}
MEDIA_EXTS={
    'image':{'.png','.jpg','.jpeg','.webp','.svg'},
    'gif':{'.gif','.webp','.mp4'},
    'audio':{'.mp3','.wav','.m4a','.aac','.ogg','.flac'},
    'video':{'.mp4','.mov','.webm','.m4v'},
    'presentation':{'.pptx','.pdf','.html','.png','.jpg','.jpeg','.webp','.svg'},
    'infographic':{'.png','.jpg','.jpeg','.webp','.svg','.pdf'},
}
PACKET_FALLBACKS={
    'animation':(('scene','timing','transition'),('keyframe','narration','visual state')),
    'short-video':(('visual','duration','audio'),('scene','beat','shot','storyboard')),
    'long-video':(('visual','duration','audio'),('scene','beat','shot','storyboard')),
    'podcast':(('audio','segment','script'),('edit','timing','show notes','talking points')),
    'presentation':(('slide','audience','duration'),('speaker notes','visual','chart','diagram')),
    'carousel':(('slide','sequence','visual'),('cover','frame','platform','dimensions')),
    'demo':(('product','step','state'),('narration','visual','interaction','screen')),
}

# These are medium-family structural floors for graceful-degradation packets. They do
# not score creative quality; they prevent a short keyword shell from impersonating the
# complete audience content and production direction promised by the contract.
PACKET_MIN_WORDS={
    'animation':140,'short-video':120,'long-video':300,'podcast':350,
    'presentation':250,'carousel':180,'demo':180,
}

MIN_MEDIA_BYTES={'image':256,'gif':256,'audio':1024,'video':1024,'presentation':512,'infographic':256}


def _selector_types(items):
    out=set()
    for item in items or []:
        typ=item.get('type') if isinstance(item,dict) else item
        if isinstance(typ,str) and typ.strip(): out.add(typ.strip())
    return out


def contract_index():
    return {c['id']:c for c in load_registry().get('contracts',[]) if c.get('id')}


def completion_spec(contract):
    """Return a stable structural evidence profile for a contract.

    Explicit frontmatter `completion_evidence` overrides inference. Inference gives the
    installed catalog useful minimum safeguards without requiring bespoke validators for
    hundreds of contracts.
    """
    explicit=contract.get('completion_evidence')
    if isinstance(explicit,str): explicit={'profile':explicit}
    explicit=explicit if isinstance(explicit,dict) else {}
    cid=str(contract.get('id','')).lower(); last=cid.split('.')[-1] if cid else ''
    writes=_selector_types(contract.get('writes'));reads=_selector_types(contract.get('reads'))
    if explicit.get('profile'):
        profile=str(explicit['profile'])
    elif '.qa.' in cid or cid.startswith('content.qa.') or cid.endswith('.qa'):
        profile='qa'
    elif contract.get('artifact_role')==CUSTOMER_FACING_ROLE:
        profile='production'
    elif cid.startswith('content.intelligence.') and writes & {'SourceRecord','Observation','Insight','Learning'}:
        profile='intelligence'
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
    default_fallback=medium in PACKET_FALLBACKS
    return {
        'version':'1.0','profile':profile,'medium':medium,
        'declared_write_types':sorted(writes),'artifact_role':contract.get('artifact_role'),
        'allow_specification_fallback':bool(explicit.get('allow_specification_fallback',default_fallback)),
        'allow_shared_subcontract_evidence':bool(explicit.get('allow_shared_subcontract_evidence',False)),
        # A required subcontract that declares canonical writes must leave one of those
        # results as evidence.  A generic status/summary file is not the promised work.
        'require_subcontract_write_evidence':bool(explicit.get('require_subcontract_write_evidence',bool(writes))),
        'required_text_components':explicit.get('required_text_components') or [],
        'strict_qa_target':bool(explicit.get('strict_qa_target', profile=='qa' and 'Asset' in reads)),
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
    seen={obj.get('object_type') for obj,_ in candidates}
    if declared & seen:return []
    return [f"completion evidence for {contract.get('id')} must include or bind at least one declared canonical write type ({', '.join(sorted(declared))}); observed {', '.join(sorted(x for x in seen if x)) or 'none'}"]


def detector_evidence_errors(contract,paths,business_id,run_id):
    if not _declared_write_errors(contract,paths,business_id,run_id,'root'):return []
    cid=contract.get('id')
    for p in paths:
        d=_json(p)
        if not isinstance(d,dict) or d.get('contract_id')!=cid:continue
        if str(d.get('status','')).lower() not in {'completed','complete','no_finding'}:continue
        if str(d.get('result','')).lower() not in {'no_finding','no_material_finding','no_opportunity','no_material_opportunity'}:continue
        checks=d.get('checks_performed',d.get('checks')); refs=d.get('evidence_refs') or []
        if not isinstance(checks,(list,dict)) or not checks or not refs:continue
        if len(_paths(refs))!=len(refs):continue
        return []
    return [f'{cid} detector completion requires either a declared canonical finding or a structured no-finding JSON record with checks_performed and existing evidence_refs']


def _substantive(value,min_words=3):
    if isinstance(value,str):return len(re.findall(r'\b\w+\b',value))>=min_words
    if isinstance(value,list):return bool(value) and any(_substantive(x,min_words) for x in value)
    if isinstance(value,dict):return bool(value) and any(_substantive(x,min_words) for x in value.values())
    return value is not None


def _record_refs(value):
    refs=[]
    if isinstance(value,str):refs.append(value)
    elif isinstance(value,list):
        for x in value:refs.extend(_record_refs(x))
    elif isinstance(value,dict):
        for key in ('ref','source_ref','evidence_ref','source_refs','evidence_refs','asset_ref','observation_ref'):
            if key in value:refs.extend(_record_refs(value[key]))
    return [x for x in refs if isinstance(x,str) and x.strip()]


def _ref_resolves(ref,business_id):
    if ref in object_index(business_id):return True
    try:return resolve_storage_ref(ref).exists()
    except Exception:return False


def intelligence_evidence_errors(contract,paths,business_id,run_id):
    """Require an auditable analysis packet in addition to concise canonical state.

    This validates a small shared Content-intelligence work-record protocol. It does not
    decide whether the interpretation is good; independent review still owns that.
    """
    cid=contract.get('id');records=[]
    for p in paths:
        data=_json(p)
        values=data if isinstance(data,list) else [data]
        for value in values:
            if not isinstance(value,dict):continue
            nested=value.get('analysis_record')
            if isinstance(nested,dict):value=nested
            if value.get('contract_id')==cid and all(k in value for k in ('analysis_scope','method','evidence_sample','comparisons','findings','limitations','recommended_actions')):
                records.append(value)
    if not records:
        return [f'{cid} completion requires a Run-local JSON intelligence work record with analysis_scope, method, evidence_sample, comparisons, findings, limitations, and recommended_actions; a concise canonical conclusion alone is not the analysis']
    all_failures=[]
    for record in records:
        failures=[]
        status=str(record.get('status','completed')).lower()
        if status not in {'completed','complete','no_finding'}:
            all_failures.append('status must be completed or no_finding');continue
        for key in ('analysis_scope','method','comparisons','limitations','recommended_actions'):
            if not _substantive(record.get(key)):
                failures.append(f'{key} is empty or non-substantive')
        sample=record.get('evidence_sample')
        if not isinstance(sample,list) or not sample:
            failures.append('evidence_sample must contain inspected item-level evidence')
        else:
            refs=_record_refs(sample)
            if not refs or not any(_ref_resolves(ref,business_id) for ref in refs):
                failures.append('evidence_sample must include at least one reconstructable canonical or local evidence reference')
            if not all(_substantive(item) for item in sample):
                failures.append('evidence_sample items must contain substantive item-level observations')
        findings=record.get('findings')
        if not isinstance(findings,list):failures.append('findings must be a list')
        elif status!='no_finding' and not findings:failures.append('completed analysis must contain at least one finding')
        else:
            for i,finding in enumerate(findings):
                if not isinstance(finding,dict) or not _substantive(finding.get('statement')):
                    failures.append(f'finding {i+1} lacks a substantive statement');continue
                if not _substantive(finding.get('mechanism')):failures.append(f'finding {i+1} lacks mechanism analysis')
                if not _record_refs(finding.get('evidence_refs')):failures.append(f'finding {i+1} lacks evidence_refs')
                if not _substantive(finding.get('alternative_explanations')):failures.append(f'finding {i+1} lacks alternative explanations')
        if not failures:return []
        all_failures.extend(failures)
    return [f'{cid} intelligence work record is incomplete: ' + '; '.join(dict.fromkeys(all_failures))]


def _structured_check(item,require_method_evidence=False):
    if not isinstance(item,dict):return False
    label=next((item.get(k) for k in ('check','name','criterion','test') if item.get(k)),None)
    outcome=next((item.get(k) for k in ('status','result','outcome','passed') if item.get(k) is not None),None)
    if not label or outcome is None:return False
    normalized_label=re.sub(r'[^a-z0-9]+',' ',str(label).lower()).strip()
    if normalized_label in {'check','qa','quality assurance','quality check','compliance','compliance validation','validation','review'}:return False
    detail=next((item.get(k) for k in ('result','outcome','evidence','finding','correction','notes') if item.get(k) not in (None,'')),None)
    if detail is None:return False
    normalized=re.sub(r'\s+',' ',str(detail).lower()).strip()
    if re.search(r'\b(?:content|marketing|seo|customer|competitor|industry)\.[a-z0-9_.-]+\b',normalized):return False
    if re.fullmatch(r'(?:verified|confirmed|validated|checked|passed) (?:full )?(?:compliance|quality assurance|all criteria|all checks|all requirements)(?: for .+)?\.?',normalized):return False
    if re.fullmatch(r'(?:quality assurance|compliance(?: validation)?) (?:has )?passed(?: all criteria)?(?: for .+)?\.?',normalized):return False
    if re.fullmatch(r'(?:passed|pass(?:ed)? all)(?: the)? required (?:quality )?checks?(?: for .+)?\.?',normalized):return False
    if re.fullmatch(r'all .{0,100}(?:verified|checked|validated)(?: successfully)?\.?',normalized):return False
    if re.fullmatch(r'.{0,100}(?:requirements?|standards?|rules?) (?:were )?(?:met|passed|verified|satisfied)(?: successfully)?\.?',normalized):return False
    if len(re.findall(r'\b\w+\b',normalized))<3:return False
    if require_method_evidence:
        method=next((item.get(k) for k in ('method','procedure','tool','inspection') if item.get(k) not in (None,'')),None)
        finding=next((item.get(k) for k in ('finding','evidence','observed','actual','result') if item.get(k) not in (None,'')),None)
        if not _substantive(method) or not _substantive(finding):return False
        normalized_outcome=str(outcome).lower().strip()
        passed=outcome is True or normalized_outcome in {'pass','passed','true','ok','not_applicable','not applicable','n/a'}
        if not passed:return False
        if normalized_outcome in {'not_applicable','not applicable','n/a'} and not _substantive(item.get('reason')):return False
    return True


def _structured_checks(checks,require_method_evidence=False):
    if isinstance(checks,list):return bool(checks) and all(_structured_check(x,require_method_evidence) for x in checks)
    if isinstance(checks,dict):
        return bool(checks) and all(
            _structured_check(v,require_method_evidence) if isinstance(v,dict) else (not require_method_evidence and isinstance(v,(bool,int,float)))
            for v in checks.values()
        )
    return False


def _qa_target_valid(data,paths,business_id,run_id,contract_id):
    """A strict QA target is an existing Asset/version other than the QA wrapper itself."""
    if not business_id:return False
    raw=next((data.get(k) for k in ('tested_asset','target_asset','asset_ref','target_ref','target_refs') if data.get(k)),None)
    values=raw if isinstance(raw,list) else [raw]
    version=next((data.get(k) for k in ('tested_version','asset_version','version') if data.get(k) is not None),None)
    if version is None:return False
    idx=object_index(business_id);evidence_paths={str(Path(p).resolve()) for p in paths}
    for value in values:
        if not isinstance(value,str) or value not in idx:continue
        asset,asset_path=idx[value]
        if asset.get('object_type')!='Asset' or str(asset.get('version'))!=str(version):continue
        loc=asset.get('location_reference')
        if loc:
            try:
                if str(resolve_storage_ref(loc).resolve()) in evidence_paths:continue
            except Exception:continue
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        if run_id and bos.get('run_id')==run_id and bos.get('run_contract_id')==contract_id:continue
        return True
    return False


def _qa_records(contract_id,paths,strict_target=False,business_id=None,run_id=None):
    out=[]
    for p in paths:
        data=_json(p)
        if not isinstance(data,dict) or data.get('contract_id')!=contract_id:continue
        if str(data.get('status','')).lower() not in {'pass','passed'}:continue
        checks=data.get('checks_performed',data.get('checks'))
        if not _structured_checks(checks,require_method_evidence=strict_target):continue
        if strict_target:
            blockers=data.get('blockers',None)
            if not isinstance(blockers,list) or blockers:continue
            if any(not isinstance(data.get(key),list) for key in ('issues_found','corrections_made','limitations')):continue
            if not _qa_target_valid(data,paths,business_id,run_id,contract_id):continue
        out.append((data,p))
    return out


def qa_evidence_errors(contract,paths,business_id=None,run_id=None):
    cid=contract.get('id'); spec=completion_spec(contract); strict=spec.get('strict_qa_target',False)
    records=_qa_records(cid,paths,strict_target=strict,business_id=business_id,run_id=run_id)
    if not records:
        if strict:return [f'{cid} completion requires a structured JSON QA pass record with matching contract_id, substantive per-check outcomes, no unresolved blockers, and an existing non-self target Asset at the exact tested version']
        return [f'{cid} completion requires a structured JSON QA pass record with matching contract_id and structured per-check outcomes']
    return []


def _media_family(medium):
    m=str(medium or '').lower()
    if m in {'image','graphic','thumbnail'}:return 'image'
    if m=='gif':return 'gif'
    if m in {'audio','voiceover'}:return 'audio'
    if m in {'video','avatar-video','short-video','long-video','clip-extraction'}:return 'video'
    if m=='demo':return 'video'
    if m=='animation':return 'animation'
    if m in {'presentation','slides','carousel'}:return 'presentation'
    if m=='infographic':return 'infographic'
    if m=='podcast':return 'audio'
    return 'text'


def _text(path):
    try:return Path(path).read_text(encoding='utf-8',errors='ignore')
    except Exception:return ''


def _required_text_component_errors(contract,paths):
    """Verify contract-authored, machine-checkable components without special-casing IDs."""
    components=completion_spec(contract).get('required_text_components') or []
    if not components:return []
    text='\n'.join(_text(p) for p in paths if Path(p).suffix.lower() in TEXT_EXTS|{'.svg'}).lower()
    errors=[]
    for raw in components:
        if isinstance(raw,str):
            label=raw;any_of=[raw];all_of=[]
        elif isinstance(raw,dict):
            label=str(raw.get('id') or raw.get('label') or raw.get('name') or 'unnamed component')
            any_of=raw.get('any_of') or raw.get('terms') or []
            all_of=raw.get('all_of') or []
            if isinstance(any_of,str):any_of=[any_of]
            if isinstance(all_of,str):all_of=[all_of]
        else:
            errors.append(f'{contract.get("id")} has invalid required_text_components metadata: {raw!r}');continue
        any_terms=[str(x).strip().lower() for x in any_of if str(x).strip()]
        all_terms=[str(x).strip().lower() for x in all_of if str(x).strip()]
        if not any_terms and not all_terms:
            errors.append(f'{contract.get("id")} required component {label!r} has no match terms');continue
        if any_terms and not any(term in text for term in any_terms):
            errors.append(f'{contract.get("id")} evidence is missing required component {label!r} (expected one of: {", ".join(any_terms)})')
        missing=[term for term in all_terms if term not in text]
        if missing:
            errors.append(f'{contract.get("id")} evidence is missing required component {label!r} terms: {", ".join(missing)}')
    return errors


def _contains_internal_completion_markers(path,contract_id):
    if Path(path).suffix.lower() not in TEXT_EXTS|{'.svg'}:return False
    text=_text(path).lower()
    cid=str(contract_id or '').lower()
    if cid and cid in text:return True
    return bool(re.search(r'\bcontract-[a-z0-9-]{8,}\b|\baura_qualification_run\b|\bqualification event\b',text))


def _png_dimensions(data):
    if len(data)>=24 and data[:8]==b'\x89PNG\r\n\x1a\n':return struct.unpack('>II',data[16:24])
    return None


def _gif_dimensions(data):
    if len(data)>=10 and data[:6] in {b'GIF87a',b'GIF89a'}:return struct.unpack('<HH',data[6:10])
    return None


def _jpeg_dimensions(data):
    if not data.startswith(b'\xff\xd8'):return None
    i=2
    while i+9<len(data):
        if data[i]!=0xff:i+=1;continue
        marker=data[i+1];i+=2
        if marker in {0xd8,0xd9} or 0xd0<=marker<=0xd7:continue
        if i+2>len(data):break
        n=int.from_bytes(data[i:i+2],'big')
        if n<2 or i+n>len(data):break
        if marker in {0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf} and n>=7:
            return int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big')
        i+=n
    return None


def _svg_dimensions(path):
    try:root=ET.parse(path).getroot()
    except Exception:return None
    def number(v):
        m=re.match(r'\s*([0-9]+(?:\.[0-9]+)?)',str(v or ''))
        return float(m.group(1)) if m else None
    w=number(root.get('width'));h=number(root.get('height'))
    if (not w or not h) and root.get('viewBox'):
        try:_,_,w,h=[float(x) for x in re.split(r'[ ,]+',root.get('viewBox').strip())]
        except Exception:return None
    return (w,h) if w and h else None


def _media_integrity_errors(path,family,contract_id):
    p=Path(path);ext=p.suffix.lower();data=p.read_bytes();errors=[]
    if len(data)<MIN_MEDIA_BYTES.get(family,1):return [f'{p.name} is too small to be a usable {family} artifact']
    if _contains_internal_completion_markers(p,contract_id):
        errors.append(f'{p.name} exposes internal contract/qualification identifiers instead of the promised audience-facing artifact')
    if ext=='.svg':
        dims=_svg_dimensions(p)
        if not dims or dims[0]<64 or dims[1]<64:errors.append(f'{p.name} is not a valid usable-size SVG')
    elif ext=='.png':
        dims=_png_dimensions(data)
        if not dims or dims[0]<64 or dims[1]<64:errors.append(f'{p.name} is not a valid usable-size PNG')
    elif ext in {'.jpg','.jpeg'}:
        dims=_jpeg_dimensions(data)
        if not dims or dims[0]<64 or dims[1]<64:errors.append(f'{p.name} is not a valid usable-size JPEG')
    elif ext=='.gif':
        dims=_gif_dimensions(data);frames=data.count(b'\x2c')
        if not dims or dims[0]<64 or dims[1]<64 or frames<2:errors.append(f'{p.name} must be a valid animated GIF with usable dimensions and multiple frames')
    elif ext in {'.mp4','.mov','.m4v'}:
        if not all(atom in data for atom in (b'ftyp',b'moov',b'mdat')):errors.append(f'{p.name} is not a structurally decodable MP4/MOV artifact')
    elif ext=='.webm':
        if not data.startswith(b'\x1a\x45\xdf\xa3'):errors.append(f'{p.name} is not a structurally valid WebM artifact')
    elif ext=='.wav':
        if not (data.startswith(b'RIFF') and data[8:12]==b'WAVE'):errors.append(f'{p.name} is not a structurally valid WAV artifact')
    elif ext=='.flac':
        if not data.startswith(b'fLaC'):errors.append(f'{p.name} is not a structurally valid FLAC artifact')
    elif ext=='.ogg':
        if not data.startswith(b'OggS'):errors.append(f'{p.name} is not a structurally valid OGG artifact')
    elif ext=='.mp3':
        if not any(data[i]==0xff and data[i+1]&0xe0==0xe0 for i in range(max(0,len(data)-1))):errors.append(f'{p.name} contains no MPEG audio frames')
    return errors


def _packet_fallback_ok(path,medium,contract_id=None):
    m=str(medium or '').lower();rules=PACKET_FALLBACKS.get(m)
    if not rules or Path(path).suffix.lower() not in TEXT_EXTS:return False
    if _contains_internal_completion_markers(path,contract_id):return False
    text=_text(path).lower()
    if len(re.findall(r'\b\w+\b',text))<PACKET_MIN_WORDS.get(m,100):return False
    required,alternatives=rules
    if not (all(x in text for x in required) and any(x in text for x in alternatives)):return False
    if m=='podcast':
        units=max(
            len(re.findall(r'(?im)^\s*#{1,6}\s+(?:segment|part|act|chapter|cold open|introduction|intro|close|conclusion)\b',text)),
            len(re.findall(r'(?im)^\s*(?:segment|part|act|chapter)\s*(?:\d+|[a-z])\b',text)),
            len(re.findall(r'\b\d{1,2}:\d{2}\b',text)),
        )
        required_groups=(
            ('listener promise','episode promise','audience'),
            ('call to action','cta','next step'),
            ('show notes','episode notes'),
            ('source notes','research notes','evidence notes','references'),
        )
        if units<3 or any(not any(term in text for term in group) for group in required_groups):return False
    elif m=='presentation':
        slides=max(
            len(re.findall(r'(?im)^\s*#{1,6}\s+slide\s+\d+\b',text)),
            len(re.findall(r'(?im)^\s*slide\s+\d+\s*[:.-]',text)),
            len(re.findall(r'"slide_(?:number|id)"\s*:',text)),
        )
        notes=len(re.findall(r'\b(?:speaker notes?|presenter notes?|narration)\b',text))
        required_groups=(
            ('audience','attendees','viewer'),
            ('objective','decision','learning outcome'),
            ('source','proof','evidence','attribution'),
            ('call to action','cta','next step','decision close'),
        )
        if slides<5 or notes<2 or any(not any(term in text for term in group) for group in required_groups):return False
    return True


def _asset_lineage_ok(asset,business_id):
    lineage=asset.get('lineage') or []
    if not isinstance(lineage,list) or not lineage:return False
    idx=object_index(business_id)
    return any(ref in idx for ref in lineage)


def production_evidence_errors(contract,paths,business_id,run_id,manifest=None):
    cid=contract.get('id');spec=completion_spec(contract);medium=spec.get('medium');family=_media_family(medium)
    bound=_run_bound_objects(business_id,run_id)
    assets=[obj for obj,_ in bound if obj.get('object_type')=='Asset' and obj.get('owner_system')==contract.get('owner_system')]
    chain_assets=[]
    for asset in assets:
        bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
        chain=bos.get('contract_chain') or []
        if cid in chain or bos.get('run_contract_id')==cid:chain_assets.append(asset)
    if chain_assets:assets=chain_assets
    if not assets:return [f'{cid} production completion requires a canonical Asset bound to this Run']
    supplied={str(p.resolve()) for p in paths};usable=[];errors=[]
    for asset in assets:
        loc=asset.get('location_reference')
        if not loc:continue
        p=resolve_storage_ref(loc)
        if not p.exists() or not p.is_file() or p.stat().st_size<=0 or str(p.resolve()) not in supplied:continue
        if not _asset_lineage_ok(asset,business_id):
            errors.append(f'{asset.get("id")} lacks lineage to existing canonical business state');continue
        ext=p.suffix.lower()
        if family in MEDIA_EXTS or family=='animation':
            accepted_exts=(MEDIA_EXTS['video']|MEDIA_EXTS['gif']) if family=='animation' else MEDIA_EXTS[family]
            if ext in accepted_exts:
                media_errors=_media_integrity_errors(p,family,cid)
                if not media_errors:usable.append(asset)
                else:errors.extend(f'{asset.get("id")}: {x}' for x in media_errors)
                continue
            if spec.get('allow_specification_fallback') and _packet_fallback_ok(p,medium,cid):
                usable.append(asset);continue
            fallback=' or a complete production packet/specification' if spec.get('allow_specification_fallback') else ''
            errors.append(f'{asset.get("id")} evidence file type {ext or "<none>"} does not satisfy expected {family} medium for {cid}{fallback}');continue
        if ext not in TEXT_EXTS:
            errors.append(f'{asset.get("id")} evidence file type {ext or "<none>"} does not satisfy expected text/document medium for {cid}');continue
        if _contains_internal_completion_markers(p,cid):
            errors.append(f'{asset.get("id")} root artifact exposes internal contract/qualification identifiers instead of the promised audience-facing result');continue
        usable.append(asset)
    if not usable:return errors or [f'{cid} has no root artifact matching its canonical Asset and expected medium']

    if manifest:
        byid=contract_index();produced={a.get('id'):str(a.get('version')) for a in usable if a.get('id')}
        for qid in manifest.get('required_subcontracts') or []:
            qc=byid.get(qid,{});qspec=completion_spec(qc)
            if qspec.get('profile')!='qa':continue
            refs=((manifest.get('contracts') or {}).get(qid) or {}).get('evidence_refs') or []
            records=_qa_records(qid,_paths(refs),strict_target=True,business_id=business_id,run_id=run_id);targeted=False
            for data,_ in records:
                raw=next((data.get(k) for k in ('tested_asset','target_asset','asset_ref','target_ref','target_refs') if data.get(k)),None)
                vals=raw if isinstance(raw,list) else [raw];vals={str(x) for x in vals if x is not None}
                qver=next((data.get(k) for k in ('tested_version','asset_version','version') if data.get(k) is not None),None)
                for aid,ver in produced.items():
                    if aid in vals and qver is not None and str(qver)==ver:
                        targeted=True;break
                if targeted:break
            if not targeted:errors.append(f'{qid} pass evidence does not target the produced Asset/version for {cid}')
    return errors


def _ref_signatures(refs):
    paths=_paths(refs)
    locs=tuple(sorted(str(p.resolve()) for p in paths))
    hashes=[]
    for p in paths:
        try:hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
        except Exception:continue
    return locs,tuple(sorted(hashes))


def subcontract_evidence_reuse_errors(manifest,contracts=None):
    """Reject distinct required jobs that merely cite the same evidence package.

    One integrated artifact may be shared only when every involved contract explicitly
    opts in and declares machine-checkable component requirements. That keeps reuse a
    contract-authored decision instead of an agent-selected completion shortcut.
    """
    contracts=contracts or contract_index();steps=manifest.get('contracts') or {}
    entries=[]
    for cid in manifest.get('required_subcontracts') or []:
        step=steps.get(cid) or {}
        if step.get('status')!='completed' or not step.get('evidence_refs'):continue
        locs,hashes=_ref_signatures(step.get('evidence_refs') or [])
        if locs:entries.append((cid,locs,hashes))
    groups=[];seen=set()
    for signature_index,kind in ((1,'same evidence reference set'),(2,'byte-identical evidence package')):
        bysig={}
        for entry in entries:bysig.setdefault(entry[signature_index],[]).append(entry[0])
        for sig,cids in bysig.items():
            unique=sorted(set(cids))
            if len(unique)<2:continue
            key=tuple(unique)
            if key in seen:continue
            seen.add(key);groups.append((kind,unique))
    errors=[]
    for kind,cids in groups:
        specs=[completion_spec(contracts.get(cid,{'id':cid})) for cid in cids]
        authored_share=all(s.get('allow_shared_subcontract_evidence') and s.get('required_text_components') for s in specs)
        if not authored_share:
            errors.append(
                f'distinct required subcontracts reuse the {kind} without contract-authored shared-evidence component rules: {", ".join(cids)}'
            )
    return errors


def subcontract_manifest_errors(manifest,business_id,run_id,contracts=None,require_complete=True):
    """Independently validate every declared required subcontract and evidence package."""
    contracts=contracts or contract_index();steps=manifest.get('contracts') or {};errors=[]
    for cid in manifest.get('required_subcontracts') or []:
        step=steps.get(cid) or {}
        if require_complete and step.get('status')!='completed':
            errors.append(f'{cid}: required subcontract is not completed');continue
        refs=step.get('evidence_refs') or []
        if require_complete and not refs:
            errors.append(f'{cid}: completed subcontract lacks evidence refs');continue
        if not refs:continue
        contract=contracts.get(cid)
        if not contract:
            errors.append(f'{cid}: contract missing from installed registry');continue
        errors.extend(f'{cid}: {x}' for x in validate_evidence(contract,refs,business_id,run_id,phase='subcontract',manifest=manifest))
    errors.extend(subcontract_evidence_reuse_errors(manifest,contracts))
    return errors


def validate_evidence(contract,refs,business_id,run_id,phase='root',manifest=None):
    paths=_paths(refs);errors=[]
    if not paths:return [f'{contract.get("id")} completion requires at least one existing non-empty evidence file']
    spec=completion_spec(contract);profile=spec['profile']
    if profile=='qa':errors.extend(qa_evidence_errors(contract,paths,business_id,run_id))
    elif profile=='production' and phase=='root':errors.extend(production_evidence_errors(contract,paths,business_id,run_id,manifest))
    elif profile=='intelligence':
        if phase=='root' or spec.get('require_subcontract_write_evidence'):
            errors.extend(_declared_write_errors(contract,paths,business_id,run_id,phase))
        errors.extend(intelligence_evidence_errors(contract,paths,business_id,run_id))
    elif profile=='detector' and phase=='root':errors.extend(detector_evidence_errors(contract,paths,business_id,run_id))
    elif profile in {'publishing','measurement','research','planning','canonical_state'}:
        if phase=='root' or spec.get('require_subcontract_write_evidence'):
            errors.extend(_declared_write_errors(contract,paths,business_id,run_id,phase))
    errors.extend(_required_text_component_errors(contract,paths))
    return errors


def qa_record_ok(contract_id,refs,business_id=None,run_id=None):
    c=contract_index().get(contract_id,{'id':contract_id})
    return not qa_evidence_errors(c,_paths(refs),business_id,run_id)
