#!/usr/bin/env python3
"""One-time migration for the Playbook → Workflow semantic refactor.

This changes vocabulary and metadata without changing the underlying business methods:
- detailed authored procedures become Workflows;
- high-level Playbooks remain separate end-to-end jobs;
- `subcontracts` becomes plain Workflow composition metadata;
- the invented AURA capability vocabulary is removed;
- organization-local process knowledge/evolution state is migrated to Workflow terms;
- old receipt/proposal compatibility fields are translated once instead of living forever.

The migration does not infer new business facts or rewrite substantive domain methodology.
It is safe to inspect first with --dry-run.
"""
from pathlib import Path
import argparse,json,os,shutil
import yaml
from _common import ROOT,contract_files,read_frontmatter,runtime_root

RETIRE_PATHS=[
    'core/capabilities/catalog.json','docs/adding-a-capability.md',
    'generated/capability-usage-index.json','generated/playbook-candidate-index.json',
    'PLAYBOOK-INDEX.md','core/schemas/learning/playbook-evolution-proposal.schema.json',
    'scripts/persist_playbook_evolution.py','core/policies/playbook-evolution.md',
    'docs/contract-authoring.md','docs/adding-a-contract.md',
]
OLD_EVOLUTION_ID='core.learning.playbook-evolution'
NEW_EVOLUTION_ID='core.learning.workflow-evolution'

BODY_REPLACEMENTS=[
    (OLD_EVOLUTION_ID,NEW_EVOLUTION_ID),
    ('PlaybookEvolutionProposal','WorkflowEvolutionProposal'),
    ('persist_playbook_evolution.py','persist_workflow_evolution.py'),
    ('this AURA playbook','this AURA Workflow'),('This AURA playbook','This AURA Workflow'),
    ('the AURA playbook','the AURA Workflow'),('The AURA playbook','The AURA Workflow'),
    ('AURA playbook method','AURA Workflow method'),('AURA playbook knowledge','AURA Workflow knowledge'),
    ('provider-neutral capability needs','the tools or resources appropriate to the work'),
    ('provider-neutral capability need','the tools or resources appropriate to the work'),
    ('subcontract-completion ledger','Workflow-composition metadata'),
    ('subcontract completion ledger','Workflow-composition metadata'),
    ('subcontract ledger','Workflow-composition metadata'),
    ('subcontract execution ledger','Workflow-composition metadata'),
]


def render(meta,body):
    front=yaml.safe_dump(meta,sort_keys=False,width=1000).rstrip();return '---\n'+front+'\n---\n'+body.lstrip('\n')
def _replace_body(body):
    for old,new in BODY_REPLACEMENTS:body=body.replace(old,new)
    return body
def _write_json(path,obj,dry_run):
    if dry_run:return
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8');os.replace(tmp,path)
def _replace_exact(value,mapping):
    if isinstance(value,str):return mapping.get(value,value)
    if isinstance(value,list):return [_replace_exact(item,mapping) for item in value]
    if isinstance(value,dict):return {key:_replace_exact(item,mapping) for key,item in value.items()}
    return value


def _migrate_contracts(dry_run):
    changed=[];retyped=0;capability_blocks=0;composition_blocks=0;body_changes=0
    for path in list(contract_files()):
        meta,body=read_frontmatter(path);dirty=False
        if meta.get('type')=='playbook':meta['type']='workflow';retyped+=1;dirty=True
        if 'capabilities' in meta:meta.pop('capabilities',None);capability_blocks+=1;dirty=True
        if 'subcontracts' in meta:
            existing=meta.pop('subcontracts') or {};current=meta.get('workflows') or {};merged={}
            for kind in ('required','conditional'):
                values=[]
                for source in (current.get(kind) or [],existing.get(kind) or []):
                    if isinstance(source,list):
                        for item in source:
                            if item not in values:values.append(item)
                if values:merged[kind]=values
            if merged:meta['workflows']=merged
            composition_blocks+=1;dirty=True
        migrated_meta=_replace_exact(meta,{OLD_EVOLUTION_ID:NEW_EVOLUTION_ID})
        if migrated_meta!=meta:meta=migrated_meta;dirty=True
        new_body=_replace_body(body)
        if new_body!=body:body_changes+=1;dirty=True;body=new_body
        if meta.get('id')==OLD_EVOLUTION_ID:meta['id']=NEW_EVOLUTION_ID;dirty=True
        reads=['WorkflowEvolutionProposal' if x=='PlaybookEvolutionProposal' else x for x in meta.get('reads',[])]
        writes=['WorkflowEvolutionProposal' if x=='PlaybookEvolutionProposal' else x for x in meta.get('writes',[])]
        if reads!=meta.get('reads',[]):meta['reads']=reads;dirty=True
        if writes!=meta.get('writes',[]):meta['writes']=writes;dirty=True
        if dirty:
            changed.append(str(path.relative_to(ROOT)))
            if not dry_run:path.write_text(render(meta,body),encoding='utf-8')
    old=ROOT/'core/contracts/learning/playbook-evolution';new=ROOT/'core/contracts/learning/workflow-evolution'
    if old.exists():
        if not dry_run:
            if new.exists():shutil.rmtree(new)
            new.parent.mkdir(parents=True,exist_ok=True);old.rename(new)
        changed.append('core/contracts/learning/playbook-evolution -> workflow-evolution')
    return changed,retyped,capability_blocks,composition_blocks,body_changes


