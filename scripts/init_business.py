#!/usr/bin/env python3
from _common import *
from canonical_store import INSTANCE_PATHS,validate_canonical,write_canonical
import shutil,argparse,json,hashlib


def _ensure_canonical_dirs(dest):
    """Create the canonical organization-state directories from one source of truth."""
    for rel in sorted(set(INSTANCE_PATHS.values())):
        path=dest/rel
        (path.parent if path.suffix.lower()=='.json' else path).mkdir(parents=True,exist_ok=True)
    # These are archive views for lifecycle helpers, not canonical object types.
    for rel in ('history/attention','history/platform-changes'):
        (dest/rel).mkdir(parents=True,exist_ok=True)


def _persist_minimal_identity(business_id,name,ts):
    """Persist the smallest truthful canonical organization identity.

    Initialization should not require invented industry/service/objective facts. The
    supplied organization name is enough to establish a Business; everything else
    remains unknown until the model/user discovers or supplies it.
    """
    source_id=f'src_{business_id}_initial_identity'
    source={
        'id':source_id,'object_type':'SourceRecord','schema_version':'1.0.0','business_id':business_id,
        'created_at':ts,'updated_at':ts,'lineage':[],'source_type':'organization_initialization_input',
        'source_reference':'organization name supplied at AURA initialization','origin':'initialization input',
        'retrieved_at':ts,'published_at':None,'content_hash':'sha256:'+hashlib.sha256(name.encode('utf-8')).hexdigest(),
        'access_scope':'business-private','extensions':{'businessos':{'captured_name':name,'source_kind':'explicit_initialization_input'}},
    }
    business={
        'id':f'biz_{business_id}','object_type':'Business','schema_version':'1.0.0','business_id':business_id,
        'created_at':ts,'updated_at':ts,'lineage':[source_id],'name':name,
        'extensions':{'businessos':{'source_ref':source_id,'source_kind':'explicit_initialization_input'}},
    }
    validate_canonical('SourceRecord',source);validate_canonical('Business',business)
    write_canonical(source);write_canonical(business)
    return source,business


def init_business(business_id,name):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',business_id):
        raise ValueError('business_id must be lowercase letters/numbers plus - or _')
    name=str(name).strip()
    if not name:raise ValueError('name must not be empty')
    dest=instance_dir(business_id)
    if dest.exists(): raise FileExistsError('Business already exists')
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(product_instance_template(),dest)
    ts=now();data=json.loads((dest/'instance.json').read_text())
    data.update({'business_id':business_id,'name':name,'created_at':ts,'enabled_systems':sorted(installed_modules()-{'core'})})
    write_json_atomic(dest/'instance.json',data)
    rp=dest/'config/external-research-profile.json'
    if rp.exists():
        rpd=json.loads(rp.read_text());rpd['business_id']=business_id;write_json_atomic(rp,rpd)
    _ensure_canonical_dirs(dest)
    _persist_minimal_identity(business_id,name,ts)
    return dest


def main():
    p=argparse.ArgumentParser(description='Initialize one AURA-managed organization from its stable ID and name. The name alone is sufficient canonical context; all other facts remain unknown until supplied or discovered.')
    p.add_argument('business_id');p.add_argument('--name',required=True);a=p.parse_args()
    try: dest=init_business(a.business_id,a.name)
    except (ValueError,FileExistsError) as e: raise SystemExit(str(e))
    print(dest)
    print(f'Initialized canonical organization identity for {a.name!r}. Validate with `python3 scripts/validate_business.py {a.business_id} --require-context`. Add more grounded context later only when it is useful; do not invent facts to satisfy setup.')


if __name__=='__main__':main()
