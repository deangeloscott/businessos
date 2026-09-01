#!/usr/bin/env python3
"""Reusable structural evidence checks for AURA work.

This module verifies that supplied artifacts/evidence have a credible shape for the job.
It has no Run, receipt, contract-execution, subcontract-ledger, or execution-plan semantics.
Passing these checks is a structural floor, not a professional-quality score.
"""
from pathlib import Path
import json,re,struct,zipfile
import xml.etree.ElementTree as ET

from _common import *
from artifact_readiness import qa_global_readiness_errors

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
SPEC_FALLBACKS={
    'animation':(('scene','timing','transition'),('keyframe','narration','visual state')),
    'short-video':(('visual','duration','audio'),('scene','beat','shot','storyboard')),
    'long-video':(('visual','duration','audio'),('scene','beat','shot','storyboard')),
    'podcast':(('audio','segment','script'),('edit','timing','show notes','talking points')),
    'presentation':(('slide','audience'),('speaker notes','visual','chart','diagram')),
    'carousel':(('slide','sequence','visual'),('cover','frame','platform','dimensions')),
    'demo':(('product','step','state'),('narration','visual','interaction','screen')),
}
MIN_MEDIA_BYTES={'image':256,'gif':256,'audio':1024,'video':1024,'presentation':512,'infographic':256}


def _selector_types(items):
    out=set()
    for item in items or []:
        typ=item.get('type') if isinstance(item,dict) else item
        if isinstance(typ,str) and typ.strip():out.add(typ.strip())
    return out


def contract_index():
    """Read authored playbook source directly; generated registries are derived views."""
    out={}
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        cid=meta.get('id')
        if isinstance(cid,str) and cid:out[cid]=meta
    return out


def completion_spec(contract):
    """Return a small structural verification profile, never an execution policy."""
    explicit=contract.get('completion_evidence')
    if isinstance(explicit,str):explicit={'profile':explicit}
    explicit=explicit if isinstance(explicit,dict) else {}
    cid=str(contract.get('id','')).lower();last=cid.split('.')[-1] if cid else ''
    writes=_selector_types(contract.get('writes'));reads=_selector_types(contract.get('reads'))
    if explicit.get('profile'):profile=str(explicit['profile'])
    elif '.qa.' in cid or cid.startswith('content.qa.') or cid.endswith('.qa'):profile='qa'
    elif contract.get('artifact_role')==CUSTOMER_FACING_ROLE:profile='production'
    elif '.intelligence.' in cid and writes & {'SourceRecord','Observation','Insight','Learning'}:profile='intelligence'
    elif contract.get('type')=='detector':profile='detector'
    elif '.publishing.' in cid or last in {'publish','publish-asset','schedule','distribution'}:profile='publishing'
    elif '.measurement.' in cid or writes & {'OutcomeEvaluation','MetricObservation'}:profile='measurement'
    elif '.research.' in cid or 'SourceRecord' in writes:profile='research'
    elif '.strategy.' in cid or any(part in cid for part in ('.email.','.landing-page.','.webinar.','.ads.')) or last.endswith(('plan','brief')):profile='planning'
    elif writes:profile='canonical_state'
    else:profile='generic'
    medium=explicit.get('medium') or (last if profile=='production' else None)
    return {
        'profile':profile,
        'medium':medium,
        'declared_write_types':sorted(writes),
        'artifact_role':contract.get('artifact_role'),
        'allow_specification_fallback':bool(explicit.get('allow_specification_fallback',medium in SPEC_FALLBACKS)),
        'require_root_write_evidence':bool(explicit.get('require_root_write_evidence',profile in {'intelligence','publishing','measurement','research','canonical_state'} and bool(writes))),
        # Retained as a negative invariant for authored metadata/tests: structural evidence
        # never requires one synthetic durable object per composed playbook component.
        'require_subcontract_write_evidence':False,
        'strict_qa_target':bool(explicit.get('strict_qa_target',profile=='qa' and 'Asset' in reads)),
    }


