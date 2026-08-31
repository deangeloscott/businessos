#!/usr/bin/env python3
"""Shared bounded-Run provenance helpers for organization-owned work receipts."""
from _common import *
import json

# Canonical state whose creation/update represents durable organizational meaning from
# bounded work. Raw runtime delivery/reaction state is intentionally absent: hosts own
# event processing, scheduling, retries, idempotency, and delivery mechanics.
RUN_BOUND_TYPES={
    'Opportunity','Initiative','DecisionRecord',
    'AttentionItem','ChangeEvent','Incident','VerificationRecord','WorkRequest',
    'Experiment','OutcomeEvaluation','Learning','PlatformChange'
}
LEGACY_ORIGINS={'imported','preexisting'}


def run_dir(business_id,run_id):
    return ROOT/'runtime'/'runs'/business_id/run_id


def run_ref(business_id,run_id):
    return str(run_dir(business_id,run_id).relative_to(ROOT))


def _canonical_dict(data,business_id):
    return isinstance(data,dict) and data.get('object_type') and data.get('business_id')==business_id


def bind_evidence_path(business_id,run_id,evidence_path,binding='run_evidence'):
    p=Path(evidence_path); p=p if p.is_absolute() else ROOT/p
    if not p.exists() or p.suffix.lower()!='.json':return False
    try:data=json.loads(p.read_text())
    except Exception:return False
    if not _canonical_dict(data,business_id):return False
    rp=run_dir(business_id,run_id)/'run.json'
    if not rp.exists():raise ValueError(f'Run missing while binding canonical evidence: {run_id}')
    r=json.loads(rp.read_text());method_type=r.get('method_type');method_ref=r.get('method_ref')
    bos=data.setdefault('extensions',{}).setdefault('businessos',{})
    prior=bos.get('run_ref');hist=list(bos.get('run_history_refs') or [])
    if prior and prior not in hist:hist.append(prior)
    rr=run_ref(business_id,run_id)
    if rr not in hist:hist.append(rr)
    bos.update({'run_ref':rr,'run_id':run_id,'run_method_type':method_type,'run_method_ref':method_ref,'run_binding':binding,'run_history_refs':hist})
    if method_type=='aura_playbook':bos['run_contract_id']=r.get('contract_id')
    else:bos.pop('run_contract_id',None)
    p.write_text(json.dumps(data,indent=2)+'\n');return True


def bind_evidence_paths(business_id,run_id,paths,binding='run_evidence'):
    return [str(p) for p in paths if bind_evidence_path(business_id,run_id,p,binding)]
