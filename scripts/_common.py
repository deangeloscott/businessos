from pathlib import Path
import json, re, yaml, hashlib, datetime, os, sys, tempfile, stat
import functools, inspect, threading, time
from contextlib import contextmanager
from contextvars import ContextVar

# AURA files and CLI text use UTF-8, including redirected Windows output.
for _stream in (sys.stdout,sys.stderr):
    if hasattr(_stream,'reconfigure'):_stream.reconfigure(encoding='utf-8')

PRODUCT_ROOT=Path(__file__).resolve().parents[1]
_WORKSPACE_ENV='BUSINESSOS_WORKSPACE'
_WORKSPACE_CONFIG_ENV='BUSINESSOS_WORKSPACE_CONFIG'
_STATE_NAMESPACES={'instances','runtime','knowledge','attachments'}
_WORKSPACE_SCOPE=ContextVar('aura_workspace_scope',default=None)
_TRANSACTION_LOCKS={}
_TRANSACTION_GUARD=threading.Lock()
_TRANSACTION_LOCAL=threading.local()


def path_link(path):
    """Recognize symlinks and Windows junctions, including older Python hosts."""
    try:info=Path(path).lstat()
    except FileNotFoundError:return False
    return stat.S_ISLNK(info.st_mode) or getattr(info,'st_reparse_tag',None)==0xA0000003


