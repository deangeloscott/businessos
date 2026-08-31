#!/usr/bin/env python3
from _common import *
import json,shutil
from generate_registry import main as generate_registry
from validate_workspace import main as validate_workspace
from process_plan import build_process_plan
from route_task import route
from init_business import init_business
from context_plan import build_plan
from validate_public_distribution import validate_public_distribution


def _validate_distribution_product_local():
    errors=[];inst=installation();installed=installed_modules();catalog=module_catalog()
    if 'core' not in installed:errors.append('core is not installed')
    present={'core'}|({p.name for p in (ROOT/'systems').iterdir() if p.is_dir()} if (ROOT/'systems').exists() else set())
    if installed!=present:errors.append(f'installed modules differ from filesystem: declared={sorted(installed)} present={sorted(present)}')
    for mid in installed:
        if mid not in catalog:errors.append(f'installed module missing from module catalog: {mid}')
        for dep in catalog.get(mid,{}).get('required_modules',[]):
            if dep not in installed:errors.append(f'{mid} missing required module {dep}')
    unexpected=[p.name for p in (ROOT/'instances').iterdir() if p.is_dir() and p.name!='_template'] if (ROOT/'instances').exists() else []
    if inst.get('standalone_distribution') and unexpected:errors.append(f'distribution includes business instances: {unexpected}')
    tpl=json.loads((ROOT/'instances/_template/instance.json').read_text());expected_enabled=sorted(installed-{'core'})
    if sorted(tpl.get('enabled_systems',[]))!=expected_enabled:errors.append('instance template enabled_systems does not match installed modules')

    generate_registry();validate_workspace();validate_public_distribution();reg={c['id']:c for c in load_registry()['contracts']}
    for cid,c in reg.items():
        for kind in ('required','conditional'):
            for item in (c.get('subcontracts') or {}).get(kind,[]) or []:
                rid=item.get('id') if isinstance(item,dict) else item
                if rid not in reg:errors.append(f'{cid} references unavailable subcontract {rid}')
    map_paths=[]
    if (ROOT/'core/process-map.json').exists():map_paths.append(ROOT/'core/process-map.json')
    map_paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for mp in map_paths:
        d=json.loads(mp.read_text())
        for a in d.get('activities',[]):
            try:build_process_plan(d['system'],a['id'])
            except Exception as e:errors.append(f"process plan {d['system']}/{a['id']}: {e}")
    for mid in sorted(installed-{'core'}):
        task=catalog[mid].get('smoke_task')
        if not task:continue
        rows=route(task,3)
        if not rows or rows[0].get('status')!='available' or rows[0].get('owner_system')!=mid:errors.append(f'route smoke failed for {mid}: {rows}')
    omitted=[m for m in catalog if m!='core' and m not in installed]
    if omitted:
        mid=omitted[0];rows=route(catalog[mid].get('smoke_task',''),3)
        if rows and rows[0].get('status')=='available' and rows[0].get('owner_system')==mid:errors.append(f'omitted module routed as available: {mid}')
    tid='distribution-smoke';dest=ROOT/'instances'/tid
    if dest.exists():shutil.rmtree(dest)
    try:
        init_business(tid,'Distribution Smoke Test');sample=next((c for c in reg.values() if c.get('owner_system')!='core'),None) or next(iter(reg.values()),None)
        if sample:
            plan=build_plan(tid,sample['id'])
            if inst.get('standalone_distribution'):
                defaults_rel='core/DEFAULTS.md'
                if defaults_rel not in plan.get('files',[]):errors.append('standalone context plan did not load Core defaults')
                else:
                    defaults=(ROOT/defaults_rel).read_text()
                    for phrase in [
                        'Installed modules are packages of AURA operational knowledge, not limits on what a capable human, model, or harness may do.',
                        'A missing module means its reusable AURA SOP knowledge is unavailable.',
                        'does **not** prohibit the active model/user from completing that work',
                        'An uninstalled optional module is never a hidden hard dependency.'
                    ]:
                        if phrase not in defaults:errors.append(f'Core defaults lost module-independence invariant: {phrase}')
    finally:
        if dest.exists():shutil.rmtree(dest)
    if errors:
        print(f'Distribution validation errors: {len(errors)}')
        for e in errors:print('ERROR',e)
        raise SystemExit(1)
    print(f"distribution validation passed: edition={inst.get('edition')} modules={','.join(sorted(installed))} contracts={len(reg)}")


def validate_distribution():
    prior=os.environ.get('BUSINESSOS_WORKSPACE');os.environ['BUSINESSOS_WORKSPACE']=str(PRODUCT_ROOT)
    try:_validate_distribution_product_local()
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior

if __name__=='__main__':validate_distribution()
