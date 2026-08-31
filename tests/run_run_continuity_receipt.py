#!/usr/bin/env python3
"""Regression coverage for Runs as lightweight organizational continuity receipts."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
BID='run-continuity-receipt'
BASE=ROOT/'instances'/BID
RUNS=ROOT/'runtime'/'runs'/BID
CONTRACT='customer-optimization.diagnosis.bottleneck-prioritization'


def req(cond,msg):
    if not cond:raise AssertionError(msg)

def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def write(rel,obj):
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n');return p


def main():
    for p in [BASE,RUNS]:
        if p.exists():shutil.rmtree(p)
    try:
        run(S/'init_business.py',BID,'--name','Run Continuity Receipt')
        rid=run(S/'create_run.py',BID,CONTRACT,'Diagnose the bounded activation bottleneck').stdout.strip()
        rp=RUNS/rid/'run.json'
        meta=json.loads(rp.read_text())
        continuity=meta.get('continuity') or {}
        req(meta.get('status')=='active','new Run should be active')
        req(continuity.get('purpose')=='organizational_work_receipt',f'Run should declare continuity purpose: {continuity}')
        req(continuity.get('state')=='active',f'new continuity receipt should be active: {continuity}')
        req(continuity.get('method_ref')==CONTRACT,f'continuity receipt should identify selected method: {continuity}')
        req(continuity.get('evidence_refs')==[] and continuity.get('result_refs')==[],f'new Run must not invent evidence/results: {continuity}')

        opp=write(f'instances/{BID}/decisions/opportunities/opp_{BID}_fixture.json',{
            'id':f'opp_{BID}_fixture','object_type':'Opportunity','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'title':'Activation bottleneck fixture','statement':'A bounded activation bottleneck requires review.','status':'candidate','objective_refs':[],'confidence':0.5,'extensions':{}
        })
        act=write(f'instances/{BID}/operations/action-packets/act_{BID}_fixture.json',{
            'id':f'act_{BID}_fixture','object_type':'ActionPacket','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'opportunity_ref':f'opp_{BID}_fixture','status':'proposed_not_executed','actions':[
                {'action_id':'review-fixture','description':'Review the bounded activation evidence.','executor_type':'HUMAN','expected_outputs':['review decision'],'status':'proposed'}],
            'extensions':{}
        })
        att=write(f'instances/{BID}/operations/attention/att_{BID}_fixture.json',{
            'id':f'att_{BID}_fixture','object_type':'AttentionItem','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'dedupe_key':'activation-fixture','attention_type':'review_needed','severity':'low','status':'open','title':'Review activation fixture',
            'reason':'The bounded regression fixture requires review.','first_seen':'2026-08-31T00:00:00+00:00','last_seen':'2026-08-31T00:00:00+00:00',
            'occurrence_count':1,'retention_class':'operational','extensions':{}
        })
        refs=[str(p.relative_to(ROOT)) for p in (opp,act,att)]
        cmd=[S/'complete_run.py',BID,rid]
        for ref in refs:cmd.extend(['--evidence',ref])
        completed=run(*cmd,check=False)
        req(completed.returncode==0,f'bounded Run should complete: {completed.stdout+completed.stderr}')
        result=json.loads(completed.stdout)
        meta=json.loads(rp.read_text());continuity=meta.get('continuity') or {}
        req(meta.get('status')=='completed','Run status should complete')
        req(continuity.get('state')=='completed',f'continuity receipt should complete with Run: {continuity}')
        req(continuity.get('method_ref')==CONTRACT,'selected method should remain stable in receipt')
        req(set(continuity.get('evidence_refs') or [])==set(refs),f'receipt should index real root evidence without copies: {continuity}')
        req(set(continuity.get('result_refs') or [])==set(refs),f'receipt should index Run-linked canonical results without creating summary objects: {continuity}')
        req(continuity.get('completed_at'),f'completed receipt should carry completion time: {continuity}')
        req(result.get('continuity')==continuity,'completion response and durable receipt should agree')

        for p in (opp,act,att):
            data=json.loads(p.read_text());bos=data.get('extensions',{}).get('businessos',{})
            req(bos.get('run_id')==rid and bos.get('run_contract_id')==CONTRACT,f'continuity refs must point at actually Run-bound canonical results: {p}')

        checked=run(S/'validate_business.py',BID,check=False)
        req(checked.returncode==0,f'continuity receipt must preserve valid business state: {checked.stdout+checked.stderr}')
        print('Run continuity receipt regressions passed: working memory stays external while material evidence/results are durably indexed')
    finally:
        for p in [BASE,RUNS]:
            if p.exists():shutil.rmtree(p)


if __name__=='__main__':main()
