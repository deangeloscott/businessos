#!/usr/bin/env python3
"""Establish a governed AURA execution envelope for ordinary organization/business work.

This is deliberately not an agent, harness, scheduler, model router, or workflow engine.
A capable agent/harness decides whether the user's request is organizational work. Once
that boundary is crossed, this helper makes the reliability mechanics deterministic:
workspace/business resolution, routing, Run creation/recovery, process/context planning,
capability preflight, and lightweight monitoring-continuity visibility. The agent then
performs the actual business work using the returned envelope and whatever authorized host
capabilities are available.
"""
from pathlib import Path
import argparse, json, os, subprocess, sys

from _common import PRODUCT_ROOT, workspace_root, instances_root, runtime_root, storage_ref
from route_and_resolve import route_and_resolve
from process_plan import build_process_plan
from context_plan import build_plan
from preflight_capabilities import preflight
from list_due_monitoring import summarize as summarize_monitoring


def _business_ids():
    root=instances_root()
    if not root.exists(): return []
    return sorted(p.name for p in root.iterdir() if p.is_dir() and p.name!='_template')


def _resolve_business(explicit=None):
    explicit=explicit or os.environ.get('BUSINESSOS_BUSINESS_ID')
    ids=_business_ids()
    if explicit:
        if explicit in ids:return {'status':'resolved','business_id':explicit,'resolution':'explicit'}
        return {'status':'needs_input','missing':['active_business'],'reason':f'Unknown business: {explicit}','available_business_ids':ids}
    if len(ids)==1:return {'status':'resolved','business_id':ids[0],'resolution':'single_workspace_business'}
    if not ids:return {'status':'needs_input','missing':['active_business'],'reason':'No initialized business exists in the active organization workspace.','available_business_ids':[]}
    return {'status':'needs_input','missing':['active_business'],'reason':'Multiple businesses exist in the active organization workspace; the active business is ambiguous.','available_business_ids':ids}


def _matching_active_runs(business_id,contract_id,task):
    root=runtime_root()/'runs'/business_id
    if not root.exists():return []
    rows=[]
    for rp in root.glob('*/run.json'):
        try:d=json.loads(rp.read_text())
        except Exception:continue
        if d.get('status')!='active':continue
        if d.get('business_id')!=business_id or d.get('contract_id')!=contract_id or d.get('task')!=task:continue
        rows.append((d.get('updated_at') or d.get('created_at') or '',d.get('run_id'),rp))
    return sorted(rows,reverse=True)


def _create_run(business_id,contract_id,task,operator_ref=None,team_ref=None,role_ref=None,output_type=None,channel=None,task_preferences=None):
    cmd=[sys.executable,str(PRODUCT_ROOT/'scripts/create_run.py'),business_id,contract_id,task]
    for flag,value in [('--operator-ref',operator_ref),('--team-ref',team_ref),('--role-ref',role_ref),('--output-type',output_type),('--channel',channel),('--task-preferences',task_preferences)]:
        if value is not None:cmd.extend([flag,str(value)])
    p=subprocess.run(cmd,cwd=PRODUCT_ROOT,capture_output=True,text=True)
    if p.returncode!=0:raise ValueError((p.stderr or p.stdout or 'Run creation failed').strip())
    rid=p.stdout.strip().splitlines()[-1].strip()
    if not rid.startswith('run_'):raise ValueError(f'Unexpected Run creation output: {p.stdout!r}')
    return rid


def _monitoring_continuity(business_id):
    try:
        data=summarize_monitoring(business_id)
        return {
            'status':'available',
            'tracked_subject_count':data.get('tracked_subject_count',0),
            'due_unbound_count':data.get('due_unbound_count',0),
            'due_unbound_subjects':data.get('due_unbound_subjects',[]),
            'environment':data.get('environment'),
            'rule':'Do not derail an unrelated request to clear a monitoring backlog. Refresh overdue work when relevant/authorized or surface one concise notice when it materially matters. A saved cadence/next check is not an active schedule without a verified scheduler binding.'
        }
    except (ValueError,json.JSONDecodeError) as e:
        return {
            'status':'degraded',
            'reason':str(e),
            'rule':'Monitoring-continuity inspection must not fabricate schedule state or silently block otherwise valid organizational work.'
        }


