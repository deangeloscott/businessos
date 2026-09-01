from pathlib import Path
import json, re, yaml, hashlib, datetime, os, sys, tempfile

PRODUCT_ROOT=Path(__file__).resolve().parents[1]
_WORKSPACE_ENV='BUSINESSOS_WORKSPACE'
_WORKSPACE_CONFIG_ENV='BUSINESSOS_WORKSPACE_CONFIG'
_STATE_NAMESPACES={'instances','runtime','knowledge','attachments'}
_ENVIRONMENT_OVERLAY_REL=Path('.businessos/environments')


def workspace_config_path():
    override=os.environ.get(_WORKSPACE_CONFIG_ENV)
    if override:
        p=Path(os.path.expanduser(os.path.expandvars(override)))
        return p if p.is_absolute() else (PRODUCT_ROOT/p).resolve()
    return PRODUCT_ROOT/'.businessos/workspace.json'


def workspace_selection_source():
    if os.environ.get(_WORKSPACE_ENV): return 'environment'
    if workspace_config_path().exists(): return 'local_link'
    return 'default_product_root'


def _read_workspace_link():
    p=workspace_config_path()
    if not p.exists(): return {}
    try:
        data=json.loads(p.read_text())
    except Exception as e:
        raise ValueError(f'Invalid BusinessOS workspace config {p}: {e}')
    return data if isinstance(data,dict) else {}


def _raw_workspace_root():
    raw=os.environ.get(_WORKSPACE_ENV) or _read_workspace_link().get('workspace_root')
    if not raw: return PRODUCT_ROOT
    p=Path(os.path.expanduser(os.path.expandvars(str(raw))))
    return p.resolve() if p.is_absolute() else (PRODUCT_ROOT/p).resolve()


_BasePath=type(Path())


class WorkspacePath(_BasePath):
    """Workspace path that preserves legacy logical refs relative to ROOT.

    Older helpers commonly call `state_path.relative_to(ROOT)`. When state is external,
    returning the workspace-relative path preserves portable refs such as
    `instances/acme/...` and `runtime/runs/acme/...` instead of leaking host paths.
    """
    def relative_to(self, other, *args, **kwargs):
        try:
            other_resolved=Path(other).resolve()
            ws=Path(_raw_workspace_root()).resolve()
            me=Path(self).resolve()
            if other_resolved==PRODUCT_ROOT.resolve() and ws!=PRODUCT_ROOT.resolve() and me.is_relative_to(ws):
                return me.relative_to(ws)
        except Exception:
            pass
        return super().relative_to(other,*args,**kwargs)


class BusinessOSRoot(_BasePath):
    """Product root with transparent state-namespace redirection.

    Product files (`core/`, `systems/`, `scripts/`, schemas, tests, distribution metadata)
    always resolve under PRODUCT_ROOT. Durable/working state namespaces can resolve to an
    explicitly configured external workspace without forcing every existing helper to
    know where that workspace lives.
    """
    def __truediv__(self, key):
        try:
            kp=Path(key)
            if Path(self).resolve()==PRODUCT_ROOT.resolve() and not kp.is_absolute() and kp.parts:
                first=kp.parts[0]
                # The packaged business template is product source, not active workspace state.
                template_ref=(first=='instances' and len(kp.parts)>1 and kp.parts[1]=='_template')
                if first in _STATE_NAMESPACES and not template_ref:
                    return WorkspacePath(_raw_workspace_root()).joinpath(*kp.parts)
        except Exception:
            pass
        return super().__truediv__(key)


ROOT=BusinessOSRoot(PRODUCT_ROOT)


def workspace_root(): return WorkspacePath(_raw_workspace_root())
def workspace_is_external(): return workspace_root().resolve()!=PRODUCT_ROOT.resolve()
def instances_root(): return workspace_root()/'instances'
def runtime_root(): return workspace_root()/'runtime'
def knowledge_root(): return workspace_root()/'knowledge'
def attachments_root(): return workspace_root()/'attachments'
def instance_dir(business_id): return instances_root()/business_id
def run_dir_path(business_id,run_id): return runtime_root()/'runs'/business_id/run_id
def product_instance_template(): return PRODUCT_ROOT/'instances/_template'


