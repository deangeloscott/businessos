#!/usr/bin/env python3
"""Prepare bounded organizational context without turning AURA into an execution controller.

Entry resolves the organization, retrieves useful durable context, and may recommend an
AURA playbook. It does not create a Run, inspect host capabilities, check schedulers,
calculate permissions, or require work to use an AURA contract. The active model/user
chooses the method and the harness supplies its real execution capabilities.
"""
from pathlib import Path
import argparse, json, os

from _common import PRODUCT_ROOT, workspace_root, resolve_business, object_index, storage_ref
from route_and_resolve import route_and_resolve
from context_plan import build_plan
from process_plan import build_process_plan

METHOD_TYPES=['aura_playbook','external_skill','model_created','ad_hoc']
BASELINE_TYPES=['Business','Brand','ProductService','Offer','AudienceSegment','Market','Objective','DecisionRecord','Learning']


def _contract(contract_id):
    if not contract_id:return None
    return next((row for row in json.loads((PRODUCT_ROOT/'generated/contract-registry.json').read_text()).get('contracts',[]) if row.get('id')==contract_id),None)


def _baseline_context(business_id,limit_per_type=3):
    """Return a small current organization-owned context set when no SOP drives retrieval."""
    idx=object_index(business_id);rows=[]
    by_type={typ:[] for typ in BASELINE_TYPES}
    for oid,(obj,path) in idx.items():
        typ=obj.get('object_type')
        if typ not in by_type or obj.get('status') in {'archived','superseded'}:continue
        by_type[typ].append((obj,path))
    for typ in BASELINE_TYPES:
        candidates=sorted(by_type[typ],key=lambda x:(x[0].get('updated_at') or x[0].get('created_at') or '',x[0].get('id') or ''),reverse=True)
        for obj,path in candidates[:limit_per_type]:
            rows.append({'object_ref':obj.get('id'),'object_type':typ,'path':storage_ref(path)})
    return rows


def _recommendation(task,business_id,operator_ref=None,team_ref=None,role_ref=None,selected_contract_id=None):
    if selected_contract_id:
        contract=_contract(selected_contract_id)
        if not contract:raise ValueError(f'Unknown AURA playbook: {selected_contract_id}')
        return {
            'contract_id':contract['id'],'owner_system':contract.get('owner_system'),'path':contract.get('path'),
            'reason':'Explicitly selected AURA playbook.','selection_mode':'explicit','status':'available'
        }
    try:return route_and_resolve(task,business_id,team_ref,role_ref,operator_ref,None)
    except ValueError as exc:
        return {'status':'unavailable','reason':str(exc)}


def _playbook_context(business_id,contract_id,focus,operator_ref,team_ref,role_ref,task_preferences,output_type,channel):
    if not contract_id:return None,None
    try:
        context=build_plan(
            business_id,contract_id,focus=focus,operator_ref=operator_ref,team_ref=team_ref,
            role_ref=role_ref,task_preferences=task_preferences,output_type=output_type,channel=channel,
        )
        process=build_process_plan(contract_id)
        return context,process
    except ValueError as exc:
        return {'error':str(exc)},None


