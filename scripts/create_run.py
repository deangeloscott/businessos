#!/usr/bin/env python3
"""Create one optional organization-owned work receipt.

A Run records bounded continuity around work that is useful to resume, inspect, or hand off.
It does not create an execution plan, subcontract ledger, capability preflight, provider
binding, permission gate, or scheduler state. Selecting an AURA playbook records the method
that was used; it does not turn the playbook into execution authority.
"""
from _common import *
import argparse, json, secrets, os, sys
from resolve_preferences import resolve_effective_preferences, _load_task_preferences

METHOD_TYPES={'aura_playbook','external_skill','model_created','ad_hoc'}


def _method_identity(run):
    method_type=run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')
    method_ref=run.get('method_ref') or run.get('contract_id')
    return method_type,method_ref


def _args(byid):
    raw=sys.argv[1:]
    # Accept the older positional form as a human convenience without preserving its
    # historical execution semantics:
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
    p.add_argument('--parent-run-id',help='Exact parent receipt when this is bounded support work')
    p.add_argument('--supersedes-run-id',help='Exact prior active receipt intentionally replaced by this same work')
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

    related={}
    for label,value in [('parent',a.parent_run_id),('superseded',a.supersedes_run_id)]:
        if not value:continue
        path=run_dir_path(a.business_id,value)/'run.json'
        if not path.exists():raise SystemExit(f'Unknown {label} Run for this business: {value}')
        try:related[label]=json.loads(path.read_text())
        except Exception as exc:raise SystemExit(f'Invalid {label} Run {value}: {exc}')
        if related[label].get('business_id')!=a.business_id:raise SystemExit(f'{label.title()} Run business_id mismatch')
    if a.supersedes_run_id:
        prior=related['superseded']
        if prior.get('status')!='active':raise SystemExit('supersedes-run-id must reference an active Run')
        prior_type,prior_ref=_method_identity(prior)
        if prior_type!=method_type or prior_ref!=method_ref or prior.get('task')!=a.task or (prior.get('focus_refs') or [])!=a.focus or prior.get('parent_run_id')!=a.parent_run_id:
            raise SystemExit('supersedes-run-id must reference the exact same method, task, focus, and parent relationship')

    rid='run_'+secrets.token_hex(8);parent=related.get('parent');prior=related.get('superseded')
    corr=(parent or prior or {}).get('correlation_id') or 'cor_'+secrets.token_hex(8)
    root_run_id=(parent or {}).get('root_run_id') or (a.parent_run_id if parent else rid)
    ts=now();d=runtime_root()/'runs'/a.business_id/rid;d.mkdir(parents=True)
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
            'completed_at':None,'superseded_by_run_id':None
        },
        'correlation_id':corr,'causation_id':a.parent_run_id or a.supersedes_run_id,
        'root_run_id':root_run_id,'parent_run_id':a.parent_run_id,'run_role':'support' if a.parent_run_id else 'root',
        'supersedes_run_id':a.supersedes_run_id,'superseded_by_run_id':None,'lifecycle_reason':None,
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
