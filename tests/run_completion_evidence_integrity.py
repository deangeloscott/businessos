#!/usr/bin/env python3
"""Regression coverage for contract-aware Run completion evidence."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import contract_index, completion_spec, validate_evidence

BID='completion-evidence-integrity';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID

def req(c,m):
    if not c:raise AssertionError(m)
def run(*args):
    return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True)
def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');return path

def main():
    for p in [BASE,RUNS]:
        if p.exists():shutil.rmtree(p)
    try:
        req(run(S/'init_business.py',BID,'--name','Completion Evidence Integrity').returncode==0,'init failed')
        contracts=contract_index()
        req(completion_spec(contracts['content.production.article'])['profile']=='production','article should use production profile')
        req(completion_spec(contracts['content.qa.pre-publish'])['profile']=='qa','pre-publish should use QA profile')
        req(completion_spec(contracts['content.measurement.content-performance'])['profile']=='measurement','content performance should use measurement profile')
        req(completion_spec(contracts['content.research.source-support'])['profile']=='research','source support should use research profile')
        req(completion_spec(contracts['seo.diagnosis.detectors.indexing'])['profile']=='detector','detector profile inference failed')

        rid=run(S/'create_run.py',BID,'content.production.article','Produce a real evidence-backed article').stdout.strip()
        req(rid.startswith('run_'),f'create_run failed: {rid}')
        manifest=json.loads((RUNS/rid/'contract-execution.json').read_text())
        req(manifest.get('root_completion_evidence_spec',{}).get('profile')=='production','Run must snapshot root completion evidence profile')
        req((manifest.get('contracts',{}).get('content.qa.pre-publish') or {}).get('completion_evidence_spec',{}).get('profile')=='qa','Run must snapshot subcontract completion evidence profile')

        # Build one canonical input and a Run-bound production Asset.
        wrk={
            'id':f'wrk_{BID}_source','object_type':'WorkRequest','business_id':BID,
            'extensions':{}
        }
        wp=BASE/'work'/'request.json';write(wp,json.dumps(wrk,indent=2)+'\n')
        short=BASE/'assets'/'article.md';write(short,'# Generic placeholder\n\n'+('generic filler words ' * 35))
        aid=f'ast_{BID}_article'
        asset={
            'id':aid,'object_type':'Asset','business_id':BID,'owner_system':'content-synthesis',
            'asset_type':'article','business_role':'customer_facing_article','version':'1','status':'draft',
            'lineage':[wrk['id']],'location_reference':str(short.relative_to(ROOT)),
            'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{rid}','run_id':rid,'run_contract_id':'content.production.article','customer_facing':True,'contract_chain':['content.production.article']}}
        }
        ap=BASE/'assets'/f'{aid}.json';write(ap,json.dumps(asset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.article'],[str(short.relative_to(ROOT))],BID,rid,phase='root')
        req(any('too small' in e for e in errs),f'short generic production placeholder must fail substance check: {errs}')
        write(short,'# Field-service implementation transparency\n\n'+('AtlasOps field service leaders need implementation visibility, workflow continuity, rollout evidence, and practical dispatch guidance. ' * 28))
        errs=validate_evidence(contracts['content.production.article'],[str(short.relative_to(ROOT))],BID,rid,phase='root')
        req(not errs,f'substantive lineage-bound article evidence should satisfy deterministic production minimums: {errs}')

        # Bare QA self-attestation must be rejected by record_contract_completion.py.
        bad=RUNS/rid/'artifacts'/'bad-prepublish.json';write(bad,json.dumps({'contract_id':'content.qa.pre-publish','status':'pass'})+'\n')
        r=run(S/'record_contract_completion.py',BID,rid,'content.qa.pre-publish','--evidence',str(bad.relative_to(ROOT)))
        req(r.returncode!=0 and 'structured JSON QA pass record' in (r.stderr+r.stdout),f'bare QA self-attestation must fail: {r.stderr+r.stdout}')
        good=RUNS/rid/'artifacts'/'good-prepublish.json';write(good,json.dumps({
            'contract_id':'content.qa.pre-publish','status':'pass','tested_asset':aid,'tested_version':'1',
            'checks_performed':[{'check':'claims','status':'pass'},{'check':'links','status':'pass'},{'check':'accessibility','status':'pass'}],
            'blockers':[]
        },indent=2)+'\n')
        r=run(S/'record_contract_completion.py',BID,rid,'content.qa.pre-publish','--evidence',str(good.relative_to(ROOT)))
        req(r.returncode==0,f'structured QA record should be recordable: {r.stderr+r.stdout}')

        # Standalone measurement/research Runs cannot complete on unrelated prose alone.
        note=RUNS/rid/'artifacts'/'note.md';write(note,'This file merely says the workflow ran.\n')
        mrun='run_measurement_fixture'
        errs=validate_evidence(contracts['content.measurement.content-performance'],[str(note.relative_to(ROOT))],BID,mrun,phase='root')
        req(any('declared canonical write type' in e for e in errs),f'measurement must require a declared canonical result: {errs}')
        result=RUNS/rid/'artifacts'/'evaluation.json';write(result,json.dumps({'id':'eval_fixture','object_type':'OutcomeEvaluation','business_id':BID})+'\n')
        req(not validate_evidence(contracts['content.measurement.content-performance'],[str(result.relative_to(ROOT))],BID,mrun,phase='root'),'typed measurement result should satisfy structural completion evidence')

        # Detectors may validly find nothing, but only with an auditable no-finding record.
        crawl=RUNS/rid/'artifacts'/'crawl.txt';write(crawl,'index inspection evidence\n')
        nofind=RUNS/rid/'artifacts'/'no-finding.json';write(nofind,json.dumps({
            'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding',
            'checks_performed':[{'check':'index state comparison','status':'pass'}],
            'evidence_refs':[str(crawl.relative_to(ROOT))]
        },indent=2)+'\n')
        req(not validate_evidence(contracts['seo.diagnosis.detectors.indexing'],[str(nofind.relative_to(ROOT))],BID,'run_detector_fixture',phase='root'),'structured detector no-finding evidence should be valid')

        print('contract-aware completion evidence regressions passed')
    finally:
        for p in [BASE,RUNS]:
            if p.exists():shutil.rmtree(p)

if __name__=='__main__':main()
