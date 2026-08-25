#!/usr/bin/env python3
"""RC12 regressions for bootstrap-generated IDs and complete canonical-reference parsing."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from validate_references import reference_errors

BID='bootstrap-reference-id-regression'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime'/'runs'/BID

def req(c,m):
    if not c: raise AssertionError(m)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    if RUNS.exists(): shutil.rmtree(RUNS)
    tmp=ROOT/'runtime'/BID
    if tmp.exists(): shutil.rmtree(tmp)
    try:
        run(S/'init_business.py',BID,'--name','Bootstrap Reference ID Regression')
        tmp.mkdir(parents=True,exist_ok=True)
        statements=[
            'Amount values must be numeric decimals; negative values represent outflows and positive values represent inflows',
            'The fixture contains no pricing, revenue, ARR, LTV, CAC, margin, churn, retention, support cost, customer value, engineering effort, or measured intervention lift; do not infer them',
        ]
        facts={'claim_constraints':statements}
        facts_path=tmp/'facts.json'; facts_path.write_text(json.dumps(facts,indent=2)+'\n')
        source_path=tmp/'source.txt'; source_path.write_text('\n'.join(x+'.' for x in statements)+'\n')
        run(S/'bootstrap_explicit_context.py',BID,'--facts-file',facts_path,'--source-file',source_path,'--initialization-only')
        claim_files=sorted((BASE/'context'/'claims').glob('*.json'))
        req(len(claim_files)==2,f'expected two claims, got {len(claim_files)}')
        ids=[json.loads(p.read_text())['id'] for p in claim_files]
        req(all(not x.endswith(('-', '_')) for x in ids),f'bootstrap must not truncate generated IDs onto a separator: {ids}')
        errs=reference_errors(BID)
        req(not errs,f'fresh bootstrap output must not create false unresolved refs: {errs}')

        # Migration safety: schema-valid historical/custom IDs may end in '-' or '_'.
        # Reference extraction must preserve the entire ID instead of dropping the final separator.
        legacy='clm_'+BID+'_legacy-'
        (BASE/'context'/'claims'/f'{legacy}.json').write_text(json.dumps({'id':legacy,'object_type':'BusinessClaim','business_id':BID},indent=2)+'\n')
        holder=BASE/'intelligence'/'observations'/f'obs_{BID}_holder.json'
        holder.write_text(json.dumps({'id':f'obs_{BID}_holder','object_type':'Observation','business_id':BID,'lineage':[legacy]},indent=2)+'\n')
        errs=reference_errors(BID)
        req(not errs,f'reference parser must preserve trailing separators in existing valid IDs: {errs}')
        print('bootstrap/reference ID regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        if RUNS.exists(): shutil.rmtree(RUNS)
        if tmp.exists(): shutil.rmtree(tmp)

if __name__=='__main__': main()
