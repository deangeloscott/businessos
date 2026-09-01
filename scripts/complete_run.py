#!/usr/bin/env python3
"""Complete an optional organization-owned work receipt.

Every method uses the same continuity primitive. A receipt may reference material evidence,
results, decisions, and unresolved work, but canonical organization objects do not need to
point back to the receipt. Completion does not certify an execution graph, provider state,
permission state, launch readiness, or business outcome.
"""
import argparse, json
from jsonschema import Draft202012Validator

from _common import *
from validate_business import validate_business


def _material_ref(business_id,raw):
    value=str(raw).strip()
    if not value:raise ValueError('Empty material reference')
    idx=object_index(business_id)
    if value in idx:return storage_ref(idx[value][1])
    path=resolve_storage_ref(value)
    if not path.exists() or not path.is_file():raise ValueError(f'Material reference does not resolve: {raw}')
    return storage_ref(path)


def _refs(business_id,values):
    out=[]
    for raw in values or []:
        ref=_material_ref(business_id,raw)
        if ref not in out:out.append(ref)
    return out


def _validate_run(run):
    schema=json.loads((PRODUCT_ROOT/'core/schemas/runtime/run.schema.json').read_text())
    return [f'{list(e.path)}: {e.message}' for e in Draft202012Validator(schema).iter_errors(run)]


def complete_run(business_id,run_id,evidence=None,result_refs=None,decision_refs=None,summary=None,unresolved=None):
    rd=run_dir_path(business_id,run_id);rp=rd/'run.json'
    if not rp.exists():raise ValueError('Run file missing')
    run=json.loads(rp.read_text())
    if run.get('business_id')!=business_id or run.get('run_id')!=run_id:raise ValueError('Run identity mismatch')
    method_type=run.get('method_type') or ('aura_playbook' if run.get('contract_id') else 'ad_hoc')
    method_ref=run.get('method_ref') or run.get('contract_id')
    if method_type=='aura_playbook':
        contract_id=run.get('contract_id')
        installed={x.get('id') for x in load_registry().get('contracts',[]) if x.get('id')}
        if not contract_id or contract_id not in installed:raise ValueError(f'AURA playbook receipt references an unavailable playbook: {contract_id!r}')
        if method_ref not in {None,contract_id}:raise ValueError('AURA playbook method_ref must equal contract_id')
        method_ref=contract_id
    elif run.get('contract_id'):
        raise ValueError('Only aura_playbook Runs may carry contract_id')

    if run.get('status')=='completed':
        return {'run_id':run_id,'status':'completed','category':'already_completed','method_type':method_type,'continuity':run.get('continuity') or {}}
    if run.get('status')!='active':raise ValueError(f"Run is not active: {run.get('status')}")

    evidence_refs=_refs(business_id,evidence)
    results=_refs(business_id,result_refs)
    decisions=_refs(business_id,decision_refs)
    unresolved_clean=[]
    for item in unresolved or []:
        text=str(item).strip()
        if text and text not in unresolved_clean:unresolved_clean.append(text)
    summary_text=str(summary).strip() if summary is not None else ''

    current=dict(run.get('continuity') or {})
    def merged(key,new):return list(dict.fromkeys([*(current.get(key) or []),*new]))
    final_evidence=merged('evidence_refs',evidence_refs)
    final_results=merged('result_refs',results)
    final_decisions=merged('decision_refs',decisions)
    final_unresolved=list(dict.fromkeys([*(current.get('unresolved') or []),*unresolved_clean]))
    final_summary=summary_text or current.get('summary')
    if not (final_summary or final_evidence or final_results or final_decisions or final_unresolved):
        raise ValueError('Run completion requires material organizational meaning: a summary, evidence/result/decision reference, or unresolved item')

    snapshot=rp.read_bytes()
    try:
        ts=now();run['method_type']=method_type;run['method_ref']=method_ref
        run['status']='completed';run['updated_at']=ts
        run['continuity']={
            'format_version':'2.0','purpose':'organizational_work_receipt','state':'completed',
            'method_type':method_type,'method_ref':method_ref,'summary':final_summary,
            'evidence_refs':final_evidence,'result_refs':final_results,'decision_refs':final_decisions,
            'unresolved':final_unresolved,'completed_at':ts
        }
        schema_errors=_validate_run(run)
        if schema_errors:raise ValueError('Run schema invalid: '+'; '.join(schema_errors[:8]))
        rp.write_text(json.dumps(run,indent=2)+'\n')
        errors,warnings,counts=validate_business(business_id)
        if errors:raise ValueError('active business validation is not clean:\n- '+'\n- '.join(errors[:12]))
    except Exception:
        rp.write_bytes(snapshot)
        raise

    return {
        'run_id':run_id,'status':'completed','method_type':method_type,'method_ref':method_ref,
        'continuity':run['continuity'],
        'validation':{'errors':0,'warnings':warnings,'canonical_object_counts':counts},
        'rule':'This receipt references material continuity one-way. It does not mutate canonical results or certify playbook conformance, external execution, authorization, production readiness, or business outcomes.'
    }


def main():
    ap=argparse.ArgumentParser(description='Complete an optional AURA work receipt for any method.')
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
