#!/usr/bin/env python3
"""Resolve the auditable customer-facing claim surface of an Asset.

Text-native artifacts can be inspected deterministically. Opaque/rendered media must
carry a compact JSON sidecar so claim governance does not depend on OCR, transcription,
or a specific rendering vendor. Pre-publish QA remains responsible for checking parity
between that declared surface and the actual rendered artifact.
"""
from html.parser import HTMLParser
from pathlib import Path
import json, re, xml.etree.ElementTree as ET
from _common import ROOT, resolve_storage_ref

TEXT_NATIVE_EXTS={'.md','.txt','.html','.htm','.rst','.csv','.svg'}
CLAIM_SURFACE_FIELDS=('visible_text','spoken_text','material_visual_claims')


class _HTMLText(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]
    def handle_data(self,data):
        if data and data.strip(): self.parts.append(data.strip())


def _clean_text(text):
    text=re.sub(r'```.*?```',' ',text,flags=re.S)
    text=re.sub(r'[#*_>`~]+',' ',text)
    return re.sub(r'[ \t]+',' ',text)


def native_text(path):
    """Return audience-readable text for formats AURA can inspect without OCR."""
    p=Path(path); suffix=p.suffix.lower(); raw=p.read_text(encoding='utf-8',errors='replace')
    if suffix in {'.html','.htm'}:
        parser=_HTMLText(); parser.feed(raw); raw='\n'.join(parser.parts)
    elif suffix=='.svg':
        try:
            root=ET.fromstring(raw); parts=[]
            for el in root.iter():
                tag=el.tag.rsplit('}',1)[-1].lower()
                if tag not in {'text','tspan','title','desc'}: continue
                text=' '.join(x.strip() for x in el.itertext() if x and x.strip())
                if text and text not in parts: parts.append(text)
            raw='\n'.join(parts)
        except ET.ParseError:
            raw=''
    return _clean_text(raw)


def units(text):
    out=[]
    for line in (text or '').splitlines():
        line=line.strip(' -\t')
        if not line: continue
        parts=re.split(r'(?<=[.!?])\s+',line)
        for part in parts:
            part=part.strip()
            if len(part)>=4 and part not in out: out.append(part)
    return out


def _surface_values(data):
    out=[]
    for key in CLAIM_SURFACE_FIELDS:
        value=data.get(key)
        values=[value] if isinstance(value,str) else value if isinstance(value,list) else []
        for item in values:
            if isinstance(item,str) and item.strip(): out.append(item.strip())
    return out


def load_claim_surface(ref,artifact_path=None):
    """Load and minimally validate an opaque-media claim-surface sidecar."""
    try:path=resolve_storage_ref(ref)
    except Exception:return None,f'claim_surface_ref cannot be resolved: {ref!r}'
    if not path.exists() or not path.is_file():return None,f'claim_surface_ref does not exist: {ref!r}'
    try:data=json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:return None,f'claim surface is not valid JSON: {exc}'
    if not isinstance(data,dict):return None,'claim surface must be a JSON object'
    values=_surface_values(data)
    reason=data.get('no_material_claims_reason')
    if not values and not (isinstance(reason,str) and len(reason.split())>=3):
        return None,'claim surface must contain visible_text, spoken_text, material_visual_claims, or a substantive no_material_claims_reason'
    if artifact_path is not None and data.get('artifact_ref'):
        try:
            target=resolve_storage_ref(data['artifact_ref']).resolve(); actual=Path(artifact_path).resolve()
            if target!=actual:return None,'claim surface artifact_ref does not match the governed Asset location_reference'
        except Exception:return None,'claim surface artifact_ref cannot be resolved'
    return data,None


def asset_claim_units(asset,artifact_path):
    """Return claim-auditable statements plus any structural surface error."""
    path=Path(artifact_path); suffix=path.suffix.lower()
    bos=(asset.get('extensions') or {}).get('businessos',{}) if isinstance(asset.get('extensions'),dict) else {}
    statements=[]
    if suffix in TEXT_NATIVE_EXTS:
        statements.extend(units(native_text(path)))
        # Optional sidecar may add material visual/spoken claims that are not text-native.
        ref=bos.get('claim_surface_ref')
        if ref:
            surface,error=load_claim_surface(ref,path)
            if error:return [],error
            statements.extend(units('\n'.join(_surface_values(surface))))
        return list(dict.fromkeys(statements)),None

    # For opaque/rendered media, a producing Run must leave an auditable surface. Imported
    # pre-existing media is not retroactively forced through this path until it is mutated.
    origin=str(bos.get('origin','')).lower()
    produced=bool(bos.get('run_ref') or bos.get('run_id')) and origin not in {'imported','preexisting'}
    if not produced:return [],None
    ref=bos.get('claim_surface_ref')
    if not ref:return [],f'customer-facing rendered Asset {asset.get("id")} requires extensions.businessos.claim_surface_ref; opaque media cannot bypass claim governance'
    surface,error=load_claim_surface(ref,path)
    if error:return [],error
    statements.extend(units('\n'.join(_surface_values(surface))))
    return list(dict.fromkeys(statements)),None
