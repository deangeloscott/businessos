#!/usr/bin/env python3
from _common import *
import json,shutil
from generate_registry import main as generate_registry
from validate_workspace import main as validate_workspace
from process_plan import build_process_plan
from find_playbooks import find_candidates as find_playbook_candidates
from find_workflows import find_candidates as find_workflow_candidates
from operating_knowledge import installed_playbooks,get_playbook
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

    generate_registry();validate_workspace();validate_public_distribution();reg={c['id']:c for c in load_registry()['workflows']}
    for wid,workflow in reg.items():
        if workflow.get('type')!='workflow':errors.append(f'{wid} is not typed as Workflow')

    map_paths=[]
    if (ROOT/'core/process-map.json').exists():map_paths.append(ROOT/'core/process-map.json')
    map_paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for mp in map_paths:
        d=json.loads(mp.read_text())
        for a in d.get('activities',[]):
            try:build_process_plan(d['system'],a['id'])
            except Exception as e:errors.append(f"Workflow knowledge {d['system']}/{a['id']}: {e}")

    # Discovery is a bounded navigation aid, not semantic method selection.
    playbook_ids={p['id'] for p in installed_playbooks()}
    for mid in sorted(installed-{'core'}):
        task=catalog[mid].get('smoke_task')
        if not task:continue
        for row in find_playbook_candidates(task,5):
            if row.get('id') not in playbook_ids or not get_playbook(row.get('id')):errors.append(f'Playbook discovery returned unavailable Playbook for {mid}: {row}')
            if row.get('owner_system') not in installed:errors.append(f'Playbook discovery returned uninstalled owner for {mid}: {row}')
            if row.get('selection_authority') is not False:errors.append(f'Playbook discovery claimed semantic authority for {mid}: {row}')
        for row in find_workflow_candidates(task,5,mid):
            wid=row.get('workflow_id')
            if wid not in reg:errors.append(f'Workflow discovery returned unknown Workflow for {mid}: {row}')
            elif row.get('owner_system') not in installed:errors.append(f'Workflow discovery returned uninstalled owner for {mid}: {row}')
            if row.get('selection_authority') is not False:errors.append(f'Workflow discovery claimed semantic authority for {mid}: {row}')

    omitted=[m for m in catalog if m!='core' and m not in installed]
    if omitted:
        for mid in omitted[:3]:
            task=catalog[mid].get('smoke_task','')
            if any(row.get('owner_system')==mid for row in find_playbook_candidates(task,5)):errors.append(f'omitted module appeared as available Playbook: {mid}')
            if any(row.get('owner_system')==mid for row in find_workflow_candidates(task,5)):errors.append(f'omitted module appeared as available Workflow: {mid}')

    tid='distribution-smoke';dest=ROOT/'instances'/tid
    if dest.exists():shutil.rmtree(dest)
    try:
        init_business(tid,'Distribution Smoke Test');sample=next((c for c in reg.values() if c.get('owner_system')!='core'),None) or next(iter(reg.values()),None)
        if sample:
            plan=build_plan(tid,sample['id'])
            if 'CONTEXT.md' not in plan.get('files',[]):errors.append('context plan lost universal AURA agent context')
            for redundant in ('core/DEFAULTS.md','core/policies/agent-execution.md','core/policies/business-isolation.md','core/policies/preferences-and-adaptation.md'):
                if redundant in plan.get('files',[]):errors.append(f'context plan front-loaded redundant universal instruction: {redundant}')
            root_context=(ROOT/'CONTEXT.md').read_text()
            for phrase in [
                'AURA operating areas are bodies of operating knowledge, not limits on what the host may do.',
                'The model/user decides semantic applicability.',
                'AURA does not define a tool allowlist or universal capability vocabulary.',
            ]:
                if phrase not in root_context:errors.append(f'root AURA context lost method/tool-independence invariant: {phrase}')
    finally:
        if dest.exists():shutil.rmtree(dest)
    if errors:
        print(f'Distribution validation errors: {len(errors)}')
        for e in errors:print('ERROR',e)
        raise SystemExit(1)
    print(f"distribution validation passed: edition={inst.get('edition')} modules={','.join(sorted(installed))} workflows={len(reg)} playbooks={len(playbook_ids)}")


def validate_distribution():
    prior=os.environ.get('BUSINESSOS_WORKSPACE');os.environ['BUSINESSOS_WORKSPACE']=str(PRODUCT_ROOT)
    try:_validate_distribution_product_local()
    finally:
        if prior is None:os.environ.pop('BUSINESSOS_WORKSPACE',None)
        else:os.environ['BUSINESSOS_WORKSPACE']=prior

if __name__=='__main__':validate_distribution()