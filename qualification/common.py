#!/usr/bin/env python3
from pathlib import Path
import datetime, hashlib, json, os, re, sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0,str(SCRIPTS))
from _common import PRODUCT_ROOT, contract_files, read_frontmatter

SECTION_RE=re.compile(r'^##\s+(.+?)\s*$',re.M)
PRODUCT_SNAPSHOT_IGNORED_DIRS={'.git','__pycache__','.pytest_cache','.venv','venv'}
PRODUCT_SNAPSHOT_IGNORED_FILES={'.DS_Store'}
PRODUCT_SNAPSHOT_IGNORED_SUFFIXES={'.pyc','.pyo'}

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def read_json(path, default=None):
    p=Path(path)
    if not p.exists(): return default
    return json.loads(p.read_text(encoding='utf-8'))

def write_json(path,obj):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    return p

def section(body,name):
    matches=list(SECTION_RE.finditer(body))
    target=name.strip().lower()
    for i,m in enumerate(matches):
        if m.group(1).strip().lower()==target:
            start=m.end(); end=matches[i+1].start() if i+1<len(matches) else len(body)
            return body[start:end].strip()
    return ''

def parse_process(text):
    out=[]
    for line in text.splitlines():
        m=re.match(r'^\s*(\d+)\.\s*(.*)$',line)
        if m: out.append(m.group(2).strip())
    return out

def parse_contract(path):
    meta,body=read_frontmatter(path)
    cid=meta.get('id')
    if not cid: raise ValueError(f'Contract missing id: {path}')
    return {
        'contract_id':cid,
        'path':str(Path(path).relative_to(PRODUCT_ROOT)),
        'type':meta.get('type'),
        'version':meta.get('version'),
        'owner_system':meta.get('owner_system') or cid.split('.')[0],
        'artifact_role':meta.get('artifact_role'),
        'reads':meta.get('reads') or [],
        'writes':meta.get('writes') or [],
        'capabilities':meta.get('capabilities') or {},
        'context':meta.get('context') or [],
        'subcontracts':meta.get('subcontracts') or {},
        'title': next((ln[2:].strip() for ln in body.splitlines() if ln.startswith('# ')),cid),
        'purpose':section(body,'Purpose'),
        'business_outcome':section(body,'Business Outcome'),
        'run_when':section(body,'Run When'),
        'process':parse_process(section(body,'Process')),
        'completion_evidence':section(body,'Completion Evidence'),
    }

def load_contracts():
    return [parse_contract(p) for p in contract_files()]

def family_for(contract_id):
    parts=contract_id.split('.')
    return '.'.join(parts[:2]) if len(parts)>1 else contract_id

def fixture_for(contract_id,owner):
    """Choose a representative benchmark business without accidental substring matches.

    Contract IDs contain words such as `production`; naive `"product" in id` matching
    misclassified those as ecommerce. Route on normalized ID tokens/phrases instead.
    """
    s=contract_id.lower()
    tokens={x for x in re.split(r'[^a-z0-9]+',s) if x}
    if {'local','gbp'} & tokens or 'service-area' in s: return 'harbor-hvac'
    if {'product','shopping','cart','checkout','merch','ecommerce'} & tokens: return 'northline-commerce'
    return 'atlasops-saas'

def competitive_profile(contract):
    cid=contract['contract_id'].lower(); owner=contract['owner_system']
    if owner=='seo-aeo':
        return 'search_live_field' if any(k in cid for k in ('content','page','query','keyword','serp','aeo','answer','citation','opportunity','strategy','brief')) else 'search_technical'
    if owner=='marketing-synthesis':
        return 'paid_and_persuasion_field' if any(k in cid for k in ('ad','creative','landing','campaign','offer','vsl','webinar','email','quiz','advertorial')) else 'marketing_outcome'
    if owner=='content-synthesis':
        return 'organic_attention_field' if any(k in cid for k in ('trend','creator','platform','content-performance','adaptation')) else 'artifact_excellence'
    if owner=='competitor-intelligence': return 'competitive_intelligence'
    if owner=='customer-intelligence': return 'customer_truth'
    if owner=='industry-intelligence': return 'ecosystem_truth'
    if owner=='customer-optimization': return 'first_party_outcomes'
    return 'organizational_memory'

