#!/usr/bin/env python3
"""Regression coverage for durable organizational work receipts without control-plane artifacts."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
BID='run-continuity-receipt'
BASE=ROOT/'instances'/BID
RUNS=ROOT/'runtime'/'runs'/BID


def req(cond,msg):
    if not cond:raise AssertionError(msg)

def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)

def load(path):return json.loads(Path(path).read_text())


def main():
    for p in [BASE,RUNS]:
        if p.exists():shutil.rmtree(p)
    try:
        run(S/'init_business.py',BID,'--name','Run Continuity Receipt')

        # External work may use AURA as organizational memory without pretending it
        # executed an AURA playbook.
        rid=run(
            S/'create_run.py',BID,'Review a bounded organizational choice',
            '--method-type','external_skill','--method-ref','decision-review-skill',
        ).stdout.strip()
        rd=RUNS/rid;rp=rd/'run.json';meta=load(rp);continuity=meta.get('continuity') or {}
        req(meta.get('method_type')=='external_skill',f'wrong method type: {meta}')
        req(meta.get('contract_id') is None,f'external work fabricated contract: {meta}')
        req(not (rd/'contract-execution.json').exists(),'external work fabricated contract execution')
        req(continuity.get('purpose')=='organizational_work_receipt',f'missing receipt purpose: {continuity}')
        req(continuity.get('state')=='active',f'new receipt should be active: {continuity}')

        # Persist real organizational meaning through the same canonical interface used
        # by AURA playbook work. The caller supplies meaning; AURA supplies identity,
        # storage, provenance, and schema validation.
        payload=rd/'work'/'results.json'
        payload.write_text(json.dumps({'objects':[{
            'key':'decision',
            'object_type':'DecisionRecord',
            'content':{
                'decision':'Use the evidence-backed option for this bounded fixture.',
                'made_by':'test-operator',
                'made_at':'2026-08-31T00:00:00+00:00',
                'applies_to':['fixture'],
                'basis_refs':[],
                'status':'current',
                'notes':'Regression fixture for organization-owned continuity.'
            }
        }]},indent=2)+'\n')
        persisted=run(S/'persist_run_results.py',BID,rid,'--input',payload,check=False)
        req(persisted.returncode==0,f'general canonical persistence failed: {persisted.stdout+persisted.stderr}')
        result=json.loads(persisted.stdout);rows=result.get('objects') or []
        req(result.get('method_type')=='external_skill' and len(rows)==1,f'wrong persistence result: {result}')
        decision_path=ROOT/rows[0]['path'];decision=load(decision_path)
        bos=decision.get('extensions',{}).get('businessos',{})
        req(decision.get('object_type')=='DecisionRecord',f'wrong canonical result: {decision}')
        req(bos.get('run_id')==rid and bos.get('run_method_type')=='external_skill',f'method provenance missing: {bos}')
        req(bos.get('run_method_ref')=='decision-review-skill',f'method reference missing: {bos}')
        req('run_contract_id' not in bos and 'contract_chain' not in bos,f'general work fabricated contract provenance: {bos}')

        # Completion indexes only material organizational meaning, not transcripts,
        # tool calls, hidden reasoning, or a fake contract-completion ledger.
        completed=run(
            S/'complete_run.py',BID,rid,
            '--result',rows[0]['path'],
            '--decision',rows[0]['path'],
            '--summary','Recorded the bounded organizational decision and its provenance.',
            '--unresolved','Revisit only if materially better evidence appears.',
            check=False,
        )
        req(completed.returncode==0,f'general Run completion failed: {completed.stdout+completed.stderr}')
        meta=load(rp);continuity=meta.get('continuity') or {}
        req(meta.get('status')=='completed' and continuity.get('state')=='completed',f'Run/receipt did not complete: {meta}')
        req(continuity.get('method_type')=='external_skill',f'receipt lost method type: {continuity}')
        req(rows[0]['path'] in continuity.get('result_refs',[]),f'receipt omitted durable result: {continuity}')
        req(rows[0]['path'] in continuity.get('decision_refs',[]),f'receipt omitted durable decision: {continuity}')
        req(continuity.get('summary') and continuity.get('unresolved'),f'receipt omitted material continuity: {continuity}')
        req(not (rd/'contract-execution.json').exists(),'completion created fake AURA playbook execution')

        checked=run(S/'validate_business.py',BID,check=False)
        req(checked.returncode==0,f'completed organizational receipt must validate: {checked.stdout+checked.stderr}')
        print('Run continuity regressions passed: canonical organizational meaning persists without legacy control-plane or fake contract execution')
    finally:
        for p in [BASE,RUNS]:
            if p.exists():shutil.rmtree(p)


if __name__=='__main__':main()
