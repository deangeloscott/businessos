#!/usr/bin/env python3
"""Prepare bounded organizational context and operating-knowledge candidates.

Entry resolves the organization, retrieves useful durable context, and surfaces a small
set of high-level Playbooks plus detailed Workflow candidates. It does not semantically
route the request, choose tools/providers, create a Run, inspect host tools, or control
execution. The active model/user chooses the method and the harness supplies its real
tools, Skills, orchestration, and execution environment.
"""
from pathlib import Path
import argparse,json,os

from _common import workspace_root,resolve_business,object_index,storage_ref,load_registry
from find_playbooks import find_candidates as find_playbook_candidates
from find_workflows import find_candidates as find_workflow_candidates
from operating_knowledge import get_playbook
from process_extensions import local_workflow_candidates,resolve_effective
from context_plan import build_plan
from process_plan import build_process_plan

METHOD_TYPES=['aura_playbook','aura_workflow','external_skill','model_created','ad_hoc']
BASELINE_TYPES=['Business','Brand','ProductService','Offer','AudienceSegment','Market','Objective','DecisionRecord','Learning']


def _baseline_context(business_id,limit_per_type=3):
    idx=object_index(business_id);rows=[];by_type={typ:[] for typ in BASELINE_TYPES}
    for _,(obj,path) in idx.items():
        typ=obj.get('object_type')
        if typ not in by_type or obj.get('status') in {'archived','superseded'}:continue
        by_type[typ].append((obj,path))
    for typ in BASELINE_TYPES:
        candidates=sorted(by_type[typ],key=lambda x:(x[0].get('updated_at') or x[0].get('created_at') or '',x[0].get('id') or ''),reverse=True)
        for obj,path in candidates[:limit_per_type]:rows.append({'object_ref':obj.get('id'),'object_type':typ,'path':storage_ref(path)})
    return rows


def _workflow_candidates(task,business_id,owner_system=None,team_ref=None,role_ref=None,operator_ref=None,top=6):
    rows=[];seen=set()
    for local in local_workflow_candidates(task,business_id,team_ref,role_ref,operator_ref,top):
        wid=local.get('workflow_id')
        if not wid:continue
        if owner_system and local.get('owner_system')!=owner_system:continue
        rows.append(local);seen.add(wid)
    for row in find_workflow_candidates(task,top,owner_system):
        wid=row.get('workflow_id')
        if not wid or wid in seen:continue
        rows.append(row);seen.add(wid)
        if len(rows)>=top:break
    return rows[:top]


def _selected_workflow(task,business_id,workflow_id,team_ref=None,role_ref=None,operator_ref=None):
    path,meta,_,extensions=resolve_effective(workflow_id,business_id,team_ref,role_ref,operator_ref)
    return {'task':task,'workflow_id':workflow_id,'owner_system':meta.get('owner_system'),'status':'available','reason':'explicitly selected by the active model/user after semantic judgment','path':str(path.relative_to(Path(__file__).resolve().parents[1])) if path else None,'process_extension_ids':[item['id'] for item in extensions],'local_workflow':bool(meta.get('local_workflow')),'selection_mode':'explicit_model_selection','semantic_selection_required':False}


def _workflow_context(business_id,workflow_id,focus,operator_ref,team_ref,role_ref,task_preferences,output_type,channel):
    if not workflow_id:return None,None
    try:return build_plan(business_id,workflow_id,focus=focus,operator_ref=operator_ref,team_ref=team_ref,role_ref=role_ref,task_preferences=task_preferences,output_type=output_type,channel=channel),build_process_plan(workflow_id=workflow_id)
    except ValueError as exc:return {'error':str(exc)},None