def _paths(refs):
    out=[]
    for ref in refs or []:
        try:p=resolve_storage_ref(ref)
        except Exception:continue
        if p.exists() and p.is_file() and p.stat().st_size>0:out.append(p)
    return out


def _json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return None

def _text(path):
    try:return Path(path).read_text(encoding='utf-8',errors='ignore')
    except Exception:return ''

def _substantive(value,min_words=3):
    if isinstance(value,str):return len(re.findall(r'\b\w+\b',value))>=min_words
    if isinstance(value,list):return bool(value) and any(_substantive(x,min_words) for x in value)
    if isinstance(value,dict):return bool(value) and any(_substantive(x,min_words) for x in value.values())
    return value is not None


def _objects_in_paths(paths,business_id=None):
    out=[]
    for path in paths:
        data=_json(path);values=data if isinstance(data,list) else [data]
        for obj in values:
            if not isinstance(obj,dict) or not obj.get('object_type'):continue
            if business_id and obj.get('business_id')!=business_id:continue
            out.append((obj,path))
    return out


def _record_refs(value):
    refs=[]
    if isinstance(value,str):refs.append(value)
    elif isinstance(value,list):
        for item in value:refs.extend(_record_refs(item))
    elif isinstance(value,dict):
        for key in ('ref','source_ref','evidence_ref','source_refs','evidence_refs','asset_ref','observation_ref'):
            if key in value:refs.extend(_record_refs(value[key]))
    return [x for x in refs if isinstance(x,str) and x.strip()]


def _ref_resolves(ref,business_id):
    if business_id and ref in object_index(business_id):return True
    try:return resolve_storage_ref(ref).exists()
    except Exception:return False


def _ref_payload_text(ref,business_id):
    idx=object_index(business_id) if business_id else {}
    if ref in idx:
        obj,_=idx[ref];parts=[]
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
        evidence=ext.get('businessos_evidence') if isinstance(ext.get('businessos_evidence'),dict) else {}
        for value in (evidence.get('captured_text'),ext.get('verbatim_user_statement')):
            if isinstance(value,str):parts.append(value)
        if evidence.get('record_payload') is not None:parts.append(json.dumps(evidence['record_payload'],sort_keys=True,ensure_ascii=False))
        for raw in (obj.get('location_reference'),obj.get('source_reference')):
            if not isinstance(raw,str):continue
            try:
                p=resolve_storage_ref(raw)
                if p.exists() and p.is_file() and p.suffix.lower() in TEXT_EXTS:parts.append(_text(p))
            except Exception:pass
        return '\n'.join(parts)
    try:
        p=resolve_storage_ref(ref);return _text(p) if p.exists() and p.is_file() else ''
    except Exception:return ''


def _literal_support_ok(item,business_id):
    if not isinstance(item,dict):return False
    excerpt=next((item.get(key) for key in ('support_excerpt','source_excerpt','captured_excerpt') if item.get(key)),None)
    refs=_record_refs(item)
    if not isinstance(excerpt,str) or len(re.findall(r'\b\w+\b',excerpt))<3 or not refs:return False
    needle=re.sub(r'\s+',' ',excerpt).strip().lower()
    return any(needle in re.sub(r'\s+',' ',_ref_payload_text(ref,business_id)).lower() for ref in refs)


def _declared_write_errors(contract,paths,business_id):
    declared=_selector_types(contract.get('writes'));seen={obj.get('object_type') for obj,_ in _objects_in_paths(paths,business_id)}
    if not declared or declared & seen:return []
    return [f"evidence for {contract.get('id')} must include at least one declared canonical write type ({', '.join(sorted(declared))}); observed {', '.join(sorted(x for x in seen if x)) or 'none'}"]


