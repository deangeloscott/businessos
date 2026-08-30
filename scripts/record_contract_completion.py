#!/usr/bin/env python3
from _common import *
from run_provenance import bind_evidence_paths
from completion_evidence import contract_index, completion_spec, validate_evidence
import argparse,json

def _run_dir(bid,rid):return ROOT/'runtime/runs'/bid/rid

def record_contract_completion(business_id,run_id,contract_id,evidence,note=None):
    d=_run_dir(business_id,run_id);mp=d/'contract-execution.json'
    if not mp.exists():raise ValueError('Run contract-execution manifest missing; create the Run with scripts/create_run.py')
    m=json.loads(mp.read_text());steps=m.get('contracts',{})
    if contract_id not in steps:raise ValueError(f'{contract_id} is not a declared required subcontract for this Run')
    if not evidence:raise ValueError('Completed contracts require at least one evidence path to an existing output/pass record')
    rels=[]
    for e in evidence:
        p=resolve_storage_ref(e)
        if not p.exists():raise ValueError(f'Evidence path does not exist: {e}')
        rels.append(storage_ref(p))
    contract=contract_index().get(contract_id)
    if not contract:raise ValueError(f'Installed contract metadata missing for {contract_id}')
    errors=validate_evidence(contract,rels,business_id,run_id,phase='subcontract',manifest=m)
    if errors:raise ValueError('Cannot record subcontract completion; evidence does not satisfy contract completion profile:\n- '+'\n- '.join(errors))
    previous=steps.get(contract_id,{})
    steps[contract_id]={**previous,'status':'completed','evidence_refs':rels,'note':note,'updated_at':now(),'completion_evidence_spec':previous.get('completion_evidence_spec') or completion_spec(contract)}
    bind_evidence_paths(business_id,run_id,rels,'subcontract_evidence')
    m['updated_at']=now();mp.write_text(json.dumps(m,indent=2)+'\n')
    return {'run_id':run_id,'contract_id':contract_id,'status':'completed','evidence_refs':rels,'completion_evidence_spec':steps[contract_id]['completion_evidence_spec']}

def main():
    ap=argparse.ArgumentParser(description='Record auditable completion evidence for one required subcontract in a BusinessOS Run.')
    ap.add_argument('business_id');ap.add_argument('run_id');ap.add_argument('contract_id');ap.add_argument('--evidence',action='append',default=[]);ap.add_argument('--note');a=ap.parse_args()
    try:result=record_contract_completion(a.business_id,a.run_id,a.contract_id,a.evidence,a.note)
    except (ValueError,json.JSONDecodeError) as e:raise SystemExit(str(e))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