def prepare_work(task,business_id=None,workspace=None,focus=None,operator_ref=None,team_ref=None,role_ref=None,task_preferences=None,output_type=None,channel=None,selected_contract_id=None):
    task=(task or '').strip()
    if not task:return {'format_version':'2.0','status':'needs_input','missing':['request']}
    if workspace:os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':
        return {'format_version':'2.0','status':'needs_input','workspace':str(workspace_root()),**{k:v for k,v in resolved.items() if k!='status'}}
    bid=resolved['business_id'];focus=focus or []
    route=_recommendation(task,bid,operator_ref,team_ref,role_ref,selected_contract_id)

    recommended_id=None
    if route.get('status')=='available' and not route.get('semantic_selection_required'):
        recommended_id=route.get('contract_id')
    context,process=_playbook_context(bid,recommended_id,focus,operator_ref,team_ref,role_ref,task_preferences,output_type,channel)
    baseline=_baseline_context(bid)

    if context and not context.get('error'):
        object_context=[{'object_ref':oid,'path':path} for oid,path in zip(context.get('object_refs',[]),context.get('object_files',[]))]
        context_files=context.get('files',[])
        capabilities={
            'required':context.get('required_capabilities',[]),
            'optional':context.get('optional_capabilities',[]),
            'rule':'These are provider-neutral needs of the recommended AURA playbook only. The active harness determines actual tools, providers, permissions, fallbacks, and availability.'
        }
    else:
        object_context=[];context_files=['CONTEXT.md','core/DEFAULTS.md']
        capabilities={'required':[],'optional':[],'rule':'No AURA playbook has been selected; use the active harness capabilities normally.'}

    recommendation={
        'contract_id':recommended_id,
        'owner_system':route.get('owner_system'),
        'path':route.get('path'),
        'reason':route.get('reason'),
        'selection_mode':route.get('selection_mode'),
        'status':'recommended' if recommended_id else 'none',
        'rule':'A recommendation is operational knowledge, not authority. The model/user may use it, adapt it, or choose an external Skill, model-created method, or ad-hoc method.'
    }
    if route.get('semantic_selection_required'):
        recommendation.update({'status':'model_judgment','candidates':route.get('candidates') or route.get('candidate_contracts') or []})

    return {
        'format_version':'2.0','status':'ready','workspace':str(workspace_root()),
        'business_id':bid,'business_resolution':resolved.get('resolution'),'original_request':task,
        'retrieval':{
            'baseline_context':baseline,
            'playbook_context':object_context,
            'context_files':context_files,
            'unresolved_selectors':(context or {}).get('unresolved_selectors',[]) if isinstance(context,dict) else [],
            'rule':'Load only what materially helps the request. Absence from retrieved AURA context means AURA has no selected durable record, not that the real-world fact does not exist.'
        },
        'recommended_playbook':recommendation,
        'playbook_process':process if recommended_id else None,
        'capability_requirements':capabilities,
        'method_options':METHOD_TYPES,
        'run':{
            'created':False,
            'rule':'Do not create a Run merely to begin reasoning. Create a bounded work receipt when continuity/persistence is useful, using the method actually chosen.'
        },
        'next':{
            'work':'Use the active model/harness normally with the retrieved organizational context.',
            'aura_playbook_run':f'python3 scripts/create_run.py {bid} "{task}" --contract-id <selected-playbook-id>',
            'other_method_run':f'python3 scripts/create_run.py {bid} "{task}" --method-type <external_skill|model_created|ad_hoc> [--method-ref <name>]',
            'persistence':'When material organizational meaning is produced, persist it through supported canonical helpers and complete the work receipt with its evidence/results/decisions/unresolved work.',
        },
        'persistence_test':'Would a capable future model working for this organization materially benefit from knowing this after the current session/runtime is gone?',
        'rule':'AURA prepares organizational memory and operational knowledge; it does not decide whether the harness is allowed or able to execute the work.'
    }


def main():
    p=argparse.ArgumentParser(description='Resolve organization context and optional AURA playbook guidance without creating an execution-control envelope.')
    p.add_argument('task');p.add_argument('--business-id');p.add_argument('--workspace');p.add_argument('--focus',action='append',default=[])
    p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref');p.add_argument('--task-preferences')
    p.add_argument('--output-type');p.add_argument('--channel');p.add_argument('--selected-contract')
    a=p.parse_args()
    try:result=prepare_work(a.task,a.business_id,a.workspace,a.focus,a.operator_ref,a.team_ref,a.role_ref,a.task_preferences,a.output_type,a.channel,a.selected_contract)
    except (ValueError,json.JSONDecodeError) as exc:result={'format_version':'2.0','status':'needs_judgment','reason':str(exc)}
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(0 if result.get('status')=='ready' else 2)


if __name__=='__main__':main()
