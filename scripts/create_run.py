#!/usr/bin/env python3
"""Create one optional organization-owned work receipt.

A Run records bounded continuity when that continuity is actually useful. It does not create
an execution plan, Workflow graph, capability preflight, provider binding, permission gate,
or scheduler state. Method fields record what materially framed the work; they do not turn
Playbooks or Workflows into execution authority.
"""
from _common import *
import argparse,json,secrets,os,sys
from resolve_preferences import resolve_effective_preferences,_load_task_preferences
from operating_knowledge import get_playbook

METHOD_TYPES={'aura_playbook','aura_workflow','external_skill','model_created','ad_hoc'}


def _args(byid):
    raw=sys.argv[1:]
    # Human convenience: create_run.py BUSINESS_ID WORKFLOW_ID TASK
    if len(raw)>=3 and raw[1] in byid and not raw[2].startswith('-'):
        raw=[raw[0],raw[2],'--workflow-id',raw[1],*raw[3:]]
    p=argparse.ArgumentParser(description='Create an optional bounded AURA work receipt for any method.')
    p.add_argument('business_id');p.add_argument('task')
    p.add_argument('--playbook-id',help='AURA Playbook that materially framed the work.')
    p.add_argument('--workflow-id',help='Detailed AURA Workflow materially used for the work.')
    p.add_argument('--method-type',choices=sorted(METHOD_TYPES),help='Explicit provenance when no AURA Playbook/Workflow is selected.')
    p.add_argument('--method-ref',help='Reference/name for an external Skill, model-created method, or other method.')
    p.add_argument('--focus',action='append',default=[])
    p.add_argument('--operator-ref',default=None);p.add_argument('--team-ref',default=None);p.add_argument('--role-ref',default=None)
    p.add_argument('--output-type');p.add_argument('--channel');p.add_argument('--task-preferences')
    return p.parse_args(raw)


def main():
    reg=load_registry();byid={x['id']:x for x in reg['contracts']};a=_args(byid)
    if not (ROOT/'instances'/a.business_id).exists():raise SystemExit('Unknown business')
    workflow=byid.get(a.workflow_id) if a.workflow_id else None
    if a.workflow_id and not workflow:raise SystemExit('Unknown AURA Workflow')
    if workflow and workflow.get('type')!='workflow':raise SystemExit(f'{a.workflow_id} is not an AURA Workflow')
    playbook=get_playbook(a.playbook_id,reg.get('contracts',[])) if a.playbook_id else None
    if a.playbook_id and not playbook:raise SystemExit('Unknown AURA Playbook')

    if playbook:
        if a.method_type and a.method_type!='aura_playbook':raise SystemExit('--playbook-id cannot be combined with a different method type')
        method_type='aura_playbook';method_ref=playbook['id']
        if a.method_ref and a.method_ref!=method_ref:raise SystemExit('AURA Playbook method_ref must equal playbook_id')
    elif workflow:
        if a.method_type and a.method_type!='aura_workflow':raise SystemExit('--workflow-id cannot be combined with a different method type')
        method_type='aura_workflow';method_ref=a.workflow_id
        if a.method_ref and a.method_ref!=method_ref:raise SystemExit('AURA Workflow method_ref must equal workflow_id')
    else:
        method_type=a.method_type or 'ad_hoc';method_ref=a.method_ref
        if method_type in {'aura_playbook','aura_workflow'}:raise SystemExit(f'{method_type} requires the matching AURA identifier')

    owner=(workflow or playbook or {}).get('owner_system')
    preference_method=a.workflow_id or (playbook.get('entry_workflow') if playbook else None)
    operator_ref=a.operator_ref or os.environ.get('BUSINESSOS_OPERATOR_REF');team_ref=a.team_ref or os.environ.get('BUSINESSOS_TEAM_REF');role_ref=a.role_ref or os.environ.get('BUSINESSOS_ROLE_REF')
    try:
        task_preferences=_load_task_preferences(a.task_preferences)
        pref=resolve_effective_preferences(a.business_id,operator_ref,team_ref,role_ref,owner,preference_method,a.output_type,a.channel,task_preferences)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))

    rid='run_'+secrets.token_hex(8);ts=now();d=runtime_root()/'runs'/a.business_id/rid;d.mkdir(parents=True)
    pref_ref=f'runtime/runs/{a.business_id}/{rid}/artifacts/effective-preferences.json'
    obj={
        'run_id':rid,'business_id':a.business_id,'task':a.task,
        'method_type':method_type,'method_ref':method_ref,'playbook_id':playbook['id'] if playbook else None,'workflow_id':a.workflow_id,
        'status':'active','focus_refs':a.focus,'operator_ref':operator_ref,'team_ref':team_ref,'role_ref':role_ref,
        'preference_output_type':a.output_type,'preference_channel':a.channel,'preference_snapshot_ref':pref_ref,
        'continuity':{'format_version':'2.0','purpose':'organizational_work_receipt','state':'active','method_type':method_type,'method_ref':method_ref,'summary':None,'evidence_refs':[],'result_refs':[],'decision_refs':[],'unresolved':[],'completed_at':None},
        'created_at':ts,'updated_at':ts
    }
    (d/'run.json').write_text(json.dumps(obj,indent=2)+'\n')
    for name in ('artifacts','work'):(d/name).mkdir()
    (d/'artifacts'/'effective-preferences.json').write_text(json.dumps(pref,indent=2)+'\n')
    (d/'README.md').write_text('Optional local continuity for one bounded piece of organizational work. Preserve only what helps the organization resume, inspect, or learn from the work. The active model/harness owns tools, permissions, retries, subagents, scheduling, and execution.\n')
    print(rid)

if __name__=='__main__':main()
