#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
import copy,hashlib,json,re,zipfile

IDENTIFYING_KEYS={'business_id','business_name','company_name','client_name','customer_name','domain','email','phone'}
FORBIDDEN_KEYS={'password','passwd','secret','client_secret','api_key','apikey','access_token','refresh_token','private_key','credential','credentials','session_cookie','cookie','auth_token'}

def schema_by_title(title):
    for p in schemas():
        try:d=json.loads(p.read_text())
        except Exception:continue
        if d.get('title')==title:return d
    raise ValueError(f'Unknown schema title: {title}')

def validate_schema(title,obj):
    errs=sorted(Draft202012Validator(schema_by_title(title)).iter_errors(obj),key=lambda e:list(e.path))
    if errs: raise ValueError('; '.join(f"{list(e.path)}: {e.message}" for e in errs))

def _version_tuple(value):
    try:
        parts=tuple(int(x) for x in str(value).split('.'))
        if len(parts)!=3: raise ValueError
        return parts
    except Exception: raise ValueError(f'Invalid semantic version: {value!r}')

def compatibility_status(compatibility,version=None,target_contract_id=None):
    version=_version_tuple(version or os_version()); compatibility=compatibility or {}; minv=compatibility.get('businessos_min'); maxv=compatibility.get('businessos_max')
    if minv and version<_version_tuple(minv): return 'incompatible'
    if maxv and version>_version_tuple(maxv): return 'incompatible'
    if target_contract_id:
        found=False
        for p in contract_files():
            try:m,_=read_frontmatter(p)
            except Exception:continue
            if m.get('id')==target_contract_id:found=True;break
        if not found:return 'review'
    return 'compatible'

def find_forbidden_keys(value,path=''):
    hits=[]
    if isinstance(value,dict):
        for k,v in value.items():
            kp=f'{path}.{k}' if path else str(k)
            if str(k).lower() in FORBIDDEN_KEYS:hits.append(kp)
            hits.extend(find_forbidden_keys(v,kp))
    elif isinstance(value,list):
        for i,v in enumerate(value):hits.extend(find_forbidden_keys(v,f'{path}[{i}]'))
    return hits

def find_identifying_keys(value,path=''):
    hits=[]
    if isinstance(value,dict):
        for k,v in value.items():
            kp=f'{path}.{k}' if path else str(k)
            if str(k).lower() in IDENTIFYING_KEYS:hits.append(kp)
            hits.extend(find_identifying_keys(v,kp))
    elif isinstance(value,list):
        for i,v in enumerate(value):hits.extend(find_identifying_keys(v,f'{path}[{i}]'))
    return hits

def canonical_hash(package):
    data=copy.deepcopy(package); data.setdefault('integrity',{})['content_hash']=None; raw=json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode(); return hashlib.sha256(raw).hexdigest()

def innovation_fingerprint(process):
    selected={k:process.get(k) for k in ['mode','owner_system','target_contract_id','local_contract_id','title','purpose','route_terms','reads','writes','required_capabilities','optional_capabilities','applies_when','does_not_apply_when','instructions','verification']}; raw=json.dumps(selected,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode(); return hashlib.sha256(raw).hexdigest()

def load_package(path):
    path=Path(path)
    if not path.exists():raise ValueError(f'Package not found: {path}')
    if path.suffix.lower()=='.zip':
        with zipfile.ZipFile(path,'r') as z:
            names=[n for n in z.namelist() if n.endswith('.json')]
            if 'innovation-package.json' in names:name='innovation-package.json'
            elif len(names)==1:name=names[0]
            else:raise ValueError('ZIP must contain innovation-package.json or exactly one JSON package')
            return json.loads(z.read(name).decode('utf-8'))
    return json.loads(path.read_text())

def validate_package(package,require_export_approval=False):
    validate_schema('InnovationPackage',package); hits=find_forbidden_keys(package)
    if hits:raise ValueError('InnovationPackage contains forbidden secret/credential field(s): '+', '.join(hits))
    if package.get('privacy',{}).get('raw_private_state_included') is not False:raise ValueError('raw_private_state_included must be false')
    if package.get('privacy',{}).get('secrets_included') is not False:raise ValueError('secrets_included must be false')
    if require_export_approval and not package.get('privacy',{}).get('user_approved_export'):raise ValueError('Package is a local draft and was not explicitly approved for export')
    expected=package.get('integrity',{}).get('content_hash')
    if expected and expected!=canonical_hash(package):raise ValueError('InnovationPackage integrity hash mismatch')
    return True

def bounded_summary(value,label):
    if value is None:return None
    if not isinstance(value,dict):raise ValueError(f'{label} must be a bounded JSON object')
    hits=find_forbidden_keys(value)
    if hits:raise ValueError(f'{label} contains forbidden secret/credential field(s): '+', '.join(hits))
    raw=json.dumps(value,ensure_ascii=False)
    if len(raw)>50000:raise ValueError(f'{label} is too large; provide a bounded summary rather than raw business state')
    return value
