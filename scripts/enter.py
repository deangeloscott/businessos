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

from _common import PRODUCT_ROOT,workspace_root,resolve_business,object_index,storage_ref,load_registry,describe_object,resolve_focus
from find_playbooks import find_candidates as find_playbook_candidates
from find_workflows import find_candidates as find_workflow_candidates
from operating_knowledge import get_playbook
from process_extensions import local_workflow_candidates,resolve_effective
from context_plan import build_plan
from process_plan import build_process_plan
from _lexical import tokens,document_frequency,weighted_overlap
from correction_impacts import pending_corrections
from generate_knowledge_layer import knowledge_layer_freshness

METHOD_TYPES=['aura_playbook','aura_workflow','external_skill','model_created','ad_hoc']
BASELINE_TYPES=['Business','Brand','ProductService','Offer','AudienceSegment','Market','Objective','DecisionRecord','Learning']


def _recipe_menu():
    """Expose the installed optional craft shelf without loading it into context."""
    path=PRODUCT_ROOT/'recipes'/'README.md'
    if not path.is_file():return None
    return {'path':'recipes/README.md','role':'optional_navigation','rule':'Open only when a recipe would materially help; recipes are starting points, not a required method or source of business truth.'}


def _baseline_context(business_id,limit_per_type=3,index=None):
    idx=index if index is not None else object_index(business_id);rows=[];by_type={typ:[] for typ in BASELINE_TYPES}
    for _,(obj,path) in idx.items():
        typ=obj.get('object_type')
        if typ not in by_type or obj.get('status') in {'archived','superseded'}:continue
        by_type[typ].append((obj,path))
    for typ in BASELINE_TYPES:
        candidates=sorted(by_type[typ],key=lambda x:(x[0].get('updated_at') or x[0].get('created_at') or '',x[0].get('id') or ''),reverse=True)
        for obj,path in candidates[:limit_per_type]:rows.append(describe_object(obj,path))
    return rows


def _saved_work_candidates(task,index,limit=6,offset=0):
    """Shared weighted lexical discovery; status and matches are not authority."""
    fields=('id','title','name','statement','summary','business_role','purpose','description','asset_type','location_reference','conclusion','task')
    objects=[obj for obj,_ in index.values()]
    frequencies=document_frequency(objects,fields);terms=tokens(task);ranked=[]
    for obj,path in index.values():
        text=' '.join(str(obj.get(key) or '') for key in fields)
        score,matched=weighted_overlap(terms,text,frequencies,len(objects))
        if not matched:continue
        title_score,_=weighted_overlap(terms,' '.join(str(obj.get(key) or '') for key in ('title','name','business_role','purpose')),frequencies,len(objects))
        row=describe_object(obj,path);row.update(matched_terms=matched,lexical_score=round(score+title_score,6))
        ranked.append((obj.get('status') in {'archived','superseded'},-row['lexical_score'],obj['id'],row))
    return [item[-1] for item in sorted(ranked,key=lambda item:item[:3])[offset:offset+limit]]


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
    return build_plan(business_id,workflow_id,focus=focus,operator_ref=operator_ref,team_ref=team_ref,role_ref=role_ref,task_preferences=task_preferences,output_type=output_type,channel=channel),build_process_plan(workflow_id=workflow_id)


