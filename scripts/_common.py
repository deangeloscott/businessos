from pathlib import Path
import json, re, yaml, hashlib, datetime, os, sys
ROOT=Path(__file__).resolve().parents[1]

def read_frontmatter(path):
    text=Path(path).read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}, text
    end=text.find('\n---\n',4)
    if end<0: raise ValueError(f'Unclosed frontmatter: {path}')
    meta=yaml.safe_load(text[4:end]) or {}
    return meta,text[end+5:]

def contract_files():
    return sorted([p for p in ROOT.rglob('CONTEXT.md') if '/contracts/' in p.as_posix()])

def schemas():
    return sorted(ROOT.rglob('*.schema.json'))

def load_registry():
    p=ROOT/'generated/contract-registry.json'
    if not p.exists(): raise SystemExit('Run scripts/generate_registry.py first')
    return json.loads(p.read_text())

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')


def os_version():
    p=ROOT/'VERSION'
    return p.read_text().strip() if p.exists() else '0.0.0'

def installation():
    p=ROOT/'INSTALLATION.json'
    if p.exists():
        return json.loads(p.read_text())
    installed=['core']+[p.name for p in sorted((ROOT/'systems').iterdir()) if p.is_dir()] if (ROOT/'systems').exists() else ['core']
    return {'format_version':'1.0','source_version':os_version(),'edition':'unmanaged','display_name':"ViralTrac's BusinessOS",'installed_modules':installed,'standalone_distribution':False}

def installed_modules():
    return set(installation().get('installed_modules',[]))

def publisher_metadata():
    p=ROOT/'PUBLISHER.json'
    if not p.exists(): return {}
    return json.loads(p.read_text())

def provider_registry():
    p=ROOT/'core/providers/registry.json'
    if not p.exists(): return {'format_version':'1.0','providers':[]}
    return json.loads(p.read_text())

def module_catalog():
    p=ROOT/'distribution/module-catalog.json'
    if not p.exists(): return {}
    d=json.loads(p.read_text())
    return {m['id']:m for m in d.get('modules',[])}


SYSTEMS={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
CONTEXT_TYPES={'Business','Brand','ProductService','Offer','AudienceSegment','Market','Objective','EconomicContext'}

def selector_type(sel):
    return sel.get('type') if isinstance(sel,dict) else sel

def normalize_selector(sel):
    if isinstance(sel,dict): return sel
    return {'type':sel}

def iter_instance_objects(business_id):
    base=ROOT/'instances'/business_id
    if not base.exists(): return []
    out=[]
    for p in base.rglob('*.json'):
        try: data=json.loads(p.read_text())
        except Exception: continue
        vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if isinstance(obj,dict) and obj.get('id') and obj.get('business_id')==business_id:
                out.append((obj,p))
    for p in base.rglob('*.jsonl'):
        try:
            for line in p.read_text().splitlines():
                if not line.strip(): continue
                obj=json.loads(line)
                if isinstance(obj,dict) and obj.get('id') and obj.get('business_id')==business_id: out.append((obj,p))
        except Exception: continue
    return out

def object_index(business_id):
    return {obj['id']:(obj,p) for obj,p in iter_instance_objects(business_id)}

def object_matches(obj,selector):
    s=normalize_selector(selector)
    if obj.get('object_type')!=s.get('type'): return False
    for k,v in s.items():
        if k=='type': continue
        if obj.get(k)!=v: return False
    return True

def refs_in_object(obj):
    pat=re.compile(r'\b(?:src|obs|ins|prf|opp|ini|act|wrk|apr|chg|ver|ast|mdef|mobs|exp|eval|lrn|inc|cup|cmp|plt|jrn|iev|ocs|odm|sas|aud|brd|biz|eco|mkt|obj|off|prd)_[A-Za-z0-9_-]+\b')
    return set(pat.findall(json.dumps(obj)))