def environment_product_dir(environment):
    return PRODUCT_ROOT/'deployment/environments'/str(environment)


def environment_overlay_dir(environment,create=False):
    """Host/environment state owned by the active workspace, never product source."""
    path=workspace_root()/_ENVIRONMENT_OVERLAY_REL/str(environment)
    if create:path.mkdir(parents=True,exist_ok=True)
    return path


def environment_exists(environment):
    return environment_overlay_dir(environment).exists() or environment_product_dir(environment).exists()


def environment_names():
    names=set()
    for root in (PRODUCT_ROOT/'deployment/environments', workspace_root()/_ENVIRONMENT_OVERLAY_REL):
        if root.exists():
            names.update(p.name for p in root.iterdir() if p.is_dir() and p.name!='_template')
    return sorted(names)


def environment_file(environment,relative,writable=False,seed_product_default=True):
    """Resolve effective environment config with workspace overlay > shipped default.

    Reads prefer workspace-owned host state and fall back per-file to immutable product
    defaults. Writes always target the workspace overlay. When useful, a shipped default
    is copied once into the overlay before mutation so normal runtime configuration never
    dirties the AURA product tree or conflicts with product upgrades.
    """
    rel=Path(relative)
    if rel.is_absolute() or '..' in rel.parts: raise ValueError('Environment-relative path required')
    if not environment_exists(environment): raise ValueError(f'Unknown environment: {environment}')
    overlay=environment_overlay_dir(environment,create=writable)/rel
    product=environment_product_dir(environment)/rel
    if writable:
        overlay.parent.mkdir(parents=True,exist_ok=True)
        if seed_product_default and not overlay.exists() and product.exists() and product.is_file():
            overlay.write_bytes(product.read_bytes())
        return overlay
    return overlay if overlay.exists() else product


def workspace_profile():
    root=workspace_root(); p=root/'.businessos/workspace.json'
    if p.exists():
        try:
            d=json.loads(p.read_text())
            if isinstance(d,dict): return d
        except Exception: pass
    link={} if workspace_selection_source()=='environment' else _read_workspace_link()
    return {'profile':link.get('profile','simple'),'workspace_root':str(root),'knowledge_enabled':link.get('knowledge_enabled',True)}


def business_ids():
    root=instances_root()
    if not root.exists(): return []
    return sorted(p.name for p in root.iterdir() if p.is_dir() and p.name!='_template')


def resolve_business(explicit=None):
    """Resolve exactly one active business without guessing across workspace instances."""
    explicit=explicit or os.environ.get('BUSINESSOS_BUSINESS_ID')
    ids=business_ids()
    if explicit:
        if explicit in ids:return {'status':'resolved','business_id':explicit,'resolution':'explicit'}
        return {'status':'needs_input','missing':['active_business'],'reason':f'Unknown business: {explicit}','available_business_ids':ids}
    if len(ids)==1:return {'status':'resolved','business_id':ids[0],'resolution':'single_workspace_business'}
    if not ids:return {'status':'needs_input','missing':['active_business'],'reason':'No initialized business exists in the active organization workspace.','available_business_ids':[]}
    return {'status':'needs_input','missing':['active_business'],'reason':'Multiple businesses exist in the active organization workspace; the active business is ambiguous.','available_business_ids':ids}


def write_json_atomic(path,data):
    """Write JSON atomically in the destination directory."""
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);tmp=None
    try:
        fd,tmp=tempfile.mkstemp(prefix=f'.{p.name}.',suffix='.tmp',dir=str(p.parent))
        with os.fdopen(fd,'w',encoding='utf-8') as handle:
            json.dump(data,handle,indent=2,ensure_ascii=False);handle.write('\n');handle.flush();os.fsync(handle.fileno())
        os.replace(tmp,p);tmp=None
    finally:
        if tmp:
            try:Path(tmp).unlink()
            except FileNotFoundError:pass
    return p