def prepare_work(task,business_id=None,workspace=None,focus=None,operator_ref=None,team_ref=None,role_ref=None,task_preferences=None,output_type=None,channel=None,selected_playbook_id=None,selected_workflow_id=None,saved_work_limit=6,saved_work_offset=0):
    task=(task or '').strip()
    if not task:return {'format_version':'4.2','status':'needs_input','missing':['request']}
    if not 1<=saved_work_limit<=100 or saved_work_offset<0:raise ValueError('saved_work_limit must be 1..100 and saved_work_offset nonnegative')
    if workspace:os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=resolve_business(business_id)
    if resolved.get('status')!='resolved':
        menu=_recipe_menu();payload={'format_version':'4.2','status':'needs_input','workspace':str(workspace_root()),**{k:v for k,v in resolved.items() if k!='status'}}
        if menu:payload['recipe_menu']=menu
        return payload
    bid=resolved['business_id'];focus=focus or [];registry=load_registry().get('workflows',[])
    read_diagnostics=[];index=object_index(bid,read_diagnostics);focused,unresolved_focus=resolve_focus(index,focus,read_diagnostics)
    focus_context=[describe_object(obj,path) for obj,path in focused.values()]
    playbook=get_playbook(selected_playbook_id,registry) if selected_playbook_id else None
    if selected_playbook_id and not playbook:raise ValueError(f'Unknown or unavailable Playbook: {selected_playbook_id}')
    owner=playbook.get('owner_system') if playbook else None
    selected_workflow=_selected_workflow(task,bid,selected_workflow_id,team_ref,role_ref,operator_ref) if selected_workflow_id else None
    if selected_workflow and owner and selected_workflow.get('owner_system')!=owner:selected_workflow={**selected_workflow,'cross_area':True}
    playbook_candidates=[] if playbook else find_playbook_candidates(task,3);workflow_candidates=[] if selected_workflow else _workflow_candidates(task,bid,owner,team_ref,role_ref,operator_ref)
    context,workflow_view=_workflow_context(bid,selected_workflow_id,focus,operator_ref,team_ref,role_ref,task_preferences,output_type,channel);baseline=_baseline_context(bid,index=index)
    if context and not context.get('error'):
        object_context=context.get('object_context',[]);context_files=context.get('files',[]);supporting_context_refs=context.get('supporting_context_refs',[]);context_reading_rule=context.get('context_reading_rule')
    else:
        object_context=[];context_files=['CONTEXT.md','docs/operating-knowledge.md'];supporting_context_refs=[];context_reading_rule='Load only the small universal context that materially helps. Optional recipe navigation is separate from organizational context.'
    recipe_menu=_recipe_menu()
    for row in focus_context:
        if row['path'] not in context_files:context_files.append(row['path'])
    playbook_view=None
    if playbook:
        try:playbook_view=build_process_plan(playbook_id=playbook['id'])
        except ValueError as exc:playbook_view={'error':str(exc)}
    candidates=_saved_work_candidates(task,index,saved_work_limit+1,saved_work_offset)
    return {
        'format_version':'4.2','status':'needs_judgment' if unresolved_focus or read_diagnostics else 'ready','workspace':str(workspace_root()),'business_id':bid,'business_resolution':resolved.get('resolution'),'original_request':task,
        'retrieval':{
            'focus_context':focus_context,'unresolved_focus':unresolved_focus,'saved_work_candidates':candidates[:saved_work_limit],
            'saved_work_search':{'limit':saved_work_limit,'offset':saved_work_offset,'next_offset':saved_work_offset+saved_work_limit if len(candidates)>saved_work_limit else None,'broaden':'Use --saved-work-limit (up to 100), --saved-work-offset, or different title/purpose/filename terms. Linked document contents are not indexed.'},
            'read_diagnostics':read_diagnostics[:10],'read_diagnostic_count':len(read_diagnostics),
            'correction_review':pending_corrections(index,saved_work_limit),
            'knowledge_view':knowledge_layer_freshness(bid),
            'lookup_rule':'Candidates are lexical matches, not accepted conclusions. Read records and artifacts; status, assumptions and evidence limits matter. Recency is not authority. Missing optional context does not block useful work. Resolve missing refs/read failures before relying on completeness.',
            'baseline_context':baseline,'workflow_context':object_context,'context_files':context_files,'supporting_context_refs':supporting_context_refs,'context_reading_rule':context_reading_rule,
            'unresolved_selectors':(context or {}).get('unresolved_selectors',[]) if isinstance(context,dict) else [],
            'rule':'Load only what materially helps. No match is not proof of absence; read failures mean retrieval is incomplete.'},
        'operating_knowledge':{'selected_playbook':playbook,'playbook_candidates':playbook_candidates,'playbook_view':playbook_view,'selected_workflow':selected_workflow,'workflow_candidates':workflow_candidates,'workflow_view':workflow_view if selected_workflow_id else None,'rule':'Playbooks frame end-to-end business jobs; Workflows provide reusable procedures. The active model/user decides what applies, how to compose it, and whether another Skill or method is better.'},
        'recipe_menu':recipe_menu,
        'method_options':METHOD_TYPES,'execution_rule':'Use the active model/harness normally. AURA does not define a tool/provider allowlist; use the best available tools, external Skills, resources, and orchestration that serve the requested outcome.','run':{'created':False,'rule':'Do not create a Run merely to begin reasoning. A bounded work receipt is optional when continuity/provenance materially benefits from one.'},
        'next':{'work':'Use the active model/harness normally with the retrieved organizational context.','select_playbook':f'python3 scripts/enter.py {json.dumps(task)} --business-id {bid} --selected-playbook <playbook-id>','select_workflow':f'python3 scripts/enter.py {json.dumps(task)} --business-id {bid} --selected-workflow <workflow-id>','persistence':'Persist only material organizational meaning through supported canonical helpers. A Run is optional and should not be required merely to remember durable truth.'},
        'persistence_test':'Would a capable future model working for this organization materially benefit from knowing this after the current session/runtime is gone?','rule':'AURA supplies organization memory and reusable operating knowledge; semantic intent and execution remain with the active intelligence/runtime.'
    }


def main():
    p=argparse.ArgumentParser(description='Resolve organization context and optional AURA Playbook/Workflow candidates without semantic routing or execution-control machinery.');p.add_argument('task');p.add_argument('--business-id');p.add_argument('--workspace');p.add_argument('--focus',action='append',default=[],metavar='OBJECT_ID',help='Exact saved object ID; repeat for multiple records. Put search words in the positional task.');p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref');p.add_argument('--task-preferences');p.add_argument('--output-type');p.add_argument('--channel');p.add_argument('--selected-playbook');p.add_argument('--selected-workflow');p.add_argument('--json',action='store_true',help='JSON is already the default.');p.add_argument('--saved-work-limit',type=int,default=6);p.add_argument('--saved-work-offset',type=int,default=0);a=p.parse_args()
    try:result=prepare_work(a.task,a.business_id,a.workspace,a.focus,a.operator_ref,a.team_ref,a.role_ref,a.task_preferences,a.output_type,a.channel,a.selected_playbook,a.selected_workflow,a.saved_work_limit,a.saved_work_offset)
    except (ValueError,json.JSONDecodeError) as exc:result={'format_version':'4.2','status':'needs_judgment','reason':str(exc)}
    print(json.dumps(result,indent=2,ensure_ascii=False));raise SystemExit(0 if result.get('status')=='ready' else 2)

if __name__=='__main__':main()
