#!/usr/bin/env python3
"""Regression coverage for durable memory plus one-way optional work receipts."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
BID='run-continuity-receipt'
BASE=ROOT/'instances'/BID
RUNS=ROOT/'runtime'/'runs'/BID
RETIRED_RUN_BACKLINK_FIELDS={
    'run_ref','run_id','run_method_type','run_method_ref','run_contract_id',
    'run_binding','run_history_refs','contract_chain'
}


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

        # External work may use an optional AURA receipt without pretending that an AURA
        # playbook executed it.
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

        # Durable organizational meaning is persisted through the ordinary memory primitive,
        # independently from the receipt.
        payload=rd/'work'/'memory.json'
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
        remembered=run(S/'remember.py',BID,'--input',payload,check=False)
        req(remembered.returncode==0,f'ordinary canonical memory failed: {remembered.stdout+remembered.stderr}')
        result=json.loads(remembered.stdout);rows=result.get('objects') or []
        req(len(rows)==1 and rows[0].get('object_type')=='DecisionRecord',f'wrong memory result: {result}')
        decision_path=ROOT/rows[0]['path'];decision=load(decision_path)
        bos=decision.get('extensions',{}).get('businessos',{}) if isinstance(decision.get('extensions'),dict) else {}
        req(not (RETIRED_RUN_BACKLINK_FIELDS & set(bos)),f'ordinary memory was coupled to a receipt: {bos}')
        before=decision_path.read_bytes()

        # The receipt may point to already-valid durable meaning. Closing it must not write
        # method/Run bookkeeping back into that canonical object.
        completed=run(
            S/'complete_run.py',BID,rid,
            '--result',rows[0]['path'],
            '--decision',rows[0]['path'],
            '--summary','Recorded the bounded organizational decision.',
            '--unresolved','Revisit only if materially better evidence appears.',
            check=False,
        )
        req(completed.returncode==0,f'general Run completion failed: {completed.stdout+completed.stderr}')
        meta=load(rp);continuity=meta.get('continuity') or {}
        req(meta.get('status')=='completed' and continuity.get('state')=='completed',f'Run/receipt did not complete: {meta}')
        req(continuity.get('method_type')=='external_skill' and continuity.get('method_ref')=='decision-review-skill',f'receipt lost method provenance: {continuity}')
        req(rows[0]['path'] in continuity.get('result_refs',[]),f'receipt omitted durable result: {continuity}')
        req(rows[0]['path'] in continuity.get('decision_refs',[]),f'receipt omitted durable decision: {continuity}')
        req(continuity.get('summary') and continuity.get('unresolved'),f'receipt omitted material continuity: {continuity}')
        req(decision_path.read_bytes()==before,'completing a receipt mutated canonical organization memory')
        decision=load(decision_path);bos=decision.get('extensions',{}).get('businessos',{}) if isinstance(decision.get('extensions'),dict) else {}
        req(not (RETIRED_RUN_BACKLINK_FIELDS & set(bos)),f'receipt completion reintroduced canonical Run backlinks: {bos}')

        for rel in ['scripts/persist_run_results.py','scripts/run_provenance.py','scripts/run_lifecycle.py','scripts/reconcile_runs.py']:
            req(not (ROOT/rel).exists(),f'retired receipt coupling helper reappeared: {rel}')

        checked=run(S/'validate_business.py',BID,check=False)
        req(checked.returncode==0,f'completed organizational receipt must validate: {checked.stdout+checked.stderr}')
        print('Run continuity regressions passed: durable memory stands alone and optional receipts reference it one-way')
    finally:
        for p in [BASE,RUNS]:
            if p.exists():shutil.rmtree(p)


if __name__=='__main__':main()
