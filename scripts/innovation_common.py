#!/usr/bin/env python3
from _common import *
from jsonschema import Draft202012Validator
import copy,hashlib,json,re,zipfile

IDENTIFYING_KEYS={'business_id','business_name','company_name','client_name','customer_name','domain','email','phone'}
FORBIDDEN_KEYS={'password','passwd','secret','client_secret','api_key','apikey','access_token','refresh_token','private_key','credential','credentials','session_cookie','cookie','auth_token'}

def schema_by_title(title):
    for path in schemas():
        try:data=json.loads(path.read_text())
        except Exception:continue
        if data.get('title')==title:return data
    raise ValueError(f'Unknown schema title: {title}')
def validate_schema(title,obj):
    errors=sorted(Draft202012Validator(schema_by_title(title)).iter_errors(obj),key=lambda error:list(error.path))
    if errors:raise ValueError('; '.join(f"{list(error.path)}: {error.message}" for error in errors))
def _version_tuple(value):
    try:
        parts=tuple(int(x) for x in str(value).split('.'))
        if len(parts)!=3:raise ValueError
        return parts
    except Exception:raise ValueError(f'Invalid semantic version: {value!r}')
def compatibility_status(compatibility,version=None,target_contract_id=None):
    version=_version_tuple(version or os_version());compatibility=compatibility or {};minimum=compatibility.get('aura_min');maximum=compatibility.get('aura_max')
    if minimum and version<_version_tuple(minimum):return 'incompatible'
    if maximum and version>_version_tuple(maximum):return 'incompatible'
    if target_contract_id:
        found=False
        for path in contract_files():
            try:meta,_=read_frontmatter(path)
            except Exception:continue
            if meta.get('id')==target_contract_id and meta.get('type')=='workflow':found=True;break
        if not found:return 'review'
    return 'compatible'
def innovation_support_root(business_id):return instance_dir(business_id)/'support'/'innovation-exchange'
def innovation_package_dir(business_id):return innovation_support_root(business_id)/'packages'
def innovation_entry_dir(business_id):return innovation_support_root(business_id)/'entries'
def innovation_entry_path(business_id,entry_id):return innovation_entry_dir(business_id)/f'{entry_id}.json'
def iter_innovation_entries(business_id):
    root=innovation_entry_dir(business_id)
    if not root.exists():return []
    rows=[]
    for path in sorted(root.glob('iex_*.json')):
        try:data=json.loads(path.read_text())
        except Exception:continue
        if isinstance(data,dict) and data.get('business_id')==business_id:rows.append((data,path))
    return rows
def find_forbidden_keys(value,path=''):
    hits=[]
    if isinstance(value,dict):
        for key,item in value.items():
            current=f'{path}.{key}' if path else str(key)
            if str(key).lower() in FORBIDDEN_KEYS:hits.append(current)
            hits.extend(find_forbidden_keys(item,current))
    elif isinstance(value,list):
        for index,item in enumerate(value):hits.extend(find_forbidden_keys(item,f'{path}[{index}]'))
    return hits
def find_identifying_keys(value,path=''):
    hits=[]
    if isinstance(value,dict):
        for key,item in value.items():
            current=f'{path}.{key}' if path else str(key)
            if str(key).lower() in IDENTIFYING_KEYS:hits.append(current)
            hits.extend(find_identifying_keys(item,current))
    elif isinstance(value,list):
        for index,item in enumerate(value):hits.extend(find_identifying_keys(item,f'{path}[{index}]'))
    return hits
def canonical_hash(package):
    data=copy.deepcopy(package);data.setdefault('integrity',{})['content_hash']=None;raw=json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();return hashlib.sha256(raw).hexdigest()
def innovation_fingerprint(process):
    selected={key:process.get(key) for key in ['mode','owner_system','target_contract_id','local_contract_id','title','purpose','discovery_terms','reads','writes','applies_when','does_not_apply_when','instructions','verification']};raw=json.dumps(selected,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();return hashlib.sha256(raw).hexdigest()
def load_package(path):
    path=Path(path)
    if not path.exists():raise ValueError(f'Package not found: {path}')
    if path.suffix.lower()=='.zip':
        with zipfile.ZipFile(path,'r') as archive:
            names=[name for name in archive.namelist() if name.endswith('.json')]
            if 'innovation-package.json' in names:name='innovation-package.json'
            elif len(names)==1:name=names[0]
            else:raise ValueError('ZIP must contain innovation-package.json or exactly one JSON package')
            return json.loads(archive.read(name).decode('utf-8'))
    return json.loads(path.read_text())
def validate_package(package,require_export_approval=False):
    validate_schema('InnovationPackage',package);hits=find_forbidden_keys(package)
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
