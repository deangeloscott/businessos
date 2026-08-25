#!/usr/bin/env python3
from _common import *
import shutil,argparse,json

def init_business(business_id,name):
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,63}',business_id):
        raise ValueError('business_id must be lowercase letters/numbers plus - or _')
    dest=ROOT/'instances'/business_id
    if dest.exists(): raise FileExistsError('Business already exists')
    shutil.copytree(ROOT/'instances/_template',dest)
    data=json.loads((dest/'instance.json').read_text());data.update({'business_id':business_id,'name':name,'created_at':now(),'enabled_systems':sorted(installed_modules()-{'core'})});(dest/'instance.json').write_text(json.dumps(data,indent=2)+'\n')
    rp=dest/'config/external-research-profile.json'
    if rp.exists():
        rpd=json.loads(rp.read_text());rpd['business_id']=business_id;rp.write_text(json.dumps(rpd,indent=2)+'\n')
    dirs=['context/brand','context/products','context/offers','context/audiences','context/markets','context/objectives','context/economics','context/constraints','context/preferences','intelligence/sources','intelligence/observations','intelligence/insights','intelligence/proof','decisions/opportunities','decisions/initiatives','operations/action-packets','operations/work-requests','operations/approvals','operations/change-events','operations/verifications','operations/incidents','operations/attention','intelligence/platform-changes','history/attention','history/platform-changes','assets','measurement/metric-definitions','measurement/metric-observations','measurement/experiments','measurement/outcome-evaluations','learning/business']
    for d in dirs:(dest/d).mkdir(parents=True,exist_ok=True)
    for sysid in data.get('enabled_systems',[]):
        (dest/'learning/domain'/sysid).mkdir(parents=True,exist_ok=True);(dest/'domains'/sysid).mkdir(parents=True,exist_ok=True)
    return dest

def main():
    p=argparse.ArgumentParser();p.add_argument('business_id');p.add_argument('--name',required=True);a=p.parse_args()
    try: dest=init_business(a.business_id,a.name)
    except (ValueError,FileExistsError) as e: raise SystemExit(str(e))
    print(dest)
    print(f'NEXT: run `python3 scripts/bootstrap_explicit_context.py {a.business_id} --help`. Preserve the full original request: if anything remains after setup, pass it with `--residual-request "<remaining natural-language request>"`; use `--initialization-only` only when setup/persistence was the entire request. Prefer relative runtime facts files + --source-text, then validate with `python3 scripts/validate_business.py {a.business_id} --require-context`. Do not create replacement BusinessOS scripts if a helper invocation fails.')
if __name__=='__main__':main()
