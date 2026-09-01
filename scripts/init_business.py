#!/usr/bin/env python3
from _common import *
from canonical_store import INSTANCE_PATHS
import shutil,argparse,json


def _ensure_canonical_dirs(dest):
    """Create the canonical organization-state directories from one source of truth."""
    for rel in sorted(set(INSTANCE_PATHS.values())):
        path=dest/rel
        (path.parent if path.suffix.lower()=='.json' else path).mkdir(parents=True,exist_ok=True)
    # These are archive views for lifecycle helpers, not canonical object types.
    for rel in ('history/attention','history/platform-changes'):
        (dest/rel).mkdir(parents=True,exist_ok=True)


def init_business(business_id,name):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',business_id):
        raise ValueError('business_id must be lowercase letters/numbers plus - or _')
    dest=instance_dir(business_id)
    if dest.exists(): raise FileExistsError('Business already exists')
    dest.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(product_instance_template(),dest)
    data=json.loads((dest/'instance.json').read_text())
    data.update({'business_id':business_id,'name':name,'created_at':now(),'enabled_systems':sorted(installed_modules()-{'core'})})
    (dest/'instance.json').write_text(json.dumps(data,indent=2)+'\n')
    rp=dest/'config/external-research-profile.json'
    if rp.exists():
        rpd=json.loads(rp.read_text());rpd['business_id']=business_id;rp.write_text(json.dumps(rpd,indent=2)+'\n')
    _ensure_canonical_dirs(dest)
    return dest


def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');p.add_argument('--name',required=True);a=p.parse_args()
    try: dest=init_business(a.business_id,a.name)
    except (ValueError,FileExistsError) as e: raise SystemExit(str(e))
    print(dest)
    print(f'NEXT: run `python3 scripts/bootstrap_explicit_context.py {a.business_id} --help`. Preserve the full original request: if anything remains after setup, pass it with `--residual-request "<remaining natural-language request>"`; use `--initialization-only` only when setup/persistence was the entire request. Prefer relative runtime facts files + --source-text, then validate with `python3 scripts/validate_business.py {a.business_id} --require-context`. Do not create replacement AURA scripts if a helper invocation fails.')


if __name__=='__main__':main()