def detector_evidence_errors(contract,paths,business_id):
    if not _declared_write_errors(contract,paths,business_id):return []
    cid=contract.get('id')
    for path in paths:
        data=_json(path)
        if not isinstance(data,dict) or data.get('contract_id')!=cid:continue
        if str(data.get('status','')).lower() not in {'completed','complete','no_finding'}:continue
        if str(data.get('result','')).lower() not in {'no_finding','no_material_finding','no_opportunity','no_material_opportunity'}:continue
        checks=data.get('checks_performed',data.get('checks'));refs=data.get('evidence_refs') or []
        if isinstance(checks,(list,dict)) and checks and refs and len(_paths(refs))==len(refs):return []
    return [f'{cid} detector evidence requires either a declared canonical finding or a structured no-finding JSON record with checks_performed and existing evidence_refs']


def intelligence_evidence_errors(contract,paths,business_id):
    cid=contract.get('id');records=[];required=('method','evidence_sample','findings','limitations','recommended_actions')
    for path in paths:
        data=_json(path);values=data if isinstance(data,list) else [data]
        for value in values:
            if not isinstance(value,dict):continue
            if isinstance(value.get('analysis_record'),dict):value=value['analysis_record']
            if value.get('contract_id')==cid and all(key in value for key in required):records.append(value)
    if not records:return [f'{cid} requires an auditable intelligence work record with method, evidence_sample, findings, limitations, and recommended_actions; a concise canonical conclusion alone is not the work record']
    failures=[]
    for record in records:
        current=[];status=str(record.get('status','completed')).lower()
        if status not in {'completed','complete','no_finding'}:current.append('status must be completed or no_finding')
        for key in ('method','limitations','recommended_actions'):
            if not _substantive(record.get(key)):current.append(f'{key} is empty or non-substantive')
        sample=record.get('evidence_sample')
        if not isinstance(sample,list) or not sample:current.append('evidence_sample must contain inspected item-level evidence')
        else:
            refs=_record_refs(sample);unresolved=sorted(set(ref for ref in refs if not _ref_resolves(ref,business_id)))
            if not refs or unresolved:current.append('unresolved evidence_sample references'+(f': {", ".join(unresolved)}' if unresolved else ''))
            if not all(_substantive(item) for item in sample):current.append('evidence_sample items must contain substantive observations')
            if not all(_literal_support_ok(item,business_id) for item in sample):current.append('each evidence_sample item requires a literal support_excerpt present in its referenced captured evidence')
        findings=record.get('findings')
        if not isinstance(findings,list):current.append('findings must be a list')
        elif status!='no_finding' and not findings:current.append('completed analysis must contain at least one finding')
        else:
            for i,finding in enumerate(findings):
                if not isinstance(finding,dict) or not _substantive(finding.get('statement')):current.append(f'finding {i+1} lacks a substantive statement');continue
                if not _substantive(finding.get('mechanism')):current.append(f'finding {i+1} lacks mechanism analysis')
                refs=_record_refs(finding.get('evidence_refs'));unresolved=sorted(set(ref for ref in refs if not _ref_resolves(ref,business_id)))
                if not refs:current.append(f'finding {i+1} lacks evidence_refs')
                elif unresolved:current.append(f'finding {i+1} has unresolved evidence_refs: {", ".join(unresolved)}')
        if not current:return []
        failures.extend(current)
    return [f'{cid} intelligence work record is incomplete: '+'; '.join(dict.fromkeys(failures))]


def _asset_index(business_id):
    if not business_id:return {}
    return {obj.get('id'):(obj,path) for obj,path in iter_instance_objects(business_id) if obj.get('object_type')=='Asset' and obj.get('id')}


def _qa_target(data,qa_record_path,business_id):
    raw=next((data.get(key) for key in ('tested_asset','target_asset','asset_ref','target_ref') if data.get(key)),None)
    version=next((data.get(key) for key in ('tested_version','asset_version','version') if data.get(key) is not None),None)
    if not isinstance(raw,str) or version is None:return None
    item=_asset_index(business_id).get(raw)
    if not item:return None
    asset,asset_path=item
    if str(asset.get('version'))!=str(version):return None
    try:record_path=Path(qa_record_path).resolve()
    except Exception:record_path=None
    if record_path and Path(asset_path).resolve()==record_path:return None
    loc=asset.get('location_reference')
    if isinstance(loc,str):
        try:
            if record_path and resolve_storage_ref(loc).resolve()==record_path:return None
        except Exception:pass
    return asset


