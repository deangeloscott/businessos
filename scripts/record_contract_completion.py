#!/usr/bin/env python3
from _common import *
from run_provenance import bind_evidence_paths
from completion_evidence import contract_index, completion_spec, validate_evidence
import argparse,json

def _run_dir(bid,rid):return ROOT/'runtime/runs'/bid/rid

def main():
    ap=argparse.ArgumentParser(description='Record auditable completion evidence for one required subcontract in a BusinessOS Run.')
    ap.add_argument('business_id');ap.add_argument('run_id');ap.add_argument('contract_id');ap.add_argument('--evidence',action='append',default=[]);ap.add_argument('--note');a=ap.parse_args()
    d=_run_dir(a.business_id,a.run_id);mp=d/'contract-execution.json'
    if not mp.exists():raise SystemExit('Run contract-execution manifest missing; create the Run with scripts/create_run.py')
    m=json.loads(mp.read_text());steps=m.get('contracts',{})
    if a.contract_id not in steps:raise SystemExit(f'{a.contract_id} is not a declared required subcontract for this Run')
    if not a.evidence:raise SystemExit('Completed contracts require at least one --evidence path to an existing output/pass record')
    rels=[]
    for e in a.evidence:
        p=resolve_storage_ref(e)
        if not p.exists():raise SystemExit(f'Evidence path does not exist: {e}')
        rels.append(storage_ref(p))
    contract=contract_index().get(a.contract_id)
    if not contract:raise SystemExit(f'Installed contract metadata missing for {a.contract_id}')
    errors=validate_evidence(contract,rels,a.business_id,a.run_id,phase='subcontract',manifest=m)
    if errors:raise SystemExit('Cannot record subcontract completion; evidence does not satisfy contract completion profile:\n- '+'\n- '.join(errors))
    previous=steps.get(a.contract_id,{})
    steps[a.contract_id]={**previous,'status':'completed','evidence_refs':rels,'note':a.note,'updated_at':now(),'completion_evidence_spec':previous.get('completion_evidence_spec') or completion_spec(contract)}
    bind_evidence_paths(a.business_id,a.run_id,rels,'subcontract_evidence')
    m['updated_at']=now();mp.write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps({'run_id':a.run_id,'contract_id':a.contract_id,'status':'completed','evidence_refs':rels,'completion_evidence_spec':steps[a.contract_id]['completion_evidence_spec']},indent=2))
if __name__=='__main__':main()