def enter(task,business_id=None,workspace=None,operator_ref=None,team_ref=None,role_ref=None,output_type=None,channel=None,task_preferences=None,new_run=False,include_optional_capabilities=True):
    task=(task or '').strip()
    if not task:return {'format_version':'1.0','status':'needs_input','missing':['request'],'reason':'Preserve and provide the user\'s original organizational request.'}
    if workspace:
        os.environ['BUSINESSOS_WORKSPACE']=str(Path(workspace).expanduser().resolve())
    resolved=_resolve_business(business_id)
    if resolved['status']!='resolved':
        return {'format_version':'1.0','status':'needs_input','workspace':str(workspace_root()),**{k:v for k,v in resolved.items() if k!='status'}}
    bid=resolved['business_id']
    continuity=_monitoring_continuity(bid)
    try:route=route_and_resolve(task,bid,team_ref,role_ref,operator_ref)
    except ValueError as e:return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'monitoring_continuity':continuity,'reason':str(e)}
    cid=route.get('contract_id')
    if not cid or route.get('status')!='available':
        return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'original_request':task,'route':route,'monitoring_continuity':continuity,'reason':'AURA did not resolve an available business-work entry contract.'}

    matches=[] if new_run else _matching_active_runs(bid,cid,task)
    if matches:
        rid=matches[0][1];resumed=True
    else:
        try:rid=_create_run(bid,cid,task,operator_ref,team_ref,role_ref,output_type,channel,task_preferences);resumed=False
        except ValueError as e:return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'original_request':task,'route':route,'monitoring_continuity':continuity,'reason':str(e)}

    run_dir=runtime_root()/'runs'/bid/rid
    work_dir=run_dir/'work';work_dir.mkdir(parents=True,exist_ok=True)
    try:
        process=build_process_plan(contract_id=cid)
        context=build_plan(bid,cid,operator_ref=operator_ref,team_ref=team_ref,role_ref=role_ref,run_id=rid)
        capabilities=preflight(bid,cid,include_optional=include_optional_capabilities)
    except (ValueError,json.JSONDecodeError) as e:
        return {'format_version':'1.0','status':'blocked','business_id':bid,'workspace':str(workspace_root()),'original_request':task,'route':route,'monitoring_continuity':continuity,'run_id':rid,'run_ref':storage_ref(run_dir),'reason':str(e)}

    env={
        'BUSINESSOS_WORKSPACE':str(workspace_root()),
        'BUSINESSOS_BUSINESS_ID':bid,
        'BUSINESSOS_RUN_ID':rid,
        'BUSINESSOS_CONTRACT_ID':cid,
        'BUSINESSOS_WORK_DIR':str(work_dir),
    }
    return {
        'format_version':'1.0',
        'status':'ready',
        'workspace':str(workspace_root()),
        'business_id':bid,
        'business_resolution':resolved.get('resolution'),
        'original_request':task,
        'route':route,
        'monitoring_continuity':continuity,
        'run':{
            'run_id':rid,
            'resumed':resumed,
            'run_ref':storage_ref(run_dir),
            'work_dir':str(work_dir),
            'work_ref':storage_ref(work_dir),
        },
        'process_plan':process,
        'context_plan':context,
        'capability_preflight':capabilities,
        'execution_env':env,
        'agent_handoff':{
            'instruction':'Continue the user\'s complete original request inside this AURA Run. Use the resolved context/process and authorized host Skills/tools as executors; do not replace AURA routing, business truth, authorization, evidence, canonical state, required subcontracts, QA, completion, or Learning.',
            'scratch_rule':'Use the Run work_dir for build/cache/render/temp state. The AURA product root remains read-only during ordinary business operation.',
            'persistence_rule':'Persist only material organizational evidence, findings, decisions, governed Assets/state, completion evidence, and evidence-supported Learning; ordinary scratch/tool internals remain working state.',
            'continuity_rule':'Use monitoring_continuity as a lightweight memory cue, not a competing task queue. If overdue unbound monitoring is relevant to this request, refresh it through the appropriate AURA process. If it materially matters but is unrelated, surface at most one concise notice. Otherwise continue the user\'s request. Never describe planned cadence as an active schedule without a verified scheduler binding.',
            'human_ux_rule':'In the final response, describe saved work using the organization/human knowledge concept first. Raw canonical/runtime filesystem paths are optional advanced inspection details, not the primary UX.'
        },
    }


def main():
    p=argparse.ArgumentParser(description='Enter AURA for an ordinary organization/business request and return a governed execution envelope. This helper is not for unrelated personal tasks or AURA product-development work.')
    p.add_argument('request',help='The user\'s complete original natural-language organizational request')
    p.add_argument('--business-id')
    p.add_argument('--workspace',help='Optional organization workspace root; otherwise use configured BUSINESSOS_WORKSPACE/workspace link')
    p.add_argument('--operator-ref');p.add_argument('--team-ref');p.add_argument('--role-ref')
    p.add_argument('--output-type');p.add_argument('--channel');p.add_argument('--task-preferences')
    p.add_argument('--new-run',action='store_true',help='Force a new Run instead of resuming an exact active business+contract+request match')
    p.add_argument('--required-only-capabilities',action='store_true',help='Skip optional capability checks in the returned preflight')
    a=p.parse_args()
    out=enter(a.request,a.business_id,a.workspace,a.operator_ref,a.team_ref,a.role_ref,a.output_type,a.channel,a.task_preferences,a.new_run,not a.required_only_capabilities)
    print(json.dumps(out,indent=2)+'\n',end='')
    raise SystemExit(0 if out.get('status')=='ready' else 2)


if __name__=='__main__':main()