def prepare_work(task,business_id=None,workspace=None,focus=None,operator_ref=None,team_ref=None,role_ref=None,task_preferences=None,output_type=None,channel=None,selected_playbook_id=None,selected_workflow_id=None):
    task=(task or '').strip()
    if not task:return {'format_version':'4.2','status':'needs_input','missing':['request']}
    if workspace:os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':return {'format_version':'4.2','status':'needs_input','workspace':str(workspace_root()),**{k:v for k,v in resolved.items() if k!='status'}}
    bid=resolved['business_id'];focus=focus or [];registry=load_registry().get('contracts',[])
    playbook=get_playbook(selected_playbook_id,registry) if selected_playbook_id else None
    if selected_playbook_id and not playbook:raise ValueError(f'Unknown or unavailable Playbook: {selected_playbook_id}')
    owner=playbook.get('owner_system') if playbook else None
    selected_workflow=_selected_workflow(task,bid,selected_workflow_id,team_ref,role_ref,operator_ref) if selected_workflow_id else None
    if selected_workflow and owner and selected_workflow.get('owner_system')!=owner:selected_workflow={**selected_workflow,'cross_area':True}
    playbook_candidates=[] if playbook else find_playbook_candidates(task,3);workflow_candidates=[] if selected_workflow else _workflow_candidates(task,bid,owner,team_ref,role_ref,operator_ref)
    context,process=_workflow_context(bid,selected_workflow_id,focus,operator_ref,team_ref,role_ref,task_preferences,output_type,channel);baseline=_baseline_context(bid)
    if context and not context.get('error'):
        object_context=[{'object_ref':oid,'path':path} for oid,path in zip(context.get('object_refs',[]),context.get('object_files',[]))];context_files=context.get('files',[])
    else:object_context=[];context_files=['CONTEXT.md','docs/operating-knowledge.md']
    playbook_view=None
    if playbook:
        try:playbook_view=build_process_plan(playbook_id=playbook['id'])
        except ValueError as exc:playbook_view={'error':str(exc)}
    return {
        'format_version':'4.2','status':'ready','workspace':str(workspace_root()),'business_id':bid,'business_resolution':resolved.get('resolution'),'original_request':task,
        'retrieval':{'baseline_context':baseline,'workflow_context':object_context,'context_files':context_files,'unresolved_selectors':(context or {}).get('unresolved_selectors',[]) if isinstance(context,dict) else [],'rule':'Load only what materially helps the request. Absence from retrieved AURA context means AURA has no selected durable record, not that the real-world fact does not exist.'},
        'operating_knowledge':{'selected_playbook':playbook,'playbook_candidates':playbook_candidates,'playbook_view':playbook_view,'selected_workflow':selected_workflow,'workflow_candidates':workflow_candidates,'workflow_process':process if selected_workflow_id else None,'rule':'Playbooks frame end-to-end business jobs; Workflows provide reusable procedures. The active model/user decides what applies, how to compose it, and whether another Skill or method is better.'},
        'method_options':METHOD_TYPES,'execution_rule':'Use the active model/harness normally. AURA does not define a tool/provider allowlist; use the best available tools, external Skills, resources, and orchestration that serve the requested outcome.','run':{'created':False,'rule':'Do not create a Run merely to begin reasoning. A bounded work receipt is optional when continuity/provenance materially benefits from one.'},
        'next':{'work':'Use the active model/harness normally with the retrieved organizational context.','select_playbook':f'python3 scripts/enter.py {json.dumps(task)} --business-id {bid} --selected-playbook <playbook-id>','select_workflow':f'python3 scripts/enter.py {json.dumps(task)} --business-id {bid} --selected-workflow <workflow-id>','persistence':'Persist only material organizational meaning through supported canonical helpers. A Run is optional and should not be required merely to remember durable truth.'},
        'persistence_test':'Would a capable future model working for this organization materially benefit from knowing this after the current session/runtime is gone?','rule':'AURA supplies organization memory and reusable operating knowledge; semantic intent and execution remain with the active intelligence/runtime.'
    }


def main():
    p=argparse.ArgumentParser(description='Resolve organization context and optional AURA Playbook/Workflow candidates without semantic routing or execution-control machinery.');p.add_argument('task');p.add_argument('--business-id');p.add_argument('--workspace');p.add_argument('--focus',action='append',default=[]);p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref');p.add_argument('--task-preferences');p.add_argument('--output-type');p.add_argument('--channel');p.add_argument('--selected-playbook');p.add_argument('--selected-workflow');a=p.parse_args()
    try:result=prepare_work(a.task,a.business_id,a.workspace,a.focus,a.operator_ref,a.team_ref,a.role_ref,a.task_preferences,a.output_type,a.channel,a.selected_playbook,a.selected_workflow)
    except (ValueError,json.JSONDecodeError) as exc:result={'format_version':'4.2','status':'needs_judgment','reason':str(exc)}
    print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(0 if result.get('status')=='ready' else 2)

if __name__=='__main__':main()
