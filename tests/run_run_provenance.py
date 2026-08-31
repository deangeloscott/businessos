#!/usr/bin/env python3
"""Regression coverage for AURA work receipts and conditional SOP conformance.

The invariant is deliberately architectural rather than compatibility-oriented:
- every method may have a truthful organization-owned Run/work receipt;
- external Skills, model-created methods, and ad-hoc work do not fabricate AURA
  contract execution;
- selecting an AURA playbook opts into its stronger completion/evidence rules.
"""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'scripts'
BID='run-provenance-regression'
BASE=ROOT/'instances'/BID
RUNS=ROOT/'runtime'/'runs'/BID


def req(condition,message):
    if not condition:
        raise AssertionError(message)


def run(*args,check=True):
    return subprocess.run(
        [sys.executable,*map(str,args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=check,
    )


def load(path):
    return json.loads(Path(path).read_text())


def write(path,text):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text)
    return path


def create_general(method_type,task,method_ref=None):
    args=[S/'create_run.py',BID,task,'--method-type',method_type]
    if method_ref:
        args.extend(['--method-ref',method_ref])
    rid=run(*args).stdout.strip()
    rd=RUNS/rid
    state=load(rd/'run.json')
    req(state['method_type']==method_type,f'{method_type} Run method_type mismatch: {state}')
    req(state.get('contract_id') is None,f'{method_type} Run fabricated contract_id: {state}')
    req(state.get('completion_policy_ref') is None,f'{method_type} Run fabricated SOP completion policy: {state}')
    req(not (rd/'contract-execution.json').exists(),f'{method_type} Run fabricated contract execution')
    return rid,rd,state


def complete_general(rid,rd,method_type):
    evidence=write(rd/'artifacts'/'evidence.txt',f'{method_type} evidence\n')
    result=write(rd/'artifacts'/'result.md',f'# {method_type} result\n\nUseful bounded work result.\n')
    completed=run(
        S/'complete_run.py',BID,rid,
        '--evidence',str(evidence.relative_to(ROOT)),
        '--result',str(result.relative_to(ROOT)),
        '--summary',f'Completed useful {method_type} work and preserved its material result.',
        '--unresolved','Revisit only if new organizational evidence materially changes the result.',
    )
    payload=json.loads(completed.stdout)
    req(payload.get('status')=='completed',f'{method_type} Run did not complete: {payload}')
    state=load(rd/'run.json')
    receipt=state.get('continuity') or {}
    req(state.get('status')=='completed',f'{method_type} Run state not completed: {state}')
    req(receipt.get('purpose')=='organizational_work_receipt',f'{method_type} receipt purpose missing: {receipt}')
    req(receipt.get('method_type')==method_type,f'{method_type} receipt method mismatch: {receipt}')
    req(str(evidence.relative_to(ROOT)) in receipt.get('evidence_refs',[]),f'{method_type} receipt omitted evidence: {receipt}')
    req(str(result.relative_to(ROOT)) in receipt.get('result_refs',[]),f'{method_type} receipt omitted result: {receipt}')
    req(receipt.get('summary'),f'{method_type} receipt omitted summary: {receipt}')
    req(receipt.get('unresolved'),f'{method_type} receipt omitted unresolved work: {receipt}')
    req(not (rd/'contract-execution.json').exists(),f'{method_type} completion created fake contract execution')


def main():
    if BASE.exists():
        shutil.rmtree(BASE)
    if RUNS.exists():
        shutil.rmtree(RUNS)
    try:
        run(S/'init_business.py',BID,'--name','Run Provenance Regression')

        # Non-AURA methods preserve organizational continuity without pretending to
        # execute an AURA playbook or manufacturing contract-completion state.
        for method_type,method_ref in [
            ('external_skill','competitor-research-skill'),
            ('model_created','model-created:conversion-diagnostic'),
            ('ad_hoc',None),
        ]:
            rid,rd,_=create_general(method_type,f'Bounded {method_type} fixture',method_ref)
            complete_general(rid,rd,method_type)

        # Selecting an AURA playbook is the explicit opt-in to its stronger
        # contract/evidence conformance machinery.
        contract_id='seo.diagnosis.detectors.indexing'
        rid=run(
            S/'create_run.py',BID,'Inspect bounded indexing evidence',
            '--contract-id',contract_id,
        ).stdout.strip()
        rd=RUNS/rid
        state=load(rd/'run.json')
        manifest=load(rd/'contract-execution.json')
        req(state.get('method_type')=='aura_playbook',f'AURA playbook Run method mismatch: {state}')
        req(state.get('contract_id')==contract_id,f'AURA playbook Run contract mismatch: {state}')
        req(state.get('completion_policy_ref'),f'AURA playbook Run omitted completion policy: {state}')
        req(manifest.get('root_contract_id')==contract_id,f'AURA playbook manifest root mismatch: {manifest}')

        inspected=write(rd/'artifacts'/'inspection.txt','bounded indexing inspection evidence\n')
        nofinding=rd/'artifacts'/'no-finding.json'
        nofinding.write_text(json.dumps({
            'contract_id':contract_id,
            'status':'completed',
            'result':'no_finding',
            'checks_performed':[{'check':'bounded index-state comparison','status':'pass'}],
            'evidence_refs':[str(inspected.relative_to(ROOT))],
        },indent=2)+'\n')
        completed=run(
            S/'complete_run.py',BID,rid,
            '--evidence',str(nofinding.relative_to(ROOT)),
            check=False,
        )
        req(completed.returncode==0,f'AURA playbook completion failed: {completed.stdout+completed.stderr}')
        state=load(rd/'run.json')
        manifest=load(rd/'contract-execution.json')
        receipt=state.get('continuity') or {}
        req(state.get('status')=='completed',f'AURA playbook Run not completed: {state}')
        req(manifest.get('root_status')=='completed',f'AURA playbook conformance not completed: {manifest}')
        req(receipt.get('method_type')=='aura_playbook',f'AURA receipt lost method type: {receipt}')
        req(receipt.get('method_ref')==contract_id,f'AURA receipt lost playbook ref: {receipt}')
        req(str(nofinding.relative_to(ROOT)) in receipt.get('evidence_refs',[]),f'AURA receipt omitted root evidence: {receipt}')

        # Whole-business integrity must accept both kinds of completed work together.
        # Explicit Business context is an onboarding concern and intentionally not part
        # of this Run/provenance regression.
        validated=run(S/'validate_business.py',BID,check=False)
        req(validated.returncode==0,f'combined work-receipt validation failed: {validated.stdout+validated.stderr}')

        # Deleted authority/control-plane concepts must not be recreated as a side effect
        # of ordinary work receipt creation or completion.
        for retired in [
            ROOT/'core'/'schemas'/'action'/'action-packet.schema.json',
            ROOT/'core'/'schemas'/'action'/'approval.schema.json',
            ROOT/'core'/'policies'/'approval.md',
            ROOT/'core'/'policies'/'risk.md',
            ROOT/'core'/'policies'/'autonomy.md',
        ]:
            req(not retired.exists(),f'retired control-plane artifact reappeared: {retired.relative_to(ROOT)}')

        print('Run work-receipt and conditional AURA playbook provenance regressions passed')
    finally:
        if BASE.exists():
            shutil.rmtree(BASE)
        if RUNS.exists():
            shutil.rmtree(RUNS)


if __name__=='__main__':
    main()
