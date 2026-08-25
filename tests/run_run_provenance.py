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
            'id':f'opp_{BID}_fixture','object_type':'Opportunity','business_id':BID,'owner_system':'customer-optimization','extensions':{}
        })
        act=write(f'instances/{BID}/operations/action-packets/act_{BID}_fixture.json',{
            'id':f'act_{BID}_fixture','object_type':'ActionPacket','business_id':BID,'owner_system':'customer-optimization','status':'proposed_not_executed','extensions':{}
        })
        att=write(f'instances/{BID}/operations/attention/att_{BID}_fixture.json',{
            'id':f'att_{BID}_fixture','object_type':'AttentionItem','business_id':BID,'owner_system':'customer-optimization','status':'open','extensions':{}
        })
        paths=[opp,act,att]

        # Exact RC8 failure: execution-significant canonical state with no Run must fail.
        errs=run_completion_errors(BID,objects(paths))
        req(all(any(t in e and 'requires extensions.businessos.run_ref' in e for e in errs) for t in ['Opportunity','ActionPacket','AttentionItem']),f'no-Run state must fail for all bounded outputs: {errs}')

        # A completed but unrelated Run is not enough merely because an object points at it.
        unrelated=run(S/'create_run.py',BID,'seo.diagnosis.detectors.indexing','Unrelated SEO fixture Run').stdout.strip()
        note=ROOT/'runtime'/BID/'unrelated.txt'; note.parent.mkdir(parents=True,exist_ok=True); note.write_text('unrelated evidence\n')
        run(S/'complete_run.py',BID,unrelated,'--evidence',str(note.relative_to(ROOT)))
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
        run(S/'complete_run.py',BID,rid,
            '--evidence',str(opp.relative_to(ROOT)),
            '--evidence',str(act.relative_to(ROOT)),
            '--evidence',str(att.relative_to(ROOT)))
        bound=objects(paths); errs=run_completion_errors(BID,bound)
        req(not errs,f'completed bounded Run with canonical completion evidence should pass even when intervention remains proposed/blocked: {errs}')
        for obj,_ in bound:
            bos=obj['extensions']['businessos']
            req(bos['run_id']==rid and bos['run_contract_id']=='customer-optimization.diagnosis.bottleneck-prioritization','completion helper must stamp canonical Run provenance')

        # Historical/imported state remains valid without retroactive Run fabrication.
        hist={'id':'opp_historical','object_type':'Opportunity','business_id':BID,'owner_system':'customer-optimization','extensions':{'businessos':{'origin':'preexisting'}}}
        req(not run_completion_errors(BID,[(hist,f'instances/{BID}/history/opportunity.json')]),'explicit preexisting state must remain migration-compatible')
        print('run provenance regressions passed')
    finally:
        if BASE.exists(): shutil.rmtree(BASE)
        if RUNS.exists(): shutil.rmtree(RUNS)
        d=ROOT/'runtime'/BID
        if d.exists(): shutil.rmtree(d)

if __name__=='__main__': main()
