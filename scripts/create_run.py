#!/usr/bin/env python3
"""Create one optional organization-owned work receipt.

A Run records bounded continuity around one piece of work when that continuity is useful to
resume, inspect, or hand off. It does not create an execution plan, parent/child work graph,
subcontract ledger, capability preflight, provider binding, permission gate, or scheduler
state. Selecting an AURA playbook records the method that was used; it does not turn the
playbook into execution authority.
"""
from _common import *
import argparse, json, secrets, os, sys
from resolve_preferences import resolve_effective_preferences, _load_task_preferences

METHOD_TYPES={'aura_playbook','external_skill','model_created','ad_hoc'}


def _args(byid):
    raw=sys.argv[1:]
    # Accept the older positional human convenience:
    #   create_run.py BUSINESS_ID CONTRACT_ID TASK
    # Canonical form:
    #   create_run.py BUSINESS_ID TASK [--contract-id ... | --method-type ...]
    if len(raw)>=3 and raw[1] in byid and not raw[2].startswith('-'):
        raw=[raw[0],raw[2],'--contract-id',raw[1],*raw[3:]]
    p=argparse.ArgumentParser(description='Create an optional bounded AURA work receipt for any method.')
    p.add_argument('business_id');p.add_argument('task')
    p.add_argument('--contract-id',help='AURA playbook actually used for the work. Implies --method-type aura_playbook.')
    p.add_argument('--method-type',choices=sorted(METHOD_TYPES),help='How the work is actually being performed; defaults to ad_hoc when no AURA playbook is selected.')
    p.add_argument('--method-ref',help='Provider-neutral reference/name for an external Skill, model-created method, or other method.')
    p.add_argument('--focus',action='append',default=[])
    p.add_argument('--operator-ref',default=None,help='Stable operator label; defaults to BUSINESSOS_OPERATOR_REF')
    p.add_argument('--team-ref',default=None,help='Optional team label; defaults to BUSINESSOS_TEAM_REF')
    p.add_argument('--role-ref',default=None,help='Optional role label; defaults to BUSINESSOS_ROLE_REF')
    p.add_argument('--output-type',help='Optional output-type context for PreferenceProfile applicability')
    p.add_argument('--channel',help='Optional channel context for PreferenceProfile applicability')
    p.add_argument('--task-preferences',help='JSON object file of one-task optional preferences')
    return p.parse_args(raw)


def main():
    reg=load_registry();byid={x['id']:x for x in reg['contracts']};a=_args(byid)
    if not (ROOT/'instances'/a.business_id).exists():raise SystemExit('Unknown business')

    contract=None
    if a.contract_id:
        contract=byid.get(a.contract_id)
        if not contract:raise SystemExit('Unknown contract')
        if a.method_type and a.method_type!='aura_playbook':raise SystemExit('--contract-id cannot be combined with a non-AURA method type')
        method_type='aura_playbook';method_ref=a.contract_id
        if a.method_ref and a.method_ref!=a.contract_id:raise SystemExit('AURA playbook method_ref must equal contract_id')
    else:
        method_type=a.method_type or 'ad_hoc';method_ref=a.method_ref
        if method_type=='aura_playbook':raise SystemExit('aura_playbook work requires --contract-id')

    operator_ref=a.operator_ref or os.environ.get('BUSINESSOS_OPERATOR_REF')
    team_ref=a.team_ref or os.environ.get('BUSINESSOS_TEAM_REF')
    role_ref=a.role_ref or os.environ.get('BUSINESSOS_ROLE_REF')
    try:
        task_preferences=_load_task_preferences(a.task_preferences)
        pref=resolve_effective_preferences(
            a.business_id,operator_ref,team_ref,role_ref,
            contract.get('owner_system') if contract else None,
            a.contract_id if contract else None,
            a.output_type,a.channel,task_preferences
        )
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))

    rid='run_'+secrets.token_hex(8);ts=now();d=runtime_root()/'runs'/a.business_id/rid;d.mkdir(parents=True)
    pref_ref=f'runtime/runs/{a.business_id}/{rid}/artifacts/effective-preferences.json'
    obj={
        'run_id':rid,'business_id':a.business_id,'task':a.task,
        'method_type':method_type,'method_ref':method_ref,'contract_id':a.contract_id if contract else None,
        'status':'active','focus_refs':a.focus,
        'operator_ref':operator_ref,'team_ref':team_ref,'role_ref':role_ref,
        'preference_output_type':a.output_type,'preference_channel':a.channel,'preference_snapshot_ref':pref_ref,
        'continuity':{
            'format_version':'2.0','purpose':'organizational_work_receipt','state':'active',
            'method_type':method_type,'method_ref':method_ref,'summary':None,
            'evidence_refs':[],'result_refs':[],'decision_refs':[],'unresolved':[],
            'completed_at':None
        },
        'created_at':ts,'updated_at':ts
    }
    (d/'run.json').write_text(json.dumps(obj,indent=2)+'\n')
    for name in ('artifacts','work'):(d/name).mkdir()
    (d/'artifacts'/'effective-preferences.json').write_text(json.dumps(pref,indent=2)+'\n')
    (d/'README.md').write_text(
        'Optional local continuity for one bounded piece of organizational work. '
        'Use work/ for temporary working files when useful and artifacts/ for material receipt evidence. '
        'Preserve only what helps the organization resume, inspect, or learn from the work. '
        'The active model/harness owns tools, permissions, retries, subagents, scheduling, and execution.\n'
    )
    print(rid)


if __name__=='__main__':main()
