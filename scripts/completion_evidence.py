#!/usr/bin/env python3
"""Optional structural evidence checks for AURA work.

AURA may verify things it can know mechanically: referenced files exist, media is
structurally decodable, declared durable object types are actually present when a
caller explicitly asks for that check, and QA points at the real Asset/version.

This module does not infer business semantics from Workflow ids, score professional
quality, decide whether evidence is persuasive, or create an execution lifecycle.
Those judgments belong to the capable model/user and to real-work qualification.
"""
from pathlib import Path
import json
import struct
import zipfile
import xml.etree.ElementTree as ET

from _common import *

TEXT_EXTS={'.md','.txt','.html','.htm','.rst','.csv','.json'}
MEDIA_EXTS={
    'image':{'.png','.jpg','.jpeg','.webp','.svg'},
    'gif':{'.gif','.webp','.mp4'},
    'audio':{'.mp3','.wav','.m4a','.aac','.ogg','.flac'},
    'video':{'.mp4','.mov','.webm','.m4v'},
    'presentation':{'.pptx','.pdf','.html','.png','.jpg','.jpeg','.webp','.svg'},
    'infographic':{'.png','.jpg','.jpeg','.webp','.svg','.pdf'},
}
MIN_MEDIA_BYTES={'image':256,'gif':256,'audio':1024,'video':1024,'presentation':512,'infographic':256}


def _selector_types(items):
    out=set()
    for item in items or []:
        typ=item.get('type') if isinstance(item,dict) else item
        if isinstance(typ,str) and typ.strip():out.add(typ.strip())
    return out


def workflow_index():
    """Read authored Workflow source directly; generated registries are derived views."""
    out={}
    for path in workflow_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        workflow_id=meta.get('id')
        if isinstance(workflow_id,str) and workflow_id:out[workflow_id]=meta
    return out


def completion_spec(workflow):
    """Return only explicitly-authored structural verification preferences.

    Workflow names, folders, ids, reads/writes, and historical metadata are not a
    semantic classifier. If no structural profile is authored, the helper is generic.
    """
    explicit=workflow.get('completion_evidence')
    if isinstance(explicit,str):explicit={'profile':explicit}
    explicit=explicit if isinstance(explicit,dict) else {}
    return {
        'profile':str(explicit.get('profile') or 'generic'),
        'medium':explicit.get('medium'),
        'declared_write_types':sorted(_selector_types(workflow.get('writes'))),
        'allow_specification_fallback':bool(explicit.get('allow_specification_fallback',False)),
        'require_root_write_evidence':bool(explicit.get('require_root_write_evidence',False)),
        'strict_qa_target':bool(explicit.get('strict_qa_target',False)),
        'selection_authority':False,
        'semantic_authority':False,
    }


def _resolve_refs(refs):
    paths=[];unresolved=[]
    for ref in refs or []:
        try:p=resolve_storage_ref(ref)
        except Exception:
            unresolved.append(ref);continue
        if p.exists() and p.is_file() and p.stat().st_size>0:paths.append(p)
        else:unresolved.append(ref)
    return paths,unresolved


def _json(path):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except Exception:return None


def _objects_in_paths(paths,business_id=None):
    out=[]
    for path in paths:
        data=_json(path);values=data if isinstance(data,list) else [data]
        for obj in values:
            if not isinstance(obj,dict) or not obj.get('object_type'):continue
            if business_id and obj.get('business_id')!=business_id:continue
            out.append((obj,path))
    return out


def _declared_write_errors(workflow,paths,business_id):
    declared=_selector_types(workflow.get('writes'))
    seen={obj.get('object_type') for obj,_ in _objects_in_paths(paths,business_id)}
    if not declared or declared & seen:return []
    return [
        f"evidence for {workflow.get('id')} must include at least one explicitly declared durable write type "
        f"({', '.join(sorted(declared))}); observed {', '.join(sorted(x for x in seen if x)) or 'none'}"
    ]


def _ref_resolves(ref,business_id):
    if business_id and ref in object_index(business_id):return True
    try:return resolve_storage_ref(ref).exists()
    except Exception:return False


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


def _qa_ref_errors(data,business_id):
    refs=[]
    for key in ('tool_output_ref','automation_evidence_ref','scan_output_ref'):
        value=data.get(key)
        if isinstance(value,str) and value.strip():refs.append(value)
    values=data.get('evidence_refs')
    if isinstance(values,list):refs.extend(x for x in values if isinstance(x,str) and x.strip())
    checks=data.get('checks_performed',data.get('checks'))
    if isinstance(checks,list):
        for item in checks:
            if not isinstance(item,dict):continue
            for key in ('tool_output_ref','automation_evidence_ref','scan_output_ref','evidence_ref'):
                value=item.get(key)
                if isinstance(value,str) and value.strip():refs.append(value)
            values=item.get('evidence_refs')
            if isinstance(values,list):refs.extend(x for x in values if isinstance(x,str) and x.strip())
    unresolved=sorted(set(ref for ref in refs if not _ref_resolves(ref,business_id)))
    return [f"QA evidence contains unresolved reference(s): {', '.join(unresolved)}"] if unresolved else []


