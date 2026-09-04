#!/usr/bin/env python3
from pathlib import Path
import datetime,hashlib,json,os,re,sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))
from _common import PRODUCT_ROOT,workflow_files,read_frontmatter

SECTION_RE=re.compile(r'^##\s+(.+?)\s*$',re.M)
PRODUCT_SNAPSHOT_IGNORED_DIRS={'.git','__pycache__','.pytest_cache','.venv','venv'}
PRODUCT_SNAPSHOT_IGNORED_FILES={'.DS_Store'}
PRODUCT_SNAPSHOT_IGNORED_SUFFIXES={'.pyc','.pyo'}
SNAPSHOT_DIFF_IGNORED_PREFIXES=('generated/',)

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read_json(path,default=None):
    p=Path(path);return json.loads(p.read_text(encoding='utf-8')) if p.exists() else default
def write_json(path,obj):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8');return p
def section(body,name):
    matches=list(SECTION_RE.finditer(body));target=name.strip().lower()
    for i,m in enumerate(matches):
        if m.group(1).strip().lower()==target:
            start=m.end();end=matches[i+1].start() if i+1<len(matches) else len(body);return body[start:end].strip()
    return ''
def parse_process(text):
    out=[]
    for line in text.splitlines():
        m=re.match(r'^\s*(\d+)\.\s*(.*)$',line)
        if m:out.append(m.group(2).strip())
    return out
def parse_workflow(path):
    meta,body=read_frontmatter(path);wid=meta.get('id')
    if not wid:raise ValueError(f'Workflow missing id: {path}')
    return {
        'workflow_id':wid,'path':str(Path(path).relative_to(PRODUCT_ROOT)),'type':meta.get('type'),
        'owner_system':meta.get('owner_system') or wid.split('.')[0],
        'reads':meta.get('reads') or [],'writes':meta.get('writes') or [],'context':meta.get('context') or [],
        'title':next((ln[2:].strip() for ln in body.splitlines() if ln.startswith('# ')),wid),
        'purpose':section(body,'Purpose'),'business_outcome':section(body,'Business Outcome'),
        'run_when':section(body,'Run When'),'process':parse_process(section(body,'Process')),
        'completion_evidence':section(body,'Completion Evidence')
    }
def load_workflows():return [parse_workflow(p) for p in workflow_files()]
def family_for(workflow_id):
    parts=workflow_id.split('.');return '.'.join(parts[:2]) if len(parts)>1 else workflow_id
def fixture_for(workflow_id,owner):
    """Choose only the benchmark business context, never the expected method or output.

    This lightweight routing exists so local/ecommerce-specific Workflows receive a plausible
    fixture. It has no pass/fail authority and does not infer research depth, artifact type,
    evidence requirements, or quality from the Workflow id.
    """
    s=workflow_id.lower();tokens={x for x in re.split(r'[^a-z0-9]+',s) if x}
    if {'local','gbp'} & tokens or 'service-area' in s:return 'harbor-hvac'
    if {'product','shopping','cart','checkout','merch','ecommerce'} & tokens:return 'northline-commerce'
    return 'atlasops-saas'
def tree_snapshot(root):
    root=Path(root);files=[]
    if not root.exists():return {'root':str(root),'files':[],'digest':hashlib.sha256(b'').hexdigest()}
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel=str(p.relative_to(root));h=hashlib.sha256()
        try:
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
            files.append({'path':rel,'sha256':h.hexdigest(),'bytes':p.stat().st_size})
        except OSError:files.append({'path':rel,'error':'unreadable'})
    return {'root':str(root),'files':files,'digest':hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest()}
def product_snapshot_path_is_mutable(rel):
    return Path(rel).as_posix()=='.businessos/workspace.json'
def product_snapshot(root):
    root=Path(root);files=[]
    if not root.exists():return {'root':str(root),'files':[],'digest':hashlib.sha256(b'').hexdigest(),'format_version':'1.0'}
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel=p.relative_to(root);parts=rel.parts
        if any(part in PRODUCT_SNAPSHOT_IGNORED_DIRS for part in parts):continue
        if p.name in PRODUCT_SNAPSHOT_IGNORED_FILES or p.suffix.lower() in PRODUCT_SNAPSHOT_IGNORED_SUFFIXES:continue
        if product_snapshot_path_is_mutable(rel):continue
        h=hashlib.sha256()
        try:
            with p.open('rb') as f:
                for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
            files.append({'path':rel.as_posix(),'sha256':h.hexdigest(),'bytes':p.stat().st_size})
        except OSError:files.append({'path':rel.as_posix(),'error':'unreadable'})
    return {'format_version':'1.0','root':str(root),'files':files,'digest':hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest(),'file_count':len(files)}
def snapshot_diff(before,after):
    def visible(path):
        p=str(path).replace('\\','/')
        return not any(p.startswith(prefix) for prefix in SNAPSHOT_DIFF_IGNORED_PREFIXES)
    b={x['path']:x.get('sha256') for x in before.get('files',[]) if visible(x['path'])};a={x['path']:x.get('sha256') for x in after.get('files',[]) if visible(x['path'])};return {'created':sorted(set(a)-set(b)),'deleted':sorted(set(b)-set(a)),'modified':sorted(k for k in set(a)&set(b) if a[k]!=b[k])}
def workspace_from_env():
    raw=os.environ.get('BUSINESSOS_WORKSPACE')
    if not raw:raise SystemExit('BUSINESSOS_WORKSPACE must point to the qualification workspace')
    return Path(raw).expanduser().resolve()
def run_root_from_env():
    raw=os.environ.get('AURA_QUALIFICATION_RUN')
    if not raw:raise SystemExit('AURA_QUALIFICATION_RUN must point to the qualification run directory')
    return Path(raw).expanduser().resolve()