def output_policy(contract):
    cid=contract['contract_id'].lower(); role=contract.get('artifact_role')
    artifact_words=('article','newsletter','video','podcast','carousel','presentation','infographic','image','animation','gif','case-study','demo','landing-page','vsl','webinar','ad','creative','email','quiz','advertorial','asset')
    artifact_required=bool(role=='customer_facing_production_root' or any(k in cid for k in artifact_words))
    return {
        'artifact_required':artifact_required,
        'declared_writes':contract.get('writes') or [],
        'write_expectation':'persist_only_when_materially_produced',
        'actual_output_not_description':artifact_required,
    }

def tree_snapshot(root):
    root=Path(root); files=[]
    if not root.exists(): return {'root':str(root),'files':[],'digest':hashlib.sha256(b'').hexdigest()}
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel=str(p.relative_to(root)); h=hashlib.sha256()
        try:
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
            files.append({'path':rel,'sha256':h.hexdigest(),'bytes':p.stat().st_size})
        except OSError:
            files.append({'path':rel,'error':'unreadable'})
    digest=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
    return {'root':str(root),'files':files,'digest':digest}

def product_snapshot_path_is_mutable(rel):
    """Return True only for local state that is explicitly outside protected product source.

    Workspace selection metadata and a product-local `.businessos/environments/` overlay
    are host/user state. Shipped `deployment/environments/` files are product defaults and
    remain protected during qualification; ordinary host discovery must never rewrite them.
    """
    rel=Path(rel); posix=rel.as_posix()
    if posix=='.businessos/workspace.json': return True
    return len(rel.parts)>=2 and rel.parts[0]=='.businessos' and rel.parts[1]=='environments'

def product_snapshot(root):
    """Stable qualification snapshot of protected staged product source.

    Transient interpreter/editor files and explicitly workspace-local `.businessos` state
    are ignored. Product source, playbooks, policies, schemas, scripts, shipped deployment
    defaults/templates, and other installed content remain immutable during qualification.
    """
    root=Path(root); files=[]
    if not root.exists(): return {'root':str(root),'files':[],'digest':hashlib.sha256(b'').hexdigest(),'format_version':'1.0'}
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel=p.relative_to(root); parts=rel.parts
        if any(part in PRODUCT_SNAPSHOT_IGNORED_DIRS for part in parts): continue
        if p.name in PRODUCT_SNAPSHOT_IGNORED_FILES or p.suffix.lower() in PRODUCT_SNAPSHOT_IGNORED_SUFFIXES: continue
        if product_snapshot_path_is_mutable(rel): continue
        h=hashlib.sha256()
        try:
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
            files.append({'path':rel.as_posix(),'sha256':h.hexdigest(),'bytes':p.stat().st_size})
        except OSError:
            files.append({'path':rel.as_posix(),'error':'unreadable'})
    digest=hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()
    return {'format_version':'1.0','root':str(root),'files':files,'digest':digest,'file_count':len(files)}

def snapshot_diff(before,after):
    b={x['path']:x.get('sha256') for x in before.get('files',[])}; a={x['path']:x.get('sha256') for x in after.get('files',[])}
    return {'created':sorted(set(a)-set(b)),'deleted':sorted(set(b)-set(a)),'modified':sorted(k for k in set(a)&set(b) if a[k]!=b[k])}

def workspace_from_env():
    raw=os.environ.get('BUSINESSOS_WORKSPACE')
    if not raw: raise SystemExit('BUSINESSOS_WORKSPACE must point to the qualification workspace')
    return Path(raw).expanduser().resolve()

def run_root_from_env():
    raw=os.environ.get('AURA_QUALIFICATION_RUN')
    if not raw: raise SystemExit('AURA_QUALIFICATION_RUN must point to the qualification run directory')
    return Path(raw).expanduser().resolve()
