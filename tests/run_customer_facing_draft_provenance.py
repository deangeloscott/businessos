#!/usr/bin/env python3
"""Unpublished outward drafts stay customer-facing; AURA playbook provenance stays truthful when used."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from validate_run_completion import run_completion_errors

BID='customer-facing-draft-provenance'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime'/'runs'/BID

def req(c,m):
    if not c: raise AssertionError(m)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def write_asset(rid,customer_facing,origin=None,role='internal_working_draft'):
    f=BASE/'assets/homepage-draft.md';f.parent.mkdir(parents=True,exist_ok=True);f.write_text('# Homepage draft\n')
    a={
      'id':f'ast_{BID}_homepage','object_type':'Asset','schema_version':'1.0.0','business_id':BID,
      'created_at':'2026-08-25T00:00:00+00:00','updated_at':'2026-08-25T00:00:00+00:00','lineage':[],
      'asset_type':'homepage_copy_draft','owner_system':'marketing-synthesis','business_role':role,
      'location_reference':str(f.relative_to(ROOT)),'version':'1','status':'draft',
      'extensions':{'businessos':{'customer_facing':customer_facing,'run_ref':f'runtime/runs/{BID}/{rid}','contract_chain':['marketing.landing-page.copy']}}
    }
    if origin:a['extensions']['businessos']['origin']=origin
    p=BASE/'assets'/f"{a['id']}.json";p.write_text(json.dumps(a,indent=2)+'\n')
    return p,f

def objs(p):return [(json.loads(p.read_text()),str(p.relative_to(ROOT)))]

def main():
    for p in [BASE,RUNS]:
        if p.exists(): shutil.rmtree(p)
    try:
        run(S/'init_business.py',BID,'--name','Customer Facing Draft Provenance')
        rid=run(S/'create_run.py',BID,'marketing.landing-page.copy','Draft homepage copy').stdout.strip()

        # A current Run-linked artifact cannot falsely claim to predate that work, and an
        # outward draft cannot become "internal" merely because it has not been published.
        ap,fp=write_asset(rid,False,'preexisting','internal_working_draft')
        completed=run(S/'complete_run.py',BID,rid,'--evidence',ap,'--evidence',fp,check=False)
        completion_output=completed.stderr+completed.stdout
        req(completed.returncode!=0 and 'cannot combine origin=' in completion_output,
            f'Run-linked object must not use contradictory origin provenance: {completion_output}')
        req('marketing-synthesis Asset may set customer_facing=false only' in completion_output,
            f'outward marketing draft must not opt out merely because unpublished: {completion_output}')
        req(json.loads((RUNS/rid/'run.json').read_text()).get('status')!='completed',
            'failed validation must restore the prior incomplete Run state')

        # When an AURA playbook Run is actually used, its root must honestly be a
        # customer-facing production root before it can claim provenance for this draft.
        a=json.loads(ap.read_text());bos=a['extensions']['businessos'];bos.pop('origin',None);bos['customer_facing']=True;ap.write_text(json.dumps(a,indent=2)+'\n')
        errs=run_completion_errors(BID,objs(ap))
        req(any('customer-facing Asset using an AURA playbook must reference a root marked artifact_role=customer_facing_production_root' in e for e in errs),
            f'customer-facing homepage draft rooted at a non-production AURA playbook must fail: {errs}')

        # Genuine pre-existing internal support material remains valid without any Run.
        hist={
          'id':f'ast_{BID}_historical','object_type':'Asset','schema_version':'1.0.0','business_id':BID,
          'created_at':'2026-08-01T00:00:00+00:00','updated_at':'2026-08-01T00:00:00+00:00','lineage':[],
          'asset_type':'internal_strategy_note','owner_system':'marketing-synthesis','business_role':'internal_strategy',
          'location_reference':None,'version':'1','status':'draft',
          'extensions':{'businessos':{'customer_facing':False,'origin':'preexisting'}}
        }
        req(not run_completion_errors(BID,[(hist,f'instances/{BID}/assets/{hist["id"]}.json')]),
            'genuine preexisting internal marketing support Asset should not require a Run')
        print('customer-facing draft provenance regressions passed')
    finally:
        for p in [BASE,RUNS]:
            if p.exists(): shutil.rmtree(p)

if __name__=='__main__':main()