def _migrate_process_maps(dry_run):
    count=0;paths=[];core=ROOT/'core/process-map.json'
    if core.exists():paths.append(core)
    paths+=sorted((ROOT/'systems').glob('*/process-map.json'))
    for path in paths:
        data=json.loads(path.read_text(encoding='utf-8'));before=json.dumps(data,sort_keys=True)
        for activity in data.get('activities',[]):
            if activity.get('entry_contract')==OLD_EVOLUTION_ID:activity['entry_contract']=NEW_EVOLUTION_ID
            if 'supporting_contracts' in activity:activity['supporting_workflows']=activity.pop('supporting_contracts')
            activity['supporting_workflows']=[NEW_EVOLUTION_ID if x==OLD_EVOLUTION_ID else x for x in activity.get('supporting_workflows',[])]
        if json.dumps(data,sort_keys=True)!=before:
            count+=1
            if not dry_run:path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return count


def _proposal_id_map(paths):
    mapping={}
    for path in paths:
        try:obj=json.loads(path.read_text(encoding='utf-8'))
        except Exception:continue
        if not isinstance(obj,dict) or obj.get('object_type')!='PlaybookEvolutionProposal':continue
        old=str(obj.get('id') or '')
        if old.startswith('pev_'):mapping[old]='wev_'+old[4:]
    return mapping


def _migrate_instance_state(dry_run):
    root=ROOT/'instances'
    if not root.exists():return 0,0
    paths=sorted(root.glob('*/**/*.json'));id_map=_proposal_id_map(paths);changed=0;renamed=0
    for path in paths:
        try:obj=json.loads(path.read_text(encoding='utf-8'))
        except Exception:continue
        if not isinstance(obj,dict):continue
        before=json.dumps(obj,sort_keys=True);typ=obj.get('object_type')
        if typ=='ProcessExtension':
            if obj.get('mode')=='augment_contract':obj['mode']='augment_workflow'
            if obj.get('mode')=='local_playbook':obj['mode']='local_workflow'
            if 'target_contract_id' in obj:obj['target_workflow_id']=obj.pop('target_contract_id')
            if 'local_contract_id' in obj:obj['local_workflow_id']=obj.pop('local_contract_id')
            for key in ('required_capabilities','optional_capabilities'):obj.pop(key,None)
            ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {}
            if 'playbook_evolution_proposal_ref' in ext:ext['workflow_evolution_proposal_ref']=ext.pop('playbook_evolution_proposal_ref');obj['extensions']=ext
        elif typ in {'PlaybookEvolutionProposal','WorkflowEvolutionProposal'}:
            obj['object_type']='WorkflowEvolutionProposal'
            old_id=str(obj.get('id') or '');obj['id']=id_map.get(old_id,old_id)
            if obj.get('change_kind')=='new_local_playbook':obj['change_kind']='new_local_workflow'
            if 'target_contract_id' in obj:obj['target_workflow_id']=obj.pop('target_contract_id')
            if 'proposed_local_contract_id' in obj:obj['proposed_local_workflow_id']=obj.pop('proposed_local_contract_id')
            for key in ('required_capabilities','optional_capabilities'):obj.pop(key,None)
        obj=_replace_exact(obj,id_map)
        if json.dumps(obj,sort_keys=True)==before:continue
        changed+=1;target=path
        old_name=path.stem;new_id=str(obj.get('id') or '')
        if old_name in id_map and new_id==id_map[old_name]:target=path.with_name(new_id+'.json');renamed+=1
        if not dry_run:
            if target!=path and target.exists():raise RuntimeError(f'Workflow evolution migration target already exists: {target}')
            _write_json(target,obj,False)
            if target!=path:path.unlink()
    return changed,renamed


def _migrate_run_receipts(dry_run):
    root=runtime_root()/'runs'
    if not root.exists():return 0
    changed=0
    for path in sorted(root.glob('*/*/run.json')):
        try:run=json.loads(path.read_text(encoding='utf-8'))
        except Exception:continue
        if not isinstance(run,dict):continue
        before=json.dumps(run,sort_keys=True);old_workflow=run.pop('contract_id',None)
        if old_workflow and not run.get('workflow_id'):run['workflow_id']=old_workflow
        method=run.get('method_type');playbook_id=run.get('playbook_id');workflow_id=run.get('workflow_id')
        if method=='aura_playbook' and not playbook_id and workflow_id:
            run['method_type']='aura_workflow';run['method_ref']=workflow_id
            continuity=run.get('continuity')
            if isinstance(continuity,dict):continuity['method_type']='aura_workflow';continuity['method_ref']=workflow_id
        if json.dumps(run,sort_keys=True)!=before:
            changed+=1;_write_json(path,run,dry_run)
    return changed


def _retire_files(dry_run):
    removed=[]
    for rel in RETIRE_PATHS:
        path=ROOT/rel
        if path.exists():
            removed.append(rel)
            if not dry_run:
                if path.is_dir():shutil.rmtree(path)
                else:path.unlink()
    return removed


def migrate(dry_run=False):
    changed,retyped,capability_blocks,composition_blocks,body_changes=_migrate_contracts(dry_run)
    maps=_migrate_process_maps(dry_run);state,state_renames=_migrate_instance_state(dry_run);runs=_migrate_run_receipts(dry_run);removed=_retire_files(dry_run)
    return {
        'changed_workflow_files':len(changed),'retyped_playbook_metadata':retyped,
        'removed_capability_blocks':capability_blocks,'renamed_composition_blocks':composition_blocks,
        'workflow_body_term_updates':body_changes,'process_maps_updated':maps,
        'organization_state_objects_migrated':state,'workflow_evolution_ids_renamed':state_renames,
        'run_receipts_migrated':runs,'retired_files':removed,'dry_run':dry_run,
    }


def main():
    p=argparse.ArgumentParser(description='Apply the AURA Playbook → Workflow semantic migration and retire the invented capability vocabulary.');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    try:result=migrate(a.dry_run)
    except RuntimeError as exc:raise SystemExit(str(exc))
    for key,value in result.items():print(f'{key}: {value}')

if __name__=='__main__':main()