def _qa_target_text(asset):
    if not isinstance(asset,dict):return ''
    loc=asset.get('location_reference')
    if not isinstance(loc,str):return ''
    try:
        p=resolve_storage_ref(loc);return _text(p) if p.exists() and p.is_file() and p.suffix.lower() in TEXT_EXTS|{'.svg'} else ''
    except Exception:return ''


def _qa_check_ok(item,target_text,business_id):
    if not isinstance(item,dict):return False
    label=next((item.get(key) for key in ('check','name','criterion','test') if item.get(key)),None)
    outcome=next((item.get(key) for key in ('status','outcome','passed') if item.get(key) is not None),None)
    method=next((item.get(key) for key in ('method','procedure','tool','inspection') if item.get(key) not in (None,'')),None)
    finding=next((item.get(key) for key in ('finding','evidence','observed','actual','result') if item.get(key) not in (None,'')),None)
    if not label or outcome is None or not _substantive(method) or not _substantive(finding):return False
    if re.sub(r'[^a-z0-9]+',' ',str(label).lower()).strip() in {'check','qa','quality assurance','quality check','compliance','compliance validation','validation','review'}:return False
    normalized=str(outcome).lower().strip();passed=outcome is True or normalized in {'pass','passed','true','ok','not_applicable','not applicable','n/a'}
    if not passed:return False
    if normalized in {'not_applicable','not applicable','n/a'}:return _substantive(item.get('reason')) and _substantive(item.get('target_component'))
    if re.search(r'\b(?:automat(?:ed|ic)|scanner|linter|validator|flesch(?:-kincaid)?|contrast ratio|axe|lighthouse)\b',str(method),re.I):
        ref=next((item.get(key) for key in ('tool_output_ref','automation_evidence_ref','scan_output_ref') if item.get(key)),None)
        if not ref or not _ref_resolves(ref,business_id):return False
    excerpt=item.get('target_excerpt');component=item.get('target_component')
    if isinstance(excerpt,str) and len(re.findall(r'\b\w+\b',excerpt))>=2:
        if not target_text:return False
        if re.sub(r'\s+',' ',excerpt).strip().lower() not in re.sub(r'\s+',' ',target_text).lower():return False
    elif not _substantive(component):return False
    return True


def qa_evidence_errors(contract,paths,business_id=None):
    cid=contract.get('id');strict=completion_spec(contract).get('strict_qa_target',False);matched=[]
    for path in paths:
        data=_json(path)
        if not isinstance(data,dict) or data.get('contract_id')!=cid or str(data.get('status','')).lower() not in {'pass','passed'}:continue
        target=_qa_target(data,path,business_id) if strict else None
        if strict and target is None:continue
        checks=data.get('checks_performed',data.get('checks'));target_text=_qa_target_text(target)
        if not isinstance(checks,list) or not checks or not all(_qa_check_ok(item,target_text,business_id) for item in checks):continue
        if strict:
            if not isinstance(data.get('blockers'),list) or data.get('blockers'):continue
            if any(not isinstance(data.get(key),list) for key in ('issues_found','corrections_made','limitations')):continue
        matched.append(data)
    if not matched:
        suffix=' with matching contract_id, substantive per-check outcomes, no unresolved blockers, and an existing non-self target Asset at the exact tested version' if strict else ' with matching contract_id and substantive per-check outcomes'
        return [f'{cid} requires a structured JSON QA pass record{suffix}; generic self-attestation is not evidence']
    for data in matched:
        errors=qa_global_readiness_errors(data,business_id)
        if errors:return [f'{cid} {error}' for error in errors]
    return []


def qa_record_ok(contract_id,refs,business_id=None):
    contract=contract_index().get(contract_id)
    return bool(contract) and not qa_evidence_errors(contract,_paths(refs),business_id)