def storage_ref(path):
    p=Path(path).resolve(); ws=workspace_root().resolve(); prod=PRODUCT_ROOT.resolve()
    if p.is_relative_to(ws): return p.relative_to(ws).as_posix()
    if p.is_relative_to(prod): return 'product:'+p.relative_to(prod).as_posix()
    return str(p)


def resolve_storage_ref(ref):
    s=str(ref)
    if s.startswith('product:'): return PRODUCT_ROOT/s[len('product:'):]
    p=Path(s)
    if p.is_absolute(): return p
    if p.parts and p.parts[0] in _STATE_NAMESPACES: return workspace_root()/p
    candidate=workspace_root()/p
    if candidate.exists(): return candidate
    return PRODUCT_ROOT/p


def read_frontmatter(path):
    text=Path(path).read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}, text
    end=text.find('\n---\n',4)
    if end<0: raise ValueError(f'Unclosed frontmatter: {path}')
    meta=yaml.safe_load(text[4:end]) or {}
    return meta,text[end+5:]
def contract_files():
    return sorted([p for p in PRODUCT_ROOT.rglob('CONTEXT.md') if '/contracts/' in p.as_posix()])
def schemas():
    return sorted(PRODUCT_ROOT.rglob('*.schema.json'))
def load_registry():
    p=PRODUCT_ROOT/'generated/contract-registry.json'
    if not p.exists(): raise SystemExit('Run scripts/generate_registry.py first')
    return json.loads(p.read_text())
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')


def os_version():
    p=PRODUCT_ROOT/'VERSION'
    return p.read_text().strip() if p.exists() else '0.0.0'
def installation():
    p=PRODUCT_ROOT/'INSTALLATION.json'
    if p.exists():
        return json.loads(p.read_text())
    installed=['core']+[p.name for p in sorted((PRODUCT_ROOT/'systems').iterdir()) if p.is_dir()] if (PRODUCT_ROOT/'systems').exists() else ['core']
    return {'format_version':'1.0','source_version':os_version(),'edition':'unmanaged','display_name':'ViralTrac AURA','public_name':'ViralTrac AURA','name_expansion':'Agentic Understanding and Reinforcement Architecture','descriptor':'AI-native BusinessOS','installed_modules':installed,'standalone_distribution':False}
def installed_modules():
    return set(installation().get('installed_modules',[]))
def publisher_metadata():
    p=PRODUCT_ROOT/'PUBLISHER.json'
    if not p.exists(): return {}
    return json.loads(p.read_text())
def module_catalog():
    p=PRODUCT_ROOT/'distribution/module-catalog.json'
    if not p.exists(): return {}
    d=json.loads(p.read_text())
    return {m['id']:m for m in d.get('modules',[])}


SYSTEMS={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
CONTEXT_TYPES={'Business','Brand','ProductService','Offer','AudienceSegment','Market','Objective','EconomicContext','BusinessClaim','PreferenceProfile'}

def selector_type(sel):
    return sel.get('type') if isinstance(sel,dict) else sel
def normalize_selector(sel):
    if isinstance(sel,dict): return sel
    return {'type':sel}
def iter_instance_objects(business_id):
    base=instance_dir(business_id)
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
    pat=re.compile(r'\b(?:src|sprof|obs|ins|prf|opp|ini|wrk|chg|ver|ast|mdef|mobs|exp|eval|lrn|inc|att|plc|cup|cmp|plt|jrn|iev|ocs|odm|sas|aud|brd|biz|eco|mkt|obj|off|prd|clm)_[A-Za-z0-9_-]+\b')
    return set(pat.findall(json.dumps(obj)))