def qa_evidence_errors(workflow,paths,business_id=None):
    """Check QA evidence structure without deciding whether the substantive QA is good."""
    strict=completion_spec(workflow).get('strict_qa_target',False)
    failures=[]
    for path in paths:
        data=_json(path)
        if not isinstance(data,dict):continue
        checks=data.get('checks_performed',data.get('checks'))
        if not isinstance(checks,list) or not checks:
            failures.append(f'{path.name} QA record needs a non-empty checks list');continue
        if not all(isinstance(item,dict) and item for item in checks):
            failures.append(f'{path.name} QA checks must be structured objects');continue
        if strict and _qa_target(data,path,business_id) is None:
            failures.append(f'{path.name} QA record must identify an existing non-self target Asset at the exact tested version');continue
        ref_errors=_qa_ref_errors(data,business_id)
        if ref_errors:
            failures.extend(ref_errors);continue
        return []
    return list(dict.fromkeys(failures or [f"{workflow.get('id')} requires structured QA evidence"]))


def qa_record_ok(workflow_id,refs,business_id=None):
    workflow=workflow_index().get(workflow_id)
    if not workflow:return False
    paths,unresolved=_resolve_refs(refs)
    return not unresolved and bool(paths) and not qa_evidence_errors(workflow,paths,business_id)


def _media_family(medium):
    value=str(medium or '').lower()
    if value in {'image','graphic','thumbnail'}:return 'image'
    if value=='gif':return 'gif'
    if value in {'audio','voiceover','podcast'}:return 'audio'
    if value in {'video','avatar-video','short-video','long-video','clip-extraction','demo'}:return 'video'
    if value=='animation':return 'animation'
    if value in {'presentation','slides','carousel'}:return 'presentation'
    if value=='infographic':return 'infographic'
    return 'text'


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
        if marker in {0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf} and n>=7:
            return int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big')
        i+=n
    return None


def _svg_dimensions(path):
    try:root=ET.parse(path).getroot()
    except Exception:return None
    def number(value):
        raw=''.join(ch for ch in str(value or '') if ch.isdigit() or ch=='.')
        try:return float(raw) if raw else None
        except Exception:return None
    width=number(root.get('width'));height=number(root.get('height'))
    if (not width or not height) and root.get('viewBox'):
        try:_,_,width,height=[float(x) for x in root.get('viewBox').replace(',',' ').split()]
        except Exception:return None
    return (width,height) if width and height else None


def _media_integrity_errors(path,family):
    p=Path(path);ext=p.suffix.lower();data=p.read_bytes();errors=[]
    if len(data)<MIN_MEDIA_BYTES.get(family,1):return [f'{p.name} is too small to be a usable {family} artifact']
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
                with zipfile.ZipFile(p) as archive:
                    ok='[Content_Types].xml' in archive.namelist() and any(name.startswith('ppt/slides/slide') for name in archive.namelist())
            except Exception:ok=False
            if not ok:errors.append(f'{p.name} is not a structurally decodable presentation')
    return errors


def production_evidence_errors(workflow,paths):
    """Verify promised medium/decodability only; creative quality is semantic review."""
    spec=completion_spec(workflow);medium=spec.get('medium');family=_media_family(medium)
    if not medium:return []
    errors=[]
    for path in paths:
        ext=path.suffix.lower()
        if family=='text':
            if ext in TEXT_EXTS:return []
            errors.append(f'{path.name} has the wrong medium; expected text/document evidence');continue
        if ext in MEDIA_EXTS.get(family,set()):
            media_errors=_media_integrity_errors(path,family)
            if not media_errors:return []
            errors.extend(media_errors);continue
        if spec.get('allow_specification_fallback') and ext in TEXT_EXTS:
            return []
        errors.append(f'{path.name} has the wrong medium for {medium}; expected a usable {family} artifact')
    return list(dict.fromkeys(errors or [f"{workflow.get('id')} lacks usable {medium or 'production'} evidence"]))


def validate_evidence(workflow,refs,business_id=None):
    """Validate only deterministic evidence structure for one Workflow.

    Passing means the supplied references satisfy the explicitly requested structural
    checks. It does not mean the work is strategically correct, complete, persuasive,
    authorized, deployed, or professionally excellent.
    """
    paths,unresolved=_resolve_refs(refs)
    if unresolved:return [f"{workflow.get('id')} evidence contains unresolved or empty reference(s): {', '.join(map(str,unresolved))}"]
    if not paths:return [f"{workflow.get('id')} evidence requires at least one existing non-empty file/reference"]
    spec=completion_spec(workflow)
    if spec.get('profile')=='qa':return qa_evidence_errors(workflow,paths,business_id)
    if spec.get('profile')=='production':return production_evidence_errors(workflow,paths)
    if spec.get('require_root_write_evidence'):return _declared_write_errors(workflow,paths,business_id)
    return []
