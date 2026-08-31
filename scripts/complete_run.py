#!/usr/bin/env python3
"""Complete an organization-owned work receipt.

AURA playbook Runs delegate to the preserved SOP-specific completion engine. Other
methods complete through a small truth/integrity path that records material evidence,
results, decisions, unresolved work, and a concise summary without inventing contract
execution or SOP conformance.
"""
from pathlib import Path
import argparse, json

from _common import *
from complete_sop_run import complete_run as complete_sop_run, snapshot_files, restore_files
from validate_business import validate_business


def _material_ref(business_id,raw):
    """Normalize a canonical object id or resolvable storage reference to durable storage."""
    value=str(raw).strip()
    if not value:raise ValueError('Empty material reference')
    idx=object_index(business_id)
    if value in idx:
        return storage_ref(idx[value][1])
    path=resolve_storage_ref(value)
    if not path.exists() or not path.is_file():raise ValueError(f'Material reference does not resolve: {raw}')
    return storage_ref(path)


def _refs(business_id,values):
    out=[]
    for raw in values or []:
        ref=_material_ref(business_id,raw)
        if ref not in out:out.append(ref)
    return out


def complete_run(business_id,run_id,evidence=None,result_refs=None,decision_refs=None,summary=None,unresolved=None):
    run_dir=run_dir_path(business_id,run_id);run_path=run_dir/'run.json';manifest=run_dir/'contract-execution.json'
    if not run_path.exists():raise ValueError('Run file missing')

    # Selected AURA SOPs keep their strong contract-specific completion/evidence rules.
    if manifest.exists():
        return complete_sop_run(business_id,run_id,evidence or [])

    run=json.loads(run_path.read_text())
    if run.get('business_id')!=business_id or run.get('run_id')!=run_id:raise ValueError('Run identity mismatch')
    if run.get('status')!='active':raise ValueError(f"Run is not active: {run.get('status')}")
    method_type=run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')
    if method_type=='aura_playbook':
        raise ValueError('AURA playbook Run is missing its contract-execution manifest')

    evidence_refs=_refs(business_id,evidence)
    results=_refs(business_id,result_refs)
    decisions=_refs(business_id,decision_refs)
    unresolved_clean=[]
    for item in unresolved or []:
        text=str(item).strip()
        if text and text not in unresolved_clean:unresolved_clean.append(text)
    summary_text=str(summary).strip() if summary is not None else ''
    if not (summary_text or evidence_refs or results or decisions or unresolved_clean):
        raise ValueError('General Run completion requires material organizational meaning: provide a summary, evidence/result/decision reference, or unresolved item')

    before=run_path.read_bytes();ts=now()
    continuity=dict(run.get('continuity') or {})
    continuity.update({
        'format_version':'2.0','purpose':'organizational_work_receipt','state':'completed',
        'method_type':method_type,'method_ref':run.get('method_ref'),
        'summary':summary_text or continuity.get('summary'),
        'evidence_refs':evidence_refs,'result_refs':results,'decision_refs':decisions,'unresolved':unresolved_clean,
        'completed_at':ts,'superseded_by_run_id':None
    })
    run['method_type']=method_type
    run.setdefault('method_ref',run.get('contract_id'))
    run['status']='completed';run['updated_at']=ts;run['continuity']=continuity
    try:
        run_path.write_text(json.dumps(run,indent=2)+'\n')
        errors,warnings,counts=validate_business(business_id)
        if errors:raise ValueError('active business validation is not clean:\n- '+'\n- '.join(errors))
    except Exception:
        run_path.write_bytes(before)
        raise
    return {
        'run_id':run_id,'status':'completed','method_type':method_type,
        'continuity':continuity,
        'validation':{'errors':0,'warnings':warnings,'canonical_object_counts':counts}
    }


def main():
    ap=argparse.ArgumentParser(description='Complete a Run. AURA SOP Runs use SOP conformance; all other methods persist a truthful organizational work receipt.')
    ap.add_argument('business_id');ap.add_argument('run_id')
    ap.add_argument('--evidence',action='append',default=[])
    ap.add_argument('--result',action='append',default=[])
    ap.add_argument('--decision',action='append',default=[])
    ap.add_argument('--summary')
    ap.add_argument('--unresolved',action='append',default=[])
    a=ap.parse_args()
    try:result=complete_run(a.business_id,a.run_id,a.evidence,a.result,a.decision,a.summary,a.unresolved)
    except ValueError as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