def _media_family(medium):
    m=str(medium or '').lower()
    if m in {'image','graphic','thumbnail'}:return 'image'
    if m=='gif':return 'gif'
    if m in {'audio','voiceover','podcast'}:return 'audio'
    if m in {'video','avatar-video','short-video','long-video','clip-extraction','demo'}:return 'video'
    if m=='animation':return 'animation'
    if m in {'presentation','slides','carousel'}:return 'presentation'
    if m=='infographic':return 'infographic'
    return 'text'


def _contains_internal_markers(path,contract_id):
    if Path(path).suffix.lower() not in TEXT_EXTS|{'.svg'}:return False
    text=_text(path).lower();cid=str(contract_id or '').lower()
    if cid and cid in text:return True
    return bool(re.search(r'\bcontract-[a-z0-9-]{8,}\b|\baura_qualification_run\b|\bqualification event\b|\bdeliverable:\s*(?:content|marketing|seo|customer|competitor|industry)\.',text))


def _png_dimensions(data):return struct.unpack('>II',data[16:24]) if len(data)>=24 and data[:8]==b'\x89PNG\r\n\x1a\n' else None
def _gif_dimensions(data):return struct.unpack('<HH',data[6:10]) if len(data)>=10 and data[:6] in {b'GIF87a',b'GIF89a'} else None
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
        if marker in {0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf} and n>=7:return int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big')
        i+=n
    return None

def _svg_dimensions(path):
    try:root=ET.parse(path).getroot()
    except Exception:return None
    def number(value):
        match=re.match(r'\s*([0-9]+(?:\.[0-9]+)?)',str(value or ''));return float(match.group(1)) if match else None
    w=number(root.get('width'));h=number(root.get('height'))
    if (not w or not h) and root.get('viewBox'):
        try:_,_,w,h=[float(x) for x in re.split(r'[ ,]+',root.get('viewBox').strip())]
        except Exception:return None
    return (w,h) if w and h else None


def _media_integrity_errors(path,family,contract_id):
    p=Path(path);ext=p.suffix.lower();data=p.read_bytes();errors=[]
    if len(data)<MIN_MEDIA_BYTES.get(family,1):return [f'{p.name} is too small to be a usable {family} artifact']
    if _contains_internal_markers(p,contract_id):errors.append(f'{p.name} exposes internal contract/qualification identifiers instead of a customer-facing artifact')
    if family in {'image','infographic'}:
        dims=_png_dimensions(data) if ext=='.png' else (_gif_dimensions(data) if ext=='.gif' else (_jpeg_dimensions(data) if ext in {'.jpg','.jpeg'} else (_svg_dimensions(p) if ext=='.svg' else None)))
        if ext=='.pdf' and not data.startswith(b'%PDF'):errors.append(f'{p.name} is not a structurally decodable PDF')
        elif ext!='.pdf' and not dims:errors.append(f'{p.name} is not a structurally decodable {family} artifact')
    elif family=='gif':
        if ext=='.gif' and not _gif_dimensions(data):errors.append(f'{p.name} is not a structurally decodable GIF')
        elif ext=='.mp4' and not (b'ftyp' in data[:64] and b'moov' in data):errors.append(f'{p.name} is not a structurally decodable video artifact')
    elif family=='video':
        if ext in {'.mp4','.mov','.m4v'} and not (b'ftyp' in data[:64] and b'moov' in data):errors.append(f'{p.name} is not a structurally decodable video artifact')
        elif ext=='.webm' and b'\x1aE\xdf\xa3' not in data[:32]:errors.append(f'{p.name} is not a structurally decodable video artifact')
    elif family=='audio':
        if not (data.startswith(b'ID3') or data.startswith(b'RIFF') or data.startswith(b'fLaC') or data.startswith(b'OggS') or b'ftyp' in data[:64]):errors.append(f'{p.name} is not a structurally decodable audio artifact')
    elif family=='presentation':
        if ext=='.pdf' and not data.startswith(b'%PDF'):errors.append(f'{p.name} is not a structurally decodable presentation PDF')
        elif ext=='.pptx':
            try:
                with zipfile.ZipFile(p) as archive:ok='[Content_Types].xml' in archive.namelist() and any(name.startswith('ppt/slides/slide') for name in archive.namelist())
            except Exception:ok=False
            if not ok:errors.append(f'{p.name} is not a structurally decodable presentation')
    return errors


