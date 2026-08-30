#!/usr/bin/env python3
"""RC9 regressions for bounded Run provenance beyond Content/Marketing production."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'scripts'; sys.path.insert(0,str(S))
from validate_run_completion import run_completion_errors

BID='run-provenance-regression'; BASE=ROOT/'instances'/BID; RUNS=ROOT/'runtime'/'runs'/BID

def req(c,m):
    if not c: raise AssertionError(m)
def run(*args,check=True):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True,check=check)
def write(rel,obj):
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2)+'\n'); return p

def objects(paths):
    return [(json.loads(p.read_text()),str(p.relative_to(ROOT))) for p in paths]

def main():
    if BASE.exists(): shutil.rmtree(BASE)
    if RUNS.exists(): shutil.rmtree(RUNS)
    try:
        run(S/'init_business.py',BID,'--name','Run Provenance Regression')
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
            'reason':'The bounded regression fixture requires review.','first_seen':'2026-08-27T00:00:00+00:00','last_seen':'2026-08-27T00:00:00+00:00',
            'occurrence_count':1,'retention_class':'operational','extensions':{}
        })
        paths=[opp,act,att]

        # Exact RC8 failure: execution-significant canonical state with no Run must fail.
        errs=run_completion_errors(BID,objects(paths))
        req(all(any(t in e and 'requires extensions.businessos.run_ref' in e for e in errs) for t in ['Opportunity','ActionPacket','AttentionItem']),f'no-Run state must fail for all bounded outputs: {errs}')
        # Keep the active business clean while completing the independent detector Run;
        # complete_run now transactionally enforces full active-business validation.
        fixtures=[json.loads(p.read_text()) for p in paths]
        for p in paths:p.unlink()

        # A completed but unrelated Run is not enough merely because an object points at it.
        unrelated=run(S/'create_run.py',BID,'seo.diagnosis.detectors.indexing','Unrelated SEO fixture Run').stdout.strip()
        note=ROOT/'runtime'/BID/'unrelated.txt'; note.parent.mkdir(parents=True,exist_ok=True); note.write_text('fixture index inspection evidence\n')
        nofind=ROOT/'runtime'/BID/'unrelated-no-finding.json'
        nofind.write_text(json.dumps({
            'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding',
            'checks_performed':['fixture index-state comparison'],'evidence_refs':[str(note.relative_to(ROOT))]
        },indent=2)+'\n')
        run(S/'complete_run.py',BID,unrelated,'--evidence',str(nofind.relative_to(ROOT)))
        for p,obj in zip(paths,fixtures):p.write_text(json.dumps(obj,indent=2)+'\n')
        o=json.loads(opp.read_text()); bos=o.setdefault('extensions',{}).setdefault('businessos',{}); bos.update({'run_ref':f'runtime/runs/{BID}/{unrelated}','run_id':unrelated,'run_contract_id':'seo.diagnosis.detectors.indexing'}); opp.write_text(json.dumps(o,indent=2)+'\n')
        errs=run_completion_errors(BID,objects([opp]))
        req(any('owner_system does not match' in e for e in errs),f'unrelated owner Run must fail: {errs}')
        req(any('not recorded as completion evidence' in e for e in errs),f'unrelated Run without evidence binding must fail: {errs}')

        # Reset and use the correct bounded Customer Optimization Run.
        for p in paths:
            o=json.loads(p.read_text()); o['extensions']={}; p.write_text(json.dumps(o,indent=2)+'\n')
        rid=run(S/'create_run.py',BID,'customer-optimization.diagnosis.bottleneck-prioritization','Diagnose activation bottleneck and persist blocked intervention').stdout.strip()
        errs=run_completion_errors(BID,objects(paths))
        req(any('requires extensions.businessos.run_ref' in e for e in errs),f'active Run without recorded evidence must not make outputs valid: {errs}')
        completed=run(S/'complete_run.py',BID,rid,
            '--evidence',str(opp.relative_to(ROOT)),
            '--evidence',str(act.relative_to(ROOT)),
            '--evidence',str(att.relative_to(ROOT)),check=False)
        req(completed.returncode==0,f'valid bounded Run should complete cleanly: {completed.stderr+completed.stdout}')
        bound=objects(paths); errs=run_completion_errors(BID,bound)
        req(not errs,f'completed bounded Run with canonical completion evidence should pass even when intervention remains proposed/blocked: {errs}')
        for obj,_ in bound:
            bos=obj['extensions']['businessos']
            req(bos['run_id']==rid and bos['run_contract_id']=='customer-optimization.diagnosis.bottleneck-prioritization','completion helper must stamp canonical Run provenance')

        # Historical/imported state remains valid without retroactive Run fabrication.
        hist={'id':'opp_historical','object_type':'Opportunity','business_id':BID,'owner_system':'customer-optimization','extensions':{'businessos':{'origin':'preexisting'}}}
        req(not run_completion_errors(BID,[(hist,f'instances/{BID}/history/opportunity.json')]),'explicit preexisting state must remain migration-compatible')

        # A representative composite Run should need only persisted governed output plus
        # one finalizer call; the caller must not manually sequence subcontract/root helpers.
        frid=run(S/'create_run.py',BID,'customer-optimization.intervention.adoption','High-level composite finalization fixture').stdout.strip()
        root_contract='customer-optimization.intervention.adoption';sub_contract='customer-optimization.adoption.path-design'
        finalized_action=write(f'instances/{BID}/operations/action-packets/act_{BID}_finalizer.json',{
            'id':f'act_{BID}_finalizer','object_type':'ActionPacket','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'opportunity_ref':f'opp_{BID}_fixture','status':'proposed_not_executed','actions':[
                {'action_id':'review-finalizer','description':'Review the composite finalizer fixture.','executor_type':'HUMAN','expected_outputs':['review decision'],'status':'proposed'}],
            'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{frid}','run_id':frid,'run_contract_id':root_contract,'contract_chain':[root_contract,sub_contract]}}
        })
        finalized=run(S/'finalize_run.py',BID,frid,'--skip-human-knowledge',check=False)
        req(finalized.returncode==0,f'high-level composite finalization failed: {finalized.stdout+finalized.stderr}')
        final_result=json.loads(finalized.stdout)
        operations=[x.get('operation') for x in final_result.get('automatic_repairs',[])]
        req(final_result.get('status')=='completed' and operations==['record_subcontract_completion','complete_root_run'],f'finalizer did not sequence the ordinary composite completion path: {final_result}')
        fm=json.loads((RUNS/frid/'contract-execution.json').read_text())
        req(fm['contracts'][sub_contract].get('status')=='completed' and fm.get('root_status')=='completed','finalizer did not persist composite completion bookkeeping')
        req(json.loads(finalized_action.read_text()).get('extensions',{}).get('businessos',{}).get('run_binding')=='root_completion_evidence','finalizer did not preserve final root provenance binding')

        # Two structurally valid records for one semantic detector-result role are ambiguous.
        # The high-level finalizer must ask for judgment and leave the Run wholly active.
        arid=run(S/'create_run.py',BID,'seo.diagnosis.detectors.indexing','Ambiguous detector finalization fixture').stdout.strip()
        inspected=RUNS/arid/'artifacts/inspection.txt';inspected.write_text('bounded indexing inspection fixture\n')
        for suffix in ['one','two']:
            write(f'runtime/runs/{BID}/{arid}/artifacts/no-finding-{suffix}.json',{
                'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding',
                'checks_performed':[{'check':f'index-state fixture {suffix}','status':'pass'}],
                'evidence_refs':[str(inspected.relative_to(ROOT))]
            })
        ambiguous=run(S/'finalize_run.py',BID,arid,check=False)
        req(ambiguous.returncode==2,f'ambiguous finalization should require judgment: {ambiguous.stdout+ambiguous.stderr}')
        ambiguity=json.loads(ambiguous.stdout)
        req(ambiguity.get('status')=='needs_judgment',f'ambiguous evidence was not classified as judgment-required: {ambiguity}')
        req(len(ambiguity.get('issue',{}).get('candidate_refs',[]))==2,f'ambiguous evidence candidates were not surfaced exactly: {ambiguity}')
        req(json.loads((RUNS/arid/'run.json').read_text()).get('status')=='active','ambiguous finalization must leave Run active')
        am=json.loads((RUNS/arid/'contract-execution.json').read_text())
        req(am.get('root_status')=='active' and not am.get('root_evidence_refs'),'ambiguous finalization must not partially complete root state')

        # An unexpected integrated-validation failure after subcontract recording must roll
        # back the manifest, Run, and provenance-bound evidence to their exact prior bytes.
        rrid=run(S/'create_run.py',BID,'customer-optimization.intervention.adoption','Transactional rollback fixture').stdout.strip()
        rollback_action=write(f'instances/{BID}/operations/action-packets/act_{BID}_rollback.json',{
            'id':f'act_{BID}_rollback','object_type':'ActionPacket','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'opportunity_ref':f'opp_{BID}_fixture','status':'proposed_not_executed','actions':[
                {'action_id':'review-rollback','description':'Review the rollback fixture.','executor_type':'HUMAN','expected_outputs':['review decision'],'status':'proposed'}],
            'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{rrid}','run_id':rrid,'run_contract_id':root_contract,'contract_chain':[root_contract,sub_contract]}}
        })
        invalid=write(f'instances/{BID}/decisions/opportunities/opp_{BID}_invalid_rollback.json',{
            'id':f'opp_{BID}_invalid_rollback','object_type':'Opportunity','schema_version':'1.0.0','business_id':BID
        })
        rmanifest=RUNS/rrid/'contract-execution.json';rrun=RUNS/rrid/'run.json'
        before_manifest=rmanifest.read_bytes();before_run=rrun.read_bytes();before_action=rollback_action.read_bytes()
        rolled=run(S/'finalize_run.py',BID,rrid,check=False)
        req(rolled.returncode==2,f'validation failure should keep finalization incomplete: {rolled.stdout+rolled.stderr}')
        rolled_result=json.loads(rolled.stdout)
        req(rolled_result.get('category')=='finalization_validation_failed' and rolled_result.get('rollback')=='restored_pre_finalization_state',f'rollback was not reported: {rolled_result}')
        req(rmanifest.read_bytes()==before_manifest and rrun.read_bytes()==before_run and rollback_action.read_bytes()==before_action,'failed finalization did not restore exact pre-finalization state')
        req(json.loads(rrun.read_text()).get('status')=='active','failed finalization must leave Run active')
        req(json.loads(rmanifest.read_text())['contracts'][sub_contract].get('status')=='pending','failed finalization must not retain partial subcontract completion')
        invalid.unlink()
        print('run provenance regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        if RUNS.exists(): shutil.rmtree(RUNS)
        d=ROOT/'runtime'/BID
        if d.exists(): shutil.rmtree(d)

if __name__=='__main__': main()
