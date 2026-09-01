#!/usr/bin/env python3
"""Unpublished outward drafts stay customer-facing; optional method provenance stays truthful."""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from validate_run_completion import run_completion_errors

BID='customer-facing-draft-provenance';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID

def req(c,m):
    if not c:raise AssertionError(m)
def run(*args,check=True):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def write_asset(rid,customer_facing,origin=None,role='internal_working_draft'):
    artifact=BASE/'assets/homepage-draft.md';artifact.parent.mkdir(parents=True,exist_ok=True);artifact.write_text('# Homepage draft\n')
    asset={'id':f'ast_{BID}_homepage','object_type':'Asset','schema_version':'1.0.0','business_id':BID,'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],'asset_type':'homepage_copy_draft','owner_system':'marketing-synthesis','business_role':role,'location_reference':str(artifact.relative_to(ROOT)),'version':'1','status':'draft','extensions':{'businessos':{'customer_facing':customer_facing,'run_ref':f'runtime/runs/{BID}/{rid}','run_id':rid,'run_method_type':'aura_playbook','run_method_ref':'marketing.landing-page.copy','run_contract_id':'marketing.landing-page.copy'}}}
    if origin:asset['extensions']['businessos']['origin']=origin
    path=BASE/'assets'/f"{asset['id']}.json";path.write_text(json.dumps(asset,indent=2)+'\n');return path,artifact

def objs(path):return [(json.loads(path.read_text()),str(path.relative_to(ROOT)))]

def main():
    for path in [BASE,RUNS]:
        if path.exists():shutil.rmtree(path)
    try:
        run(S/'init_business.py',BID,'--name','Customer Facing Draft Provenance')
        rid=run(S/'create_run.py',BID,'Draft homepage copy','--contract-id','marketing.landing-page.copy').stdout.strip()
        asset_path,artifact_path=write_asset(rid,False,'preexisting','internal_working_draft')
        completed=run(S/'complete_run.py',BID,rid,'--result',asset_path,'--result',artifact_path,'--summary','Drafted homepage copy.',check=False);output=completed.stderr+completed.stdout
        req(completed.returncode!=0,'misclassified outward marketing draft should fail organization validation')
        req('cannot combine origin=' not in output,f'preexisting origin must remain compatible with later truthful receipt provenance: {output}')
        req('marketing-synthesis Asset may set customer_facing=false only' in output,f'outward marketing draft must not opt out merely because unpublished: {output}')
        req(json.loads((RUNS/rid/'run.json').read_text()).get('status')!='completed','failed validation must restore active receipt state')

        asset=json.loads(asset_path.read_text());asset['extensions']['businessos']['customer_facing']=True;asset_path.write_text(json.dumps(asset,indent=2)+'\n')
        errors=run_completion_errors(BID,objs(asset_path));req(not errors,f'truthful customer-facing draft should coexist with active optional playbook receipt: {errors}')
        completed=run(S/'complete_run.py',BID,rid,'--result',asset_path,'--result',artifact_path,'--summary','Drafted customer-facing homepage copy with truthful method provenance.',check=False)
        req(completed.returncode==0,f'truthful leaf-playbook receipt should complete without root/subcontract hierarchy: {completed.stdout+completed.stderr}')
        receipt=json.loads((RUNS/rid/'run.json').read_text()).get('continuity') or {}
        req(str(asset_path.relative_to(ROOT)) in receipt.get('result_refs',[]) and str(artifact_path.relative_to(ROOT)) in receipt.get('result_refs',[]),'completed receipt did not index material draft results')
        req(not (RUNS/rid/'contract-execution.json').exists(),'leaf playbook receipt recreated execution ledger')

        historical={'id':f'ast_{BID}_historical','object_type':'Asset','schema_version':'1.0.0','business_id':BID,'created_at':'2026-08-01T00:00:00+00:00','updated_at':'2026-08-01T00:00:00+00:00','lineage':[],'asset_type':'internal_strategy_note','owner_system':'marketing-synthesis','business_role':'internal_strategy','location_reference':None,'version':'1','status':'draft','extensions':{'businessos':{'customer_facing':False,'origin':'preexisting'}}}
        req(not run_completion_errors(BID,[(historical,f'instances/{BID}/assets/{historical["id"]}.json')]),'genuine preexisting internal support Asset should not require a Run')
        print('customer-facing draft provenance regressions passed: intended audience and optional method provenance remain independent')
    finally:
        for path in [BASE,RUNS]:
            if path.exists():shutil.rmtree(path)

if __name__=='__main__':main()
