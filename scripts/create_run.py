#!/usr/bin/env python3
from _common import *
import argparse,json,secrets,os
from resolve_preferences import resolve_effective_preferences, _load_task_preferences
from completion_evidence import completion_spec

COMPLETION_POLICY='core/policies/completion-evidence.md'
CONTENT_PREPUBLISH_QA='content.qa.pre-publish'

def _required_subcontract_ids(contract,byid):
    out=[]
    for item in ((contract.get('subcontracts') or {}).get('required') or []):
        cid=item.get('id') if isinstance(item,dict) else item
        if not isinstance(cid,str) or not cid.strip():
            raise SystemExit(f"Invalid required subcontract metadata for {contract.get('id')}: {item!r}")
        cid=cid.strip()
        if cid not in out: out.append(cid)
    # Content has one shared pre-publish QA floor, so older Content media contracts
    # inherit it when they do not already declare a QA subcontract. Other production
    # owners keep the QA architecture their contracts actually declare; Run creation
    # must not invent a cross-domain QA requirement merely because an Asset is public-facing.
    if (
        contract.get('owner_system')=='content-synthesis'
        and contract.get('artifact_role')=='customer_facing_production_root'
        and contract.get('id')!=CONTENT_PREPUBLISH_QA
        and not any(cid in byid and completion_spec(byid[cid]).get('profile')=='qa' for cid in out)
    ):
        out.append(CONTENT_PREPUBLISH_QA)
    return out

p=argparse.ArgumentParser()
p.add_argument('business_id');p.add_argument('contract_id');p.add_argument('task');p.add_argument('--focus',action='append',default=[])
p.add_argument('--operator-ref',default=None,help='Stable operator label; defaults to BUSINESSOS_OPERATOR_REF')
p.add_argument('--team-ref',default=None,help='Optional team label; defaults to BUSINESSOS_TEAM_REF')
p.add_argument('--role-ref',default=None,help='Optional role label; defaults to BUSINESSOS_ROLE_REF')
p.add_argument('--output-type',help='Optional output-type context for PreferenceProfile applicability')
p.add_argument('--channel',help='Optional channel context for PreferenceProfile applicability')
p.add_argument('--task-preferences',help='JSON object file of one-task optional preferences; highest preference precedence but still below mandatory requirements')
p.add_argument('--parent-run-id',help='Exact parent Run when this is bounded support work')
p.add_argument('--supersedes-run-id',help='Exact prior active Run intentionally replaced by this same contract/task/focus')
a=p.parse_args()
reg=load_registry();byid={x['id']:x for x in reg['contracts']};valid=set(byid)
if a.contract_id not in valid: raise SystemExit('Unknown contract')
if not (ROOT/'instances'/a.business_id).exists(): raise SystemExit('Unknown business')
operator_ref=a.operator_ref or os.environ.get('BUSINESSOS_OPERATOR_REF')
team_ref=a.team_ref or os.environ.get('BUSINESSOS_TEAM_REF')
role_ref=a.role_ref or os.environ.get('BUSINESSOS_ROLE_REF')
try:
    task_preferences=_load_task_preferences(a.task_preferences)
    pref=resolve_effective_preferences(a.business_id,operator_ref,team_ref,role_ref,byid[a.contract_id].get('owner_system'),a.contract_id,a.output_type,a.channel,task_preferences)
except (ValueError,json.JSONDecodeError) as e:
    raise SystemExit(str(e))
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
    if prior.get('contract_id')!=a.contract_id or prior.get('task')!=a.task or (prior.get('focus_refs') or [])!=a.focus or prior.get('parent_run_id')!=a.parent_run_id:
        raise SystemExit('supersedes-run-id must reference the exact same contract, task, focus, and parent relationship')
rid='run_'+secrets.token_hex(8);parent=related.get('parent');prior=related.get('superseded')
corr=(parent or prior or {}).get('correlation_id') or 'cor_'+secrets.token_hex(8);root_run_id=(parent or {}).get('root_run_id') or (a.parent_run_id if parent else rid)
ts=now();d=ROOT/'runtime/runs'/a.business_id/rid;d.mkdir(parents=True)
obj={'run_id':rid,'business_id':a.business_id,'task':a.task,'contract_id':a.contract_id,'status':'active','focus_refs':a.focus,
     'operator_ref':operator_ref,'team_ref':team_ref,'role_ref':role_ref,'preference_output_type':a.output_type,'preference_channel':a.channel,'preference_snapshot_ref':f'runtime/runs/{a.business_id}/{rid}/artifacts/effective-preferences.json',
     'completion_policy_ref':COMPLETION_POLICY,
     'continuity':{
         'format_version':'1.0','purpose':'organizational_work_receipt','state':'active','method_ref':a.contract_id,
         'evidence_refs':[],'result_refs':[],'completed_at':None,'superseded_by_run_id':None
     },
     'correlation_id':corr,'causation_id':a.parent_run_id or a.supersedes_run_id,
     'root_run_id':root_run_id,'parent_run_id':a.parent_run_id,'run_role':'support' if a.parent_run_id else 'root',
     'supersedes_run_id':a.supersedes_run_id,'superseded_by_run_id':None,'lifecycle_reason':None,
     'created_at':ts,'updated_at':ts}
(d/'run.json').write_text(json.dumps(obj,indent=2)+'\n');(d/'artifacts').mkdir();(d/'checkpoints').mkdir();(d/'logs').mkdir();(d/'work').mkdir()
(d/'artifacts'/'effective-preferences.json').write_text(json.dumps(pref,indent=2)+'\n')
required=_required_subcontract_ids(byid[a.contract_id],byid)
manifest={
    'format_version':'1.1','run_id':rid,'business_id':a.business_id,
    'root_contract_id':a.contract_id,'root_status':'active','completion_policy_ref':COMPLETION_POLICY,
    'root_completion_evidence_spec':completion_spec(byid[a.contract_id]),
    'required_subcontracts':required,
    'contracts':{cid:{
        'status':'pending','evidence_refs':[],'note':None,'updated_at':ts,
        'completion_evidence_spec':completion_spec(byid[cid])
    } for cid in required},
    'created_at':ts,'updated_at':ts
}
(d/'contract-execution.json').write_text(json.dumps(manifest,indent=2)+'\n');(d/'README.md').write_text(f'Run-local working/recovery state for one bounded organizational work receipt. Use work/ as the default scratch/build/cache/render directory when needed; do not place temporary or generated execution files under the AURA product root. Preserve material results rather than transcripts or hidden reasoning, and resume according to core/policies/local-state-and-recovery.md. Follow {COMPLETION_POLICY}: completion evidence profiles are deterministic minimums, not substitutes for contract-specific business quality. The effective-preferences snapshot is execution context only and does not override mandatory BusinessOS/business/Brand/contract/approval rules.\n');print(rid)
