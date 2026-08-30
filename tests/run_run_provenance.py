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

        # A representative composite Run should need only AI-authored semantic content,
        # the supported persistence interface, and one finalizer call. The input deliberately
        # contains no IDs/timestamps/paths/Run provenance and uses local aliases instead.
        frid=run(S/'create_run.py',BID,'customer-optimization.intervention.adoption','High-level composite finalization fixture').stdout.strip()
        root_contract='customer-optimization.intervention.adoption';sub_contract='customer-optimization.adoption.path-design'
        result_input=write(f'runtime/runs/{BID}/{frid}/work/results.json',{'objects':[
            {'key':'opportunity','object_type':'Opportunity','content':{
                'title':'Activation path opportunity','statement':'A bounded activation path improvement should be reviewed.','status':'candidate','objective_refs':[],'confidence':0.6}},
            {'key':'action','object_type':'ActionPacket','content':{
                'opportunity_ref':'@opportunity','status':'proposed_not_executed','actions':[
                    {'action_id':'review-finalizer','description':'Review the composite finalizer result.','executor_type':'HUMAN','expected_outputs':['review decision'],'status':'proposed'}]}},
            {'key':'request','object_type':'WorkRequest','content':{
                'executing_system':'content-synthesis','origin_opportunity_ref':'@opportunity','origin_action_ref':'@action',
                'purpose':'Prepare the bounded activation guidance for review.','required_output':'A reviewable activation guidance draft.','status':'open'}}
        ]})
        persisted=run(S/'persist_run_results.py',BID,frid,'--input',result_input,'--workspace',ROOT,check=False)
        req(persisted.returncode==0,f'supported Run-result persistence failed: {persisted.stdout+persisted.stderr}')
        persisted_result=json.loads(persisted.stdout);rows={x['key']:x for x in persisted_result.get('objects',[])}
        req(persisted_result.get('status')=='persisted' and persisted_result.get('pre_finalization_validation',{}).get('status')=='clean',f'active-Run persistence should distinguish deferred completion conditions from genuine validation errors: {persisted_result}')
        req(set(rows)=={'opportunity','action','request'},f'persistence did not return every authored result: {persisted_result}')
        finalized_action=ROOT/rows['action']['path'];finalized_opp=ROOT/rows['opportunity']['path'];finalized_request=ROOT/rows['request']['path']
        action_data=json.loads(finalized_action.read_text());opp_data=json.loads(finalized_opp.read_text());request_data=json.loads(finalized_request.read_text())
        req(action_data['opportunity_ref']==opp_data['id'] and request_data['origin_opportunity_ref']==opp_data['id'] and request_data['origin_action_ref']==action_data['id'],'persistence did not resolve local semantic references to canonical IDs')
        for data in (action_data,opp_data,request_data):
            bos=data.get('extensions',{}).get('businessos',{})
            req(data.get('created_at') and data.get('updated_at') and bos.get('run_id')==frid and bos.get('run_contract_id')==root_contract,'persistence did not supply canonical mechanical wrapping/provenance')

        # Reproduce the blind confirmation seam: explicit root evidence omits the already
        # Run-linked Opportunity. The finalizer must include it comprehensively before mutation.
        finalized=run(S/'finalize_run.py',BID,frid,'--skip-human-knowledge','--evidence',rows['action']['path'],'--evidence',rows['request']['path'],check=False)
        req(finalized.returncode==0,f'high-level composite finalization failed: {finalized.stdout+finalized.stderr}')
        final_result=json.loads(finalized.stdout)
        operations=[x.get('operation') for x in final_result.get('automatic_repairs',[])]
        req(final_result.get('status')=='completed' and operations==['include_required_run_linked_evidence','record_subcontract_completion','complete_root_run'],f'finalizer did not sequence the ordinary composite completion path: {final_result}')
        included=final_result['automatic_repairs'][0].get('evidence_refs',[])
        req(rows['opportunity']['path'] in included,f'finalizer did not safely include omitted exact Run-linked completion evidence: {final_result}')
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

        # Genuine canonical problems must be returned before finalization mutation; active-Run
        # completion status/evidence conditions themselves must not obscure the real issue.
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
        req(rolled_result.get('category')=='pre_finalization_validation_failed' and rolled_result.get('mutation')=='none',f'genuine object errors were not returned concisely before mutation: {rolled_result}')
        req(any('required' in e or 'owner_system' in e for e in rolled_result.get('errors',[])),f'pre-finalization result obscured the genuine canonical error: {rolled_result}')
        req(rmanifest.read_bytes()==before_manifest and rrun.read_bytes()==before_run and rollback_action.read_bytes()==before_action,'pre-finalization failure mutated Run or evidence state')
        req(json.loads(rrun.read_text()).get('status')=='active','failed finalization must leave Run active')
        req(json.loads(rmanifest.read_text())['contracts'][sub_contract].get('status')=='pending','failed finalization must not retain partial subcontract completion')
        invalid.unlink();rollback_action.unlink()

        # The finalizer's outer transaction still restores subcontract/provenance changes
        # if an unexpected failure occurs after its clean pre-mutation validation.
        orid=run(S/'create_run.py',BID,'customer-optimization.intervention.adoption','Outer finalizer rollback preservation fixture').stdout.strip()
        outer_action=write(f'instances/{BID}/operations/action-packets/act_{BID}_outer_transaction.json',{
            'id':f'act_{BID}_outer_transaction','object_type':'ActionPacket','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'opportunity_ref':opp_data['id'],'status':'proposed_not_executed','actions':[
                {'action_id':'outer-transaction-check','description':'Verify finalizer rollback remains intact.','executor_type':'HUMAN','expected_outputs':['rollback proof'],'status':'proposed'}],
            'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{orid}','run_id':orid,'run_contract_id':root_contract,'contract_chain':[root_contract,sub_contract]}}
        })
        omanifest=RUNS/orid/'contract-execution.json';orun=RUNS/orid/'run.json'
        outer_before=(omanifest.read_bytes(),orun.read_bytes(),outer_action.read_bytes())
        import finalize_run as finalizer_module
        original_complete=finalizer_module.complete_run
        try:
            def forced_failure(*_args,**_kwargs):raise ValueError('forced post-subcontract failure')
            finalizer_module.complete_run=forced_failure
            outer=finalizer_module.finalize_run(BID,orid,refresh_human_knowledge=False)
        finally:finalizer_module.complete_run=original_complete
        req(outer.get('category')=='finalization_validation_failed' and outer.get('rollback')=='restored_pre_finalization_state',f'outer finalizer rollback was not reported: {outer}')
        req((omanifest.read_bytes(),orun.read_bytes(),outer_action.read_bytes())==outer_before,'outer finalizer transaction did not restore exact pre-finalization bytes')
        outer_action.unlink()

        # The low-level completion transaction remains rollback-safe if an unexpected full
        # active-business failure occurs after provenance/state staging.
        txrid=run(S/'create_run.py',BID,'customer-optimization.diagnosis.bottleneck-prioritization','Low-level rollback preservation fixture').stdout.strip()
        txaction=write(f'instances/{BID}/operations/action-packets/act_{BID}_transaction.json',{
            'id':f'act_{BID}_transaction','object_type':'ActionPacket','schema_version':'1.0.0','business_id':BID,'owner_system':'customer-optimization',
            'opportunity_ref':opp_data['id'],'status':'proposed_not_executed','actions':[
                {'action_id':'transaction-check','description':'Verify completion rollback remains intact.','executor_type':'HUMAN','expected_outputs':['rollback proof'],'status':'proposed'}],
            'extensions':{}
        })
        txinvalid=write(f'instances/{BID}/decisions/opportunities/opp_{BID}_transaction_invalid.json',{
            'id':f'opp_{BID}_transaction_invalid','object_type':'Opportunity','schema_version':'1.0.0','business_id':BID
        })
        txmanifest=RUNS/txrid/'contract-execution.json';txrun=RUNS/txrid/'run.json'
        tx_before=(txmanifest.read_bytes(),txrun.read_bytes(),txaction.read_bytes())
        tx=run(S/'complete_run.py',BID,txrid,'--evidence',str(txaction.relative_to(ROOT)),check=False)
        req(tx.returncode==1 and 'active business validation is not clean' in tx.stderr,f'low-level completion did not reach its transactional validation gate: {tx.stdout+tx.stderr}')
        req((txmanifest.read_bytes(),txrun.read_bytes(),txaction.read_bytes())==tx_before,'low-level completion validation failure did not restore exact pre-completion bytes')
        txinvalid.unlink();txaction.unlink()
        print('run provenance regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        if RUNS.exists(): shutil.rmtree(RUNS)
        d=ROOT/'runtime'/BID
        if d.exists(): shutil.rmtree(d)

if __name__=='__main__': main()
