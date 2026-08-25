#!/usr/bin/env python3
from _common import *
from run_provenance import bind_evidence_paths
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
        p=Path(e);p=p if p.is_absolute() else ROOT/p
        if not p.exists():raise SystemExit(f'Evidence path does not exist: {e}')
        rels.append(str(p.relative_to(ROOT)))
    if '.qa' in a.contract_id or a.contract_id.endswith('.qa'):
        ok=False
        for rel in rels:
            p=ROOT/rel
            if p.suffix.lower()=='.json':
                try:q=json.loads(p.read_text())
                except Exception:continue
                if q.get('contract_id')==a.contract_id and str(q.get('status','')).lower() in {'pass','passed'}:ok=True
        if not ok:raise SystemExit('QA contract completion requires a JSON pass record with matching contract_id and status=pass')
    bind_evidence_paths(a.business_id,a.run_id,rels,'subcontract_evidence')
    steps[a.contract_id]={'status':'completed','evidence_refs':rels,'note':a.note,'updated_at':now()}
    m['updated_at']=now();mp.write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps({'run_id':a.run_id,'contract_id':a.contract_id,'status':'completed','evidence_refs':rels},indent=2))
if __name__=='__main__':main()