def _specification_errors(path,medium,contract_id):
    text=_text(path);low=text.lower();errors=[]
    if _contains_internal_markers(path,contract_id):errors.append(f'{Path(path).name} exposes internal contract/qualification identifiers instead of the requested deliverable')
    if any(marker in low for marker in ('this file merely says','describes a future presentation without building it','generic operations guide with no production detail')):errors.append('fallback is only a placeholder/keyword shell, not a production-ready specification')
    groups=SPEC_FALLBACKS.get(medium)
    if groups and not all(any(term in low for term in group) for group in groups):errors.append(f'{medium} fallback lacks concrete production structure required to execute the requested medium')
    if medium=='presentation' and len(re.findall(r'^##\s+slide\b',text,re.I|re.M))<2:errors.append('presentation fallback lacks an actual slide-by-slide structure')
    if medium=='podcast':
        times=[int(match.group(1))*60+int(match.group(2)) for match in re.finditer(r'\b(\d{1,2}):(\d{2})\b',text)]
        declared=re.search(r'episode length\s*:\s*(\d+(?:\.\d+)?)\s*minutes?',low)
        if declared and times and max(times)>float(declared.group(1))*60:errors.append("podcast timecodes exceed the specification's declared episode duration")
        if re.search(r'\bmastered\s+to\s+-?\d+\s*lufs\b',low) and not re.search(r'future mastering|mastering target|target.*lufs',low):errors.append('text fallback claims mastered audio even though no audio artifact was supplied')
    return errors


def production_evidence_errors(contract,paths):
    cid=contract.get('id');spec=completion_spec(contract);medium=spec.get('medium');family=_media_family(medium);usable=[];errors=[]
    for path in paths:
        ext=path.suffix.lower()
        if family=='text':
            if ext not in TEXT_EXTS:errors.append(f'{path.name} has the wrong medium; expected text/document medium');continue
            if _contains_internal_markers(path,cid):errors.append(f'{path.name} exposes internal contract/qualification identifiers instead of a customer-facing artifact');continue
            if not _substantive(_text(path),5):errors.append(f'{path.name} is not a substantive text/document artifact');continue
            usable.append(path);continue
        if ext in MEDIA_EXTS.get(family,set()):
            media_errors=_media_integrity_errors(path,family,cid)
            if media_errors:errors.extend(media_errors)
            else:usable.append(path)
            continue
        if spec.get('allow_specification_fallback') and ext in TEXT_EXTS:
            spec_errors=_specification_errors(path,medium,cid)
            if spec_errors:errors.extend(spec_errors)
            else:usable.append(path)
        else:errors.append(f'{path.name} has the wrong medium for {medium}; expected a usable {family} artifact')
    if usable:return []
    return list(dict.fromkeys(errors or [f'{cid} requires a usable {medium or "production"} artifact or truthful supported production specification']))


def validate_evidence(contract,refs,business_id=None):
    """Validate actual evidence/artifact structure for one playbook method."""
    paths=_paths(refs)
    if not paths:return [f'{contract.get("id")} evidence requires at least one existing non-empty file/reference']
    spec=completion_spec(contract);profile=spec['profile']
    if profile=='qa':return qa_evidence_errors(contract,paths,business_id)
    if profile=='production':return production_evidence_errors(contract,paths)
    if profile=='intelligence':return intelligence_evidence_errors(contract,paths,business_id)
    if profile=='detector':return detector_evidence_errors(contract,paths,business_id)
    if spec.get('require_root_write_evidence'):return _declared_write_errors(contract,paths,business_id)
    for path in paths:
        if path.suffix.lower() in TEXT_EXTS and not _contains_internal_markers(path,contract.get('id')) and _substantive(_text(path),3):return []
        if path.suffix.lower() not in TEXT_EXTS:return []
    return [f'{contract.get("id")} evidence does not contain a substantive result artifact']
