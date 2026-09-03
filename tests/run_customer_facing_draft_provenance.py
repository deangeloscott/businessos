#!/usr/bin/env python3
"""Optional Run provenance remains one-way without AURA inventing marketing-role semantics."""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from validate_run_completion import run_completion_errors

BID='customer-facing-draft-provenance';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID
WORKFLOW='marketing.assets.landing-page'


def req(c,m):
    if not c:raise AssertionError(m)
def run(*args,check=True):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def write_asset(customer_facing,origin=None,role='homepage_copy_draft'):
    artifact=BASE/'assets/homepage-draft.md';artifact.parent.mkdir(parents=True,exist_ok=True);artifact.write_text('# Homepage draft\n')
    asset={
        'id':f'ast_{BID}_homepage','object_type':'Asset','schema_version':'1.0.0','business_id':BID,
        'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],
        'asset_type':'homepage_copy_draft','business_role':role,
        'location_reference':str(artifact.relative_to(ROOT)),'version':'1','status':'draft',
        'extensions':{'businessos':{'customer_facing':customer_facing}}
    }
    if origin:asset['extensions']['businessos']['origin']=origin
    path=BASE/'assets'/f"{asset['id']}.json";path.write_text(json.dumps(asset,indent=2)+'\n');return path,artifact
def objs(path):return [(json.loads(path.read_text()),str(path.relative_to(ROOT)))]


def main():
    for path in [BASE,RUNS]:
        if path.exists():shutil.rmtree(path)
    try:
        run(S/'init_business.py',BID,'--name','Customer Facing Draft Provenance')
        rid=run(S/'create_run.py',BID,'Draft homepage copy','--workflow-id',WORKFLOW).stdout.strip()
        asset_path,artifact_path=write_asset(True,'preexisting','homepage_copy_draft')
        errors=run_completion_errors(BID,objs(asset_path));req(not errors,f'truthful outward draft should coexist with optional Workflow receipt: {errors}')
        completed=run(S/'complete_run.py',BID,rid,'--result',asset_path,'--result',artifact_path,'--summary','Drafted customer-facing homepage copy with truthful method provenance.',check=False)
        req(completed.returncode==0,f'optional Workflow receipt should complete without execution hierarchy: {completed.stdout+completed.stderr}')
        receipt=json.loads((RUNS/rid/'run.json').read_text()).get('continuity') or {}
        req(str(asset_path.relative_to(ROOT)) in receipt.get('result_refs',[]) and str(artifact_path.relative_to(ROOT)) in receipt.get('result_refs',[]),'completed receipt did not index material draft results')
        req(not (RUNS/rid/'contract-execution.json').exists(),'optional receipt recreated retired execution ledger')
        final_asset=json.loads(asset_path.read_text());bos=(final_asset.get('extensions') or {}).get('businessos') or {}
        req(not any(k.startswith('run_') or k=='run_ref' for k in bos),'optional receipt mutated canonical Asset with Run backlinks')

        # Intended audience/use is semantic organizational meaning supplied by the model/user.
        # AURA does not maintain a fixed ontology of which free-form marketing roles may be internal.
        internal={
            'id':f'ast_{BID}_internal','object_type':'Asset','schema_version':'1.0.0','business_id':BID,
            'created_at':'2026-08-01T00:00:00+00:00','updated_at':'2026-08-01T00:00:00+00:00','lineage':[],
            'asset_type':'working_note','business_role':'internal_working_draft',
            'location_reference':None,'version':'1','status':'draft',
            'extensions':{'businessos':{'customer_facing':False,'origin':'preexisting'}}
        }
        req(not run_completion_errors(BID,[(internal,f'instances/{BID}/assets/{internal["id"]}.json')]),'Run validation invented a semantic marketing-role allowlist')

        print('draft provenance regressions passed: optional Workflow receipt stays one-way and intended audience remains model/user-owned meaning')
    finally:
        for path in [BASE,RUNS]:
            if path.exists():shutil.rmtree(path)


if __name__=='__main__':main()
