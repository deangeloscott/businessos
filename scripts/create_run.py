#!/usr/bin/env python3
from _common import *
import argparse,json,secrets,os
from resolve_preferences import resolve_effective_preferences, _load_task_preferences
from completion_evidence import completion_spec

COMPLETION_POLICY='core/policies/completion-evidence.md'

def _required_subcontract_ids(contract):
    out=[]
    for item in ((contract.get('subcontracts') or {}).get('required') or []):
        cid=item.get('id') if isinstance(item,dict) else item
        if not isinstance(cid,str) or not cid.strip():
            raise SystemExit(f"Invalid required subcontract metadata for {contract.get('id')}: {item!r}")
        out.append(cid.strip())
    return out

p=argparse.ArgumentParser()
p.add_argument('business_id');p.add_argument('contract_id');p.add_argument('task');p.add_argument('--focus',action='append',default=[])
p.add_argument('--operator-ref',default=None,help='Stable operator label; defaults to BUSINESSOS_OPERATOR_REF')
p.add_argument('--team-ref',default=None,help='Optional team label; defaults to BUSINESSOS_TEAM_REF')
p.add_argument('--role-ref',default=None,help='Optional role label; defaults to BUSINESSOS_ROLE_REF')
p.add_argument('--output-type',help='Optional output-type context for PreferenceProfile applicability')
p.add_argument('--channel',help='Optional channel context for PreferenceProfile applicability')
p.add_argument('--task-preferences',help='JSON object file of one-task optional preferences; highest preference precedence but still below mandatory requirements')
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
rid='run_'+secrets.token_hex(8);corr='cor_'+secrets.token_hex(8);ts=now();d=ROOT/'runtime/runs'/a.business_id/rid;d.mkdir(parents=True)
obj={'run_id':rid,'business_id':a.business_id,'task':a.task,'contract_id':a.contract_id,'status':'active','focus_refs':a.focus,
     'operator_ref':operator_ref,'team_ref':team_ref,'role_ref':role_ref,'preference_output_type':a.output_type,'preference_channel':a.channel,'preference_snapshot_ref':f'runtime/runs/{a.business_id}/{rid}/artifacts/effective-preferences.json',
     'completion_policy_ref':COMPLETION_POLICY,'correlation_id':corr,'causation_id':None,'created_at':ts,'updated_at':ts}
(d/'run.json').write_text(json.dumps(obj,indent=2)+'\n');(d/'artifacts').mkdir();(d/'checkpoints').mkdir();(d/'logs').mkdir()
(d/'artifacts'/'effective-preferences.json').write_text(json.dumps(pref,indent=2)+'\n')
required=_required_subcontract_ids(byid[a.contract_id])
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
(d/'contract-execution.json').write_text(json.dumps(manifest,indent=2)+'\n');(d/'README.md').write_text(f'Run-local working/recovery state. Preserve validated outputs and resume according to core/policies/local-state-and-recovery.md. Follow {COMPLETION_POLICY}: completion evidence profiles are deterministic minimums, not substitutes for contract-specific business quality. The effective-preferences snapshot is execution context only and does not override mandatory BusinessOS/business/Brand/contract/approval rules.\n');print(rid)
