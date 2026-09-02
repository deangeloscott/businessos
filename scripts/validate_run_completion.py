#!/usr/bin/env python3
"""Validate optional AURA work receipts without turning them into an execution gate."""
import json
from jsonschema import Draft202012Validator
from _common import *
from operating_knowledge import get_playbook

INTERNAL_MARKETING_ROLES={'internal_brief','internal_strategy','internal_analysis','internal_research','internal_planning'}
RETIRED_RUN_BACKLINK_FIELDS={'run_ref','run_id','run_method_type','run_method_ref','run_contract_id','run_binding','run_history_refs','contract_chain'}


def _workflows():
    out={}
    for path in contract_files():
        try:meta,_=read_frontmatter(path)
        except Exception:continue
        wid=meta.get('id')
        if isinstance(wid,str) and wid:out[wid]=meta
    return out


def _method_type(run):return run.get('method_type') or 'ad_hoc'


def _run_files_errors(business_id,workflows):
    errors=[];root=runtime_root()/'runs'/business_id
    if not root.exists():return errors
    schema=json.loads((PRODUCT_ROOT/'core/schemas/runtime/run.schema.json').read_text());registry=load_registry().get('contracts',[])
    for path in sorted(root.glob('*/run.json')):
        try:run=json.loads(path.read_text())
        except Exception as exc:errors.append(f'{storage_ref(path)} invalid Run JSON: {exc}');continue
        for error in Draft202012Validator(schema).iter_errors(run):errors.append(f'{storage_ref(path)} {list(error.path)}: {error.message}')
        if run.get('business_id')!=business_id:errors.append(f'{storage_ref(path)} business_id mismatch')
        directory=path.parent
        if (directory/'contract-execution.json').exists():errors.append(f'{storage_ref(directory)} contains retired contract-execution.json; Runs are receipts, not execution ledgers')
        method=_method_type(run);workflow_id=run.get('workflow_id');playbook_id=run.get('playbook_id');method_ref=run.get('method_ref')
        if 'contract_id' in run:errors.append(f'{storage_ref(path)} contains retired Run contract_id field; use workflow_id')
        if method=='aura_workflow':
            if not workflow_id or workflow_id not in workflows or workflows[workflow_id].get('type')!='workflow':errors.append(f'{storage_ref(path)} aura_workflow Run references unavailable Workflow {workflow_id!r}')
            if method_ref not in {None,workflow_id}:errors.append(f'{storage_ref(path)} aura_workflow method_ref must equal workflow_id')
            if playbook_id is not None:errors.append(f'{storage_ref(path)} Workflow-only Run must not claim playbook_id')
        elif method=='aura_playbook':
            if not playbook_id or not get_playbook(playbook_id,registry):errors.append(f'{storage_ref(path)} aura_playbook Run references unavailable Playbook {playbook_id!r}')
            if method_ref not in {None,playbook_id}:errors.append(f'{storage_ref(path)} aura_playbook method_ref must equal playbook_id')
            if workflow_id and (workflow_id not in workflows or workflows[workflow_id].get('type')!='workflow'):errors.append(f'{storage_ref(path)} Playbook Run references unavailable supporting Workflow {workflow_id!r}')
        elif workflow_id is not None or playbook_id is not None:errors.append(f'{storage_ref(path)} non-AURA Run must not claim AURA Playbook/Workflow identifiers')
        continuity=run.get('continuity') if isinstance(run.get('continuity'),dict) else {}
        if not continuity:continue
        if continuity.get('purpose')!='organizational_work_receipt':errors.append(f'{storage_ref(path)} continuity purpose is not organizational_work_receipt')
        if continuity.get('method_type') and continuity.get('method_type')!=method:errors.append(f'{storage_ref(path)} continuity method_type does not match Run method_type')
        if run.get('status')=='completed' and continuity.get('state')!='completed':errors.append(f'{storage_ref(path)} completed Run must have continuity.state=completed')
        for key in ('evidence_refs','result_refs','decision_refs'):
            for ref in continuity.get(key) or []:
                try:target=resolve_storage_ref(ref)
                except Exception:errors.append(f'{storage_ref(path)} continuity {key} contains invalid ref {ref!r}');continue
                if not target.exists() or not target.is_file():errors.append(f'{storage_ref(path)} continuity {key} does not resolve: {ref}')
    return errors


def _canonical_backlink_errors(objects):
    errors=[]
    for obj,path in objects:
        ext=obj.get('extensions') if isinstance(obj.get('extensions'),dict) else {};bos=ext.get('businessos') if isinstance(ext.get('businessos'),dict) else {};retired=sorted(RETIRED_RUN_BACKLINK_FIELDS & set(bos))
        if retired:errors.append(f'{path} contains retired canonical-to-Run backlink fields {retired}; optional receipts reference durable results one-way')
        if obj.get('object_type')=='Asset' and obj.get('owner_system')=='marketing-synthesis' and bos.get('customer_facing',True) is False:
            role=str(obj.get('business_role') or '').strip().lower()
            if role not in INTERNAL_MARKETING_ROLES:errors.append(f'{path} marketing-synthesis Asset may set customer_facing=false only for an explicitly internal support role ({", ".join(sorted(INTERNAL_MARKETING_ROLES))}); an unpublished customer-facing draft remains customer-facing by intended use')
    return errors


def run_completion_errors(business_id,objects):
    workflows=_workflows();return [*_run_files_errors(business_id,workflows),*_canonical_backlink_errors(objects)]
