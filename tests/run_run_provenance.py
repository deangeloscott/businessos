#!/usr/bin/env python3
"""Regression: every method uses the same simple optional AURA work-receipt primitive."""
from pathlib import Path
import json,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts'
BID='run-provenance-regression';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID


def req(condition,message):
    if not condition:raise AssertionError(message)
def run(*args,check=True):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def load(path):return json.loads(Path(path).read_text())
def write(path,text):path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text);return path


def create_and_complete(method_type,task,method_ref=None,playbook_id=None,workflow_id=None):
    args=[S/'create_run.py',BID,task]
    if playbook_id:args.extend(['--playbook-id',playbook_id])
    elif workflow_id:args.extend(['--workflow-id',workflow_id])
    else:
        args.extend(['--method-type',method_type])
        if method_ref:args.extend(['--method-ref',method_ref])
    rid=run(*args).stdout.strip();rd=RUNS/rid;state=load(rd/'run.json')
    req(state['method_type']==method_type,f'{method_type} Run method mismatch: {state}')
    req(state.get('completion_policy_ref') is None,f'{method_type} Run recreated completion-policy machinery')
    req(not (rd/'contract-execution.json').exists(),f'{method_type} Run recreated an execution ledger')
    req((rd/'artifacts').is_dir() and (rd/'work').is_dir(),'receipt should expose only useful local artifact/work spaces')
    req(not (rd/'logs').exists() and not (rd/'checkpoints').exists(),'receipt recreated host/runtime log or checkpoint ownership')
    retired_relationship_fields={'correlation_id','causation_id','root_run_id','parent_run_id','run_role','supersedes_run_id','superseded_by_run_id','lifecycle_reason'}
    req(not (retired_relationship_fields & set(state)),f'{method_type} receipt recreated relationship lifecycle fields')
    req('contract_id' not in state,'Run receipt retained flattened contract provenance')

    if playbook_id:
        req(state.get('playbook_id')==playbook_id and state.get('workflow_id') is None and state.get('method_ref')==playbook_id,'AURA Playbook receipt lost truthful provenance')
    elif workflow_id:
        req(state.get('workflow_id')==workflow_id and state.get('playbook_id') is None and state.get('method_ref')==workflow_id,'AURA Workflow receipt lost truthful provenance')
    else:
        req(state.get('playbook_id') is None and state.get('workflow_id') is None,f'{method_type} receipt fabricated AURA provenance')

    evidence=write(rd/'artifacts'/'evidence.txt',f'{method_type} evidence\n');result=write(rd/'artifacts'/'result.md',f'# Result\n\nUseful bounded {method_type} work.\n')
    completed=run(S/'complete_run.py',BID,rid,'--evidence',str(evidence.relative_to(ROOT)),'--result',str(result.relative_to(ROOT)),'--summary',f'Completed useful {method_type} work.','--unresolved','Revisit only if material new evidence changes the result.')
    payload=json.loads(completed.stdout);req(payload.get('status')=='completed',f'{method_type} receipt did not complete: {payload}')
    state=load(rd/'run.json');receipt=state.get('continuity') or {}
    req(state.get('status')=='completed' and receipt.get('state')=='completed',f'{method_type} receipt state mismatch')
    req(receipt.get('purpose')=='organizational_work_receipt','receipt lost continuity purpose');req(receipt.get('method_type')==method_type,'receipt lost method type');req(receipt.get('method_ref')==state.get('method_ref'),'receipt lost method reference')
    req(str(evidence.relative_to(ROOT)) in receipt.get('evidence_refs',[]),'receipt omitted evidence');req(str(result.relative_to(ROOT)) in receipt.get('result_refs',[]),'receipt omitted result');req(not (rd/'contract-execution.json').exists(),'completion recreated execution ledger')
    return rid


def main():
    for path in (BASE,RUNS):
        if path.exists():shutil.rmtree(path)
    try:
        run(S/'init_business.py',BID,'--name','Run Provenance Regression')
        create_and_complete('external_skill','Bounded external Skill fixture','competitor-research-skill')
        create_and_complete('model_created','Bounded model-created fixture','model-created:conversion-diagnostic')
        create_and_complete('ad_hoc','Bounded ad-hoc fixture')
        create_and_complete('aura_workflow','Inspect bounded technical search evidence',workflow_id='seo.diagnosis.technical-opportunity')
        create_and_complete('aura_playbook','Research competitors end to end',playbook_id='competitor-research')

        validated=run(S/'validate_business.py',BID,check=False);req(validated.returncode==0,f'combined receipt validation failed: {validated.stdout+validated.stderr}')
        retired=['scripts/finalize_run.py','scripts/finalize_work_receipt.py','scripts/finalize_sop_run.py','scripts/complete_sop_run.py','scripts/record_contract_completion.py','scripts/run_lifecycle.py','scripts/reconcile_runs.py','scripts/run_provenance.py','scripts/persist_run_results.py']
        for rel in retired:req(not (ROOT/rel).exists(),f'retired Run execution/coupling helper reappeared: {rel}')
        schema=json.loads((ROOT/'core/schemas/runtime/run.schema.json').read_text());props=schema.get('properties',{})
        req('completion_policy_ref' not in props and 'contract_id' not in props,'Run schema recreated completion/flattened-contract authority')
        req({'playbook_id','workflow_id'}<=set(props),'Run schema lost truthful Playbook/Workflow provenance')
        retired_relationship_fields={'correlation_id','causation_id','root_run_id','parent_run_id','run_role','supersedes_run_id','superseded_by_run_id','lifecycle_reason'};req(not (retired_relationship_fields & set(props)),'Run schema recreated relationship lifecycle')

        negative=('do not ','does not ','never ','without ','no ','not required','rather than ','instead of ')
        for path in ROOT.rglob('CONTEXT.md'):
            if '/workflows/' not in path.as_posix():continue
            for line in path.read_text(encoding='utf-8').splitlines():
                low=line.lower()
                if ('manual action packet' in low or 'manual action package' in low) and not any(marker in low for marker in negative):req(False,f'{path.relative_to(ROOT)} recreated retired manual-action fallback: {line.strip()}')

        print('Run receipt regressions passed: Playbooks, Workflows, external Skills, model-created, and ad-hoc work share one optional receipt primitive')
    finally:
        for path in (BASE,RUNS):
            if path.exists():shutil.rmtree(path)

if __name__=='__main__':main()
