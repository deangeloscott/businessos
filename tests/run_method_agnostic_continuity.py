#!/usr/bin/env python3
"""Regression: AURA remembers work without fabricating AURA contract execution."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts'
BID='method-agnostic-continuity';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID


def req(condition,message):
    if not condition:raise AssertionError(message)


def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)


def write(path,data):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n');return p


def main():
    if BASE.exists():shutil.rmtree(BASE)
    if RUNS.exists():shutil.rmtree(RUNS)
    try:
        run(S/'init_business.py',BID,'--name','Method Agnostic Continuity')

        # External Skill work gets a real Run/work receipt but no fabricated AURA contract execution.
        created=run(S/'create_run.py',BID,'Research competitor positioning with an external skill','--method-type','external_skill','--method-ref','example.com/skills/competitor-research')
        rid=created.stdout.strip();rd=RUNS/rid;rp=rd/'run.json'
        req(rid.startswith('run_'),'external Skill Run was not created')
        req(rp.exists(),'external Skill Run lacks run.json')
        req(not (rd/'contract-execution.json').exists(),'external Skill Run must not fabricate contract-execution.json')
        r=json.loads(rp.read_text())
        req(r['method_type']=='external_skill' and r['contract_id'] is None,'external Skill method provenance is incorrect')

        rr=f'runtime/runs/{BID}/{rid}'
        work=write(f'instances/{BID}/operations/work-requests/wrk_{BID}.json',{
            'id':f'wrk_{BID}','object_type':'WorkRequest','schema_version':'1.0.0','business_id':BID,
            'purpose':'Preserve the material follow-up from competitor research.','requested_output':'A focused follow-up analysis.','status':'open',
            'extensions':{'businessos':{'run_ref':rr,'run_id':rid,'run_method_type':'external_skill','run_method_ref':'example.com/skills/competitor-research'}}
        })
        decision=write(f'instances/{BID}/decisions/records/dec_{BID}.json',{
            'id':f'dec_{BID}','object_type':'DecisionRecord','schema_version':'1.0.0','business_id':BID,
            'decision':'Use the differentiated positioning direction identified by the research.','made_by':'user','made_at':'2026-08-31T18:00:00+00:00','status':'current',
            'extensions':{'businessos':{'run_ref':rr,'run_id':rid,'run_method_type':'external_skill','run_method_ref':'example.com/skills/competitor-research'}}
        })
        evidence=rd/'work'/'research-note.txt';evidence.write_text('Material research evidence fixture.\n')

        finalized=run(S/'finalize_work_receipt.py',BID,rid,'--skip-human-knowledge','--summary','External research completed and a positioning decision was retained.','--evidence',str(evidence.relative_to(ROOT)),'--result',str(work.relative_to(ROOT)),'--decision',f'dec_{BID}',check=False)
        req(finalized.returncode==0,f'external Skill receipt did not finalize: {finalized.stdout+finalized.stderr}')
        result=json.loads(finalized.stdout);req(result.get('status')=='completed',f'external Skill receipt status is not completed: {result}')
        r=json.loads(rp.read_text());continuity=r['continuity']
        req(r['status']=='completed' and continuity['method_type']=='external_skill','completed Run lost method provenance')
        req(str(work.relative_to(ROOT)) in continuity['result_refs'],'durable WorkRequest missing from result_refs')
        req(str(decision.relative_to(ROOT)) in continuity['decision_refs'],'DecisionRecord missing from decision_refs')
        req(str(evidence.relative_to(ROOT)) in continuity['evidence_refs'],'explicit evidence missing from receipt')
        req(not (rd/'contract-execution.json').exists(),'finalization fabricated AURA contract execution')
        validated=run(S/'validate_business.py',BID,check=False)
        req(validated.returncode==0,f'method-agnostic completed work must pass active-business validation: {validated.stdout+validated.stderr}')

        # A genuine AURA playbook Run remains separate and must use SOP conformance finalization.
        aura=run(S/'create_run.py',BID,'seo.diagnosis.detectors.indexing','AURA detector fixture')
        arid=aura.stdout.strip();ard=RUNS/arid
        req((ard/'contract-execution.json').exists(),'AURA playbook Run must retain its contract-execution manifest')
        wrong=run(S/'finalize_work_receipt.py',BID,arid,'--skip-human-knowledge',check=False)
        req(wrong.returncode==2,'general work-receipt finalizer must refuse to certify an AURA playbook Run')
        wrong_result=json.loads(wrong.stdout)
        req(wrong_result.get('category')=='wrong_finalizer','AURA playbook refusal reason is not explicit')

        print('method-agnostic Run continuity regressions passed')
    finally:
        if BASE.exists():shutil.rmtree(BASE)
        if RUNS.exists():shutil.rmtree(RUNS)


if __name__=='__main__':main()
