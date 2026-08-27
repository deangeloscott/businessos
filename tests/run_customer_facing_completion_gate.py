#!/usr/bin/env python3
"""RC15: customer-facing production roots require a canonical governed Asset before completion."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'
BID='customer-facing-completion-gate'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime'/'runs'/BID

def run(*args,check=False):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def req(c,m):
    if not c: raise AssertionError(m)

def main():
    for p in [BASE,RUNS]:
        if p.exists(): shutil.rmtree(p)
    try:
        req(run(S/'init_business.py',BID,'--name','Completion Gate').returncode==0,'init failed')
        rid=run(S/'create_run.py',BID,'marketing.assets.landing-page','Draft landing page').stdout.strip()
        prior=BASE/'assets/prior.md';prior.parent.mkdir(parents=True,exist_ok=True);prior.write_text('Prior imported page used only as the QA fixture target.\n')
        prior_asset={'id':f'ast_{BID}_prior','object_type':'Asset','business_id':BID,'owner_system':'marketing-synthesis',
            'asset_type':'landing-page','business_role':'customer_facing_production','version':'1','status':'draft',
            'lineage':[],'location_reference':str(prior.relative_to(ROOT)),'extensions':{'businessos':{'origin':'preexisting'}}}
        (BASE/'assets'/f"{prior_asset['id']}.json").write_text(json.dumps(prior_asset)+'\n')
        # Mark declared subcontracts complete with structurally valid fixture evidence. This
        # regression is testing the separate root-Asset gate, not QA-content quality.
        m=json.loads((RUNS/rid/'contract-execution.json').read_text())
        for cid in m.get('required_subcontracts',[]):
            e=RUNS/rid/'artifacts'/((cid.replace('.','-'))+'.json');e.parent.mkdir(parents=True,exist_ok=True)
            payload=(
                {'status':'pass','contract_id':cid,'tested_asset':prior_asset['id'],'tested_version':'1',
                 'checks':[{'check':'fixture target inspection','status':'pass','method':'Read the saved prior Asset text from its location reference','finding':'The prior fixture contains one complete visible sentence.'}],
                 'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]}
                if '.qa' in cid or cid.endswith('.qa') else
                {'id':f'ast_{BID}_{cid.replace(".","-")}','object_type':'Asset','business_id':BID,'status':'completed','contract_id':cid,'extensions':{}}
            )
            e.write_text(json.dumps(payload)+'\n')
            r=run(S/'record_contract_completion.py',BID,rid,cid,'--evidence',str(e.relative_to(ROOT)))
            req(r.returncode==0,f'completion recording failed {cid}: {r.stderr or r.stdout}')
        draft=BASE/'assets/homepage.md';draft.parent.mkdir(parents=True,exist_ok=True);draft.write_text('CrewBeacon helps teams prioritize inbound leads.\n')
        # Loose file alone must not complete the root.
        r=run(S/'complete_run.py',BID,rid,'--evidence',str(draft.relative_to(ROOT)))
        req(r.returncode!=0 and 'canonical customer-facing Asset' in (r.stderr+r.stdout),f'loose file should be rejected: {r.stderr+r.stdout}')
        print('customer-facing completion gate regression passed')
    finally:
        for p in [BASE,RUNS]:
            if p.exists(): shutil.rmtree(p)
if __name__=='__main__': main()