@contextmanager
def business_transaction(business_id):
    """Serialize supported organization mutations, including validation and rollback.

    An OS-owned lock covers CLI processes; an RLock covers threads and nested helpers.
    Locks live outside canonical records and release automatically on process exit.
    """
    if not isinstance(business_id,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',business_id):
        raise ValueError('Choose a valid organization before saving changes.')
    root=Path(workspace_root()).resolve()
    path=root/'.businessos/locks'/f'{business_id}.lock'
    for candidate in (path,path.parent,path.parent.parent):
        if path_link(candidate):
            raise ValueError('The workspace lock folder is linked elsewhere. Choose its original workspace folder.')
    key=os.path.normcase(str(path))
    with _TRANSACTION_GUARD:
        lock=_TRANSACTION_LOCKS.setdefault(key,threading.RLock())
    if not lock.acquire(timeout=30):
        raise ValueError('Another save is still using this organization. Wait a moment and try again.')
    try:
        held=getattr(_TRANSACTION_LOCAL,'held',set())
        if key in held:
            yield
            return
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('a+b') as handle:
            handle.seek(0,2)
            if not handle.tell():handle.write(b'0');handle.flush()
            deadline=time.monotonic()+30
            while True:
                try:
                    handle.seek(0)
                    if os.name=='nt':
                        import msvcrt
                        msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
                    else:
                        import fcntl
                        fcntl.flock(handle.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
                    break
                except OSError:
                    if time.monotonic()>=deadline:
                        raise ValueError('Another save is still using this organization. Wait a moment and try again.') from None
                    time.sleep(.05)
            _TRANSACTION_LOCAL.held=held|{key}
            try:yield
            finally:
                _TRANSACTION_LOCAL.held=held
                handle.seek(0)
                if os.name=='nt':msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
                else:fcntl.flock(handle.fileno(),fcntl.LOCK_UN)
    finally:lock.release()


def organization_transaction(fn):
    """Guard a mutation whose first argument is its organization ID."""
    signature=inspect.signature(fn)
    @functools.wraps(fn)
    def guarded(*args,**kwargs):
        bound=signature.bind(*args,**kwargs);bound.apply_defaults()
        bid=next(iter(bound.arguments.values()))
        with business_transaction(bid):return fn(*args,**kwargs)
    return guarded


@contextmanager
def workspace_scope(root):
    """Pin helper resolution for one request without changing CLI selection."""
    token=_WORKSPACE_SCOPE.set(str(Path(root).resolve()))
    try:yield
    finally:_WORKSPACE_SCOPE.reset(token)


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
        data=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        raise ValueError(f'Invalid BusinessOS workspace config {p}: {e}')
    return data if isinstance(data,dict) else {}


def _raw_workspace_root():
    scoped=_WORKSPACE_SCOPE.get()
    if scoped:return Path(scoped)
    raw=os.environ.get(_WORKSPACE_ENV) or _read_workspace_link().get('workspace_root')
    if not raw: return PRODUCT_ROOT
    p=Path(os.path.expanduser(os.path.expandvars(str(raw))))
    return p.resolve() if p.is_absolute() else (PRODUCT_ROOT/p).resolve()


_BasePath=type(Path())


class WorkspacePath(_BasePath):
    """Workspace path that keeps portable logical refs relative to the AURA workspace.

    When organization state is external, callers may still need stable refs such as
    `instances/acme/...` and `runtime/runs/acme/...` rather than host-specific paths.
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
    """Product root with transparent routing only for organization-owned state namespaces.

    Product files (`core/`, `systems/`, `scripts/`, schemas, tests, distribution metadata)
    resolve under PRODUCT_ROOT. Organization-owned state namespaces may resolve to an
    explicitly configured external workspace so local-first state stays separate from
    immutable product source while retaining portable logical references.
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


def workspace_profile():
    root=workspace_root(); p=root/'.businessos/workspace.json'
    if p.exists():
        try:
            d=json.loads(p.read_text(encoding='utf-8'))
            if isinstance(d,dict): return d
        except Exception: pass
    link={} if workspace_selection_source()=='environment' else _read_workspace_link()
    return {'profile':link.get('profile','simple'),'workspace_root':str(root),'knowledge_enabled':link.get('knowledge_enabled',True)}


def business_ids():
    root=instances_root()
    if not root.exists(): return []
    return sorted(p.name for p in root.iterdir() if p.is_dir() and p.name!='_template')


def business_directory():
    """Return the smallest useful organization directory for model-side resolution.

    AURA exposes stable identity; the active model/harness interprets natural-language
    references and chooses a business_id. No fuzzy/semantic matching belongs here.
    """
    rows=[]
    for business_id in business_ids():
        base=instance_dir(business_id);name=None
        bp=base/'context/business.json'
        if bp.exists():
            try:
                value=json.loads(bp.read_text(encoding='utf-8')).get('name')
                if isinstance(value,str) and value.strip():name=value.strip()
            except Exception:pass
        if not name:
            ip=base/'instance.json'
            if ip.exists():
                try:
                    value=json.loads(ip.read_text(encoding='utf-8')).get('name')
                    if isinstance(value,str) and value.strip():name=value.strip()
                except Exception:pass
        rows.append({'id':business_id,'name':name or business_id})
    return rows


def resolve_business(explicit=None):
    """Resolve exactly one active business without guessing across workspace instances."""
    explicit=explicit or os.environ.get('BUSINESSOS_BUSINESS_ID')
    ids=business_ids()
    if explicit and explicit in ids:return {'status':'resolved','business_id':explicit,'resolution':'explicit'}
    if explicit:
        directory=business_directory()
        return {'status':'needs_input','missing':['active_business'],'reason':f'Unknown business: {explicit}','available_business_ids':ids,'available_businesses':directory}
    if len(ids)==1:return {'status':'resolved','business_id':ids[0],'resolution':'single_workspace_business'}
    directory=business_directory()
    if not ids:return {'status':'needs_input','missing':['active_business'],'reason':'No initialized business exists in the active organization workspace.','available_business_ids':[],'available_businesses':[]}
    return {'status':'needs_input','missing':['active_business'],'reason':'Multiple businesses exist in the active organization workspace; the active business is ambiguous.','available_business_ids':ids,'available_businesses':directory}


def write_json_atomic(path,data):
    p=Path(path);root=Path(workspace_root()).resolve()
    relative=p.absolute().relative_to(root) if p.absolute().is_relative_to(root) else None
    if relative and len(relative.parts)>2 and relative.parts[0]=='instances' and relative.parts[1]!='_template':
        with business_transaction(relative.parts[1]):return _write_json_atomic(p,data)
    return _write_json_atomic(p,data)


def _write_json_atomic(path,data):
    """Write JSON atomically in the destination directory."""
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);tmp=None
    try:
        fd,tmp=tempfile.mkstemp(prefix=f'.{p.name}.',suffix='.tmp',dir=str(p.parent))
        with os.fdopen(fd,'w',encoding='utf-8') as handle:
            json.dump(data,handle,indent=2,ensure_ascii=False);handle.write('\n');handle.flush();os.fsync(handle.fileno())
        root=workspace_root().resolve()
        relative=p.absolute().relative_to(root) if p.absolute().is_relative_to(root) else None
        if relative and len(relative.parts)>2 and relative.parts[0]=='instances' and p.is_file():
            import workspace_history
            try:workspace_history.managed(p,relative.parts[1])
            except ValueError:pass
            else:workspace_history.capture(p,relative.parts[1],'Before business record change')
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
def workflow_files():
    return sorted([p for p in PRODUCT_ROOT.rglob('CONTEXT.md') if '/workflows/' in p.as_posix()])
def schemas():
    return sorted(PRODUCT_ROOT.rglob('*.schema.json'))
def load_registry():
    p=PRODUCT_ROOT/'generated/workflow-registry.json'
    if not p.exists(): raise SystemExit('Run scripts/generate_registry.py first')
    return json.loads(p.read_text(encoding='utf-8'))
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')


def os_version():
    p=PRODUCT_ROOT/'VERSION'
    return p.read_text(encoding='utf-8').strip() if p.exists() else '0.0.0'
def installation():
    p=PRODUCT_ROOT/'INSTALLATION.json'
    if p.exists():
        return json.loads(p.read_text(encoding='utf-8'))
    installed=['core']+[p.name for p in sorted((PRODUCT_ROOT/'systems').iterdir()) if p.is_dir()] if (PRODUCT_ROOT/'systems').exists() else ['core']
    return {'format_version':'1.0','source_version':os_version(),'edition':'unmanaged','display_name':'ViralTrac AURA','public_name':'ViralTrac AURA','name_expansion':'Agentic Understanding and Reinforcement Architecture','descriptor':'organization-owned memory and operating knowledge for capable AI','installed_modules':installed,'standalone_distribution':False}
def installed_modules():
    return set(installation().get('installed_modules',[]))
def publisher_metadata():
    p=PRODUCT_ROOT/'PUBLISHER.json'
    if not p.exists(): return {}
    return json.loads(p.read_text(encoding='utf-8'))
def module_catalog():
    p=PRODUCT_ROOT/'distribution/module-catalog.json'
    if not p.exists(): return {}
    d=json.loads(p.read_text(encoding='utf-8'))
    return {m['id']:m for m in d.get('modules',[])}


SYSTEMS={'core','customer-intelligence','competitor-intelligence','industry-intelligence','seo-aeo','content-synthesis','marketing-synthesis','customer-optimization'}
CONTEXT_TYPES={'Business','Brand','ProductService','Offer','AudienceSegment','Market','Objective','EconomicContext','BusinessClaim','PreferenceProfile'}

def selector_type(sel):
    return sel.get('type') if isinstance(sel,dict) else sel
def normalize_selector(sel):
    if isinstance(sel,dict): return sel
    return {'type':sel}
def iter_instance_objects(business_id,diagnostics=None):
    """Read usable canonical objects; report unreadable canonical locations."""
    from canonical_store import INSTANCE_PATHS
    base=instance_dir(business_id)
    if not base.exists():return []
    locations=set(INSTANCE_PATHS.values());out=[]
    def report(path,reason,line=None):
        row={'path':storage_ref(path),'reason':str(reason)}
        if line is not None:row['line']=line
        if diagnostics is not None:diagnostics.append(row)
        else:print(f'WARNING unreadable canonical record: {row}',file=sys.stderr)
    def consume(data,path,expected,line=None):
        vals=data if isinstance(data,list) else [data]
        for obj in vals:
            if isinstance(obj,dict) and obj.get('id') and obj.get('object_type'):
                if not expected and obj['object_type'] not in INSTANCE_PATHS:continue
                if obj.get('business_id')==business_id:out.append((obj,path))
                else:report(path,'canonical business_id does not match this organization',line)
            elif expected:report(path,'expected canonical object with id, object_type and business_id',line)
    for path in sorted(base.rglob('*')):
        if path.suffix not in {'.json','.jsonl'} or not path.is_file():continue
        rel=path.relative_to(base)
        expected=rel.as_posix() in locations or rel.parent.as_posix() in locations
        expected=expected or (len(rel.parts)==3 and rel.parts[0]=='history' and rel.parts[1] in INSTANCE_PATHS)
        try:text=path.read_text(encoding='utf-8')
        except (OSError,UnicodeError) as exc:
            if expected:report(path,exc)
            continue
        if path.suffix=='.jsonl':
            for number,line in enumerate(text.splitlines(),1):
                if not line.strip():continue
                try:consume(json.loads(line),path,expected,number)
                except json.JSONDecodeError as exc:
                    if expected:report(path,exc,number)
        else:
            try:consume(json.loads(text),path,expected)
            except json.JSONDecodeError as exc:
                if expected:report(path,exc)
    return out
def object_index(business_id,diagnostics=None):
    index={}
    for obj,path in iter_instance_objects(business_id,diagnostics):
        if obj['id'] in index:
            row={'path':storage_ref(path),'reason':f'duplicate canonical id {obj["id"]}; resolve ambiguity before relying on it'}
            if diagnostics is not None:diagnostics.append(row)
            else:print(f'WARNING {row}',file=sys.stderr)
        else:index[obj['id']]=(obj,path)
    return index

def object_title(obj):
    return next((obj.get(key) for key in ('title','name','subject_name','statement','summary','business_role','purpose','description','conclusion','task','display_name','asset_type') if isinstance(obj.get(key),str) and obj[key].strip()),obj.get('id') or obj.get('object_type','Object'))

def describe_object(obj,path):
    """Small, readable lookup result; the original record remains authoritative."""
    title=object_title(obj)
    result={'object_ref':obj['id'],'object_type':obj.get('object_type'),'path':storage_ref(path),'title':title[:240],'status':obj.get('status'),'updated_at':obj.get('updated_at')}
    if obj.get('location_reference'):result['artifact_reference']=obj['location_reference']
    if obj.get('version'):result['version']=obj['version']
    if obj.get('business_role'):result['purpose']=obj['business_role']
    return result

def resolve_focus(index,focus,diagnostics=None):
    selected={};unresolved=[]
    for ref in dict.fromkeys(focus or []):
        if ref in index:selected[ref]=index[ref]
        else:unresolved.append({'object_ref':ref,'reason':'requested record not resolved; unreadable canonical files may contain it' if diagnostics else 'requested record not found in this organization'})
    return selected,unresolved

def object_matches(obj,selector):
    s=normalize_selector(selector)
    if obj.get('object_type')!=s.get('type'): return False
    for k,v in s.items():
        if k=='type': continue
        if obj.get(k)!=v: return False
    return True
def refs_in_object(obj):
    """Relationships live in reference fields, never in arbitrary prose or filenames."""
    from validate_references import references_in
    return references_in(obj)
