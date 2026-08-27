#!/usr/bin/env python3
"""Regression coverage for contract-aware Run completion evidence."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import contract_index, completion_spec, subcontract_evidence_reuse_errors, validate_evidence

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
        req((ROOT/'core/policies/completion-evidence.md').exists(),'completion evidence policy missing')
        req(run(S/'init_business.py',BID,'--name','Completion Evidence Integrity').returncode==0,'init failed')
        contracts=contract_index()
        req(completion_spec(contracts['content.production.article'])['profile']=='production','article should use production profile')
        req(completion_spec(contracts['content.qa.pre-publish'])['profile']=='qa','pre-publish should use QA profile')
        req(completion_spec(contracts['content.qa.pre-publish'])['strict_qa_target'] is True,'pre-publish should require target Asset/version')
        req(completion_spec(contracts['content.measurement.content-performance'])['profile']=='measurement','content performance should use measurement profile')
        req(completion_spec(contracts['content.research.source-support'])['profile']=='research','source support should use research profile')
        req(completion_spec(contracts['seo.diagnosis.detectors.indexing'])['profile']=='detector','detector profile inference failed')
        req(completion_spec(contracts['content.production.short-video'])['allow_specification_fallback'] is True,'short video should support complete production packet fallback')
        req(completion_spec(contracts['marketing.email.qa'])['strict_qa_target'] is True,'production email QA should identify the exact tested Asset/version')

        rid=run(S/'create_run.py',BID,'content.production.article','Produce a real evidence-backed article').stdout.strip()
        req(rid.startswith('run_'),f'create_run failed: {rid}')
        manifest=json.loads((RUNS/rid/'contract-execution.json').read_text())
        runmeta=json.loads((RUNS/rid/'run.json').read_text())
        req(manifest.get('completion_policy_ref')=='core/policies/completion-evidence.md','Run manifest must expose completion evidence policy')
        req(runmeta.get('completion_policy_ref')=='core/policies/completion-evidence.md','Run metadata must expose completion evidence policy')
        req(manifest.get('root_completion_evidence_spec',{}).get('profile')=='production','Run must snapshot root completion evidence profile')
        req((manifest.get('contracts',{}).get('content.qa.pre-publish') or {}).get('completion_evidence_spec',{}).get('profile')=='qa','Run must snapshot subcontract completion evidence profile')

        # Build one canonical input and a Run-bound production Asset. A file can exist and
        # still be structurally wrong for the promised medium.
        wrk={'id':f'wrk_{BID}_source','object_type':'WorkRequest','business_id':BID,'extensions':{}}
        wp=BASE/'work'/'request.json';write(wp,json.dumps(wrk,indent=2)+'\n')
        wrong=BASE/'assets'/'article.png';write(wrong,'not actually an article document\n')
        aid=f'ast_{BID}_article'
        asset={
            'id':aid,'object_type':'Asset','business_id':BID,'owner_system':'content-synthesis',
            'asset_type':'article','business_role':'customer_facing_article','version':'1','status':'draft',
            'lineage':[wrk['id']],'location_reference':str(wrong.relative_to(ROOT)),
            'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{rid}','run_id':rid,'run_contract_id':'content.production.article','customer_facing':True,'contract_chain':['content.production.article']}}
        }
        ap=BASE/'assets'/f'{aid}.json';write(ap,json.dumps(asset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.article'],[str(wrong.relative_to(ROOT))],BID,rid,phase='root')
        req(any('expected text/document medium' in e for e in errs),f'wrong-medium production placeholder must fail: {errs}')
        article_body=('# Field-service implementation transparency\n\n'
            'Operations teams need a clear implementation plan before they can judge whether a workflow change is practical. '
            'This section explains the decision, the evidence to inspect, and the questions that keep a rollout grounded. '
            'A useful review names the current process, the intended improvement, the people affected, and the uncertainty that remains. '
            'It also separates an observed result from a causal claim and gives the reader a bounded next step.\n\n')*7
        article=BASE/'assets'/'article.md';write(article,article_body)
        asset['location_reference']=str(article.relative_to(ROOT));write(ap,json.dumps(asset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.article'],[str(article.relative_to(ROOT))],BID,rid,phase='root')
        req(not errs,f'lineage-bound article document should satisfy deterministic structural minimums: {errs}')
        write(article,'# Deliverable: content.production.article\n\nThis is qualification-facing completion prose, not an article.\n')
        errs=validate_evidence(contracts['content.production.article'],[str(article.relative_to(ROOT))],BID,rid,phase='root')
        req(any('internal contract/qualification identifiers' in e for e in errs),f'internal completion metadata must not pass as a customer-facing article: {errs}')
        write(article,article_body)

        # A non-rendered video may satisfy graceful degradation only when it is a real
        # production packet, not arbitrary prose.
        vidrid='run_video_fixture';vfile=BASE/'assets'/'video-packet.md';write(vfile,'generic operations guide with no production detail\n')
        vasset={**asset,'id':f'ast_{BID}_video','asset_type':'short-video','location_reference':str(vfile.relative_to(ROOT)),'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{vidrid}','run_id':vidrid,'run_contract_id':'content.production.short-video','customer_facing':True,'contract_chain':['content.production.short-video']}}}
        vap=BASE/'assets'/f"{vasset['id']}.json";write(vap,json.dumps(vasset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.short-video'],[str(vfile.relative_to(ROOT))],BID,vidrid,phase='root')
        req(errs,f'generic prose must not count as a short-video production packet: {errs}')
        write(vfile,('# Short video production packet\n\nVisual plan and duration: 45 seconds. Audio direction supports comprehension. '\
                    'Scene 1 establishes the dispatch problem; scene 2 shows the workflow; scene 3 delivers proof and CTA. '\
                    'Visual safe areas and captions are specified for the platform. Audio pacing, shot transitions, on-screen text, '\
                    'duration, final CTA, and rendering notes are included. ')*3)
        req(not validate_evidence(contracts['content.production.short-video'],[str(vfile.relative_to(ROOT))],BID,vidrid,phase='root'),'complete video production packet should satisfy graceful-degradation structure')

        fake_mp4=BASE/'assets'/'fake.mp4';write(fake_mp4,'ftyp placeholder mdat without a playable movie index\n'*40)
        vasset['location_reference']=str(fake_mp4.relative_to(ROOT));write(vap,json.dumps(vasset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.short-video'],[str(fake_mp4.relative_to(ROOT))],BID,vidrid,phase='root')
        req(any('structurally decodable' in e for e in errs),f'extension-only fake media must fail: {errs}')

        # Bare QA self-attestation must be rejected by record_contract_completion.py.
        bad=RUNS/rid/'artifacts'/'bad-prepublish.json';write(bad,json.dumps({'contract_id':'content.qa.pre-publish','status':'pass'})+'\n')
        r=run(S/'record_contract_completion.py',BID,rid,'content.qa.pre-publish','--evidence',str(bad.relative_to(ROOT)))
        req(r.returncode!=0 and 'structured JSON QA pass record' in (r.stderr+r.stdout),f'bare QA self-attestation must fail: {r.stderr+r.stdout}')
        strings=RUNS/rid/'artifacts'/'string-prepublish.json';write(strings,json.dumps({
            'contract_id':'content.qa.pre-publish','status':'pass','tested_asset':aid,'tested_version':'1',
            'checks_performed':['checked claims','checked links','checked accessibility'],'blockers':[]
        })+'\n')
        r=run(S/'record_contract_completion.py',BID,rid,'content.qa.pre-publish','--evidence',str(strings.relative_to(ROOT)))
        req(r.returncode!=0 and 'per-check outcomes' in (r.stderr+r.stdout),f'generic string QA assertions must fail: {r.stderr+r.stdout}')
        tautology=RUNS/rid/'artifacts'/'tautological-prepublish.json';write(tautology,json.dumps({
            'contract_id':'content.qa.pre-publish','status':'pass','tested_asset':aid,'tested_version':'1',
            'checks_performed':[{'check':'brand and claims','status':'pass','result':'All brand positioning and claim rules verified successfully.'}],
            'blockers':[]
        })+'\n')
        r=run(S/'record_contract_completion.py',BID,rid,'content.qa.pre-publish','--evidence',str(tautology.relative_to(ROOT)))
        req(r.returncode!=0 and 'per-check outcomes' in (r.stderr+r.stdout),f'tautological QA result must fail: {r.stderr+r.stdout}')
        good=RUNS/rid/'artifacts'/'good-prepublish.json';write(good,json.dumps({
            'contract_id':'content.qa.pre-publish','status':'pass','tested_asset':aid,'tested_version':'1',
            'checks_performed':[
                {'check':'claims','status':'pass','method':'Compared each extracted claim with the Asset claim manifest','finding':'The operational guidance remains framed as a review method rather than a guaranteed outcome.','target_excerpt':'A useful review names the current process'},
                {'check':'links','status':'not_applicable','method':'Inspected the saved Markdown for link syntax','finding':'The draft contains no destination links to request.','target_component':'article destination links','reason':'No links are present in this article draft.'},
                {'check':'accessibility','status':'pass','method':'Inspected heading sequence and paragraph structure in the saved Markdown','finding':'One descriptive H1 precedes short reader-facing paragraphs.','target_excerpt':'Field-service implementation transparency'}
            ],
            'issues_found':[],'corrections_made':[],'limitations':[],
            'blockers':[]
        },indent=2)+'\n')
        r=run(S/'record_contract_completion.py',BID,rid,'content.qa.pre-publish','--evidence',str(good.relative_to(ROOT)))
        req(r.returncode==0,f'structured QA record should be recordable: {r.stderr+r.stdout}')

        # A declared-write subcontract cannot complete on a generic status/summary stub.
        generic_sub=RUNS/rid/'artifacts'/'generic-audience-context.json';write(generic_sub,json.dumps({
            'contract_id':'content.strategy.audience-context','business_id':BID,'status':'completed',
            'subcontract_summary':'Completed required subcontract content.strategy.audience-context.',
            'target_audience':'Operations leaders','core_objective':'Increase qualified demand'
        },indent=2)+'\n')
        sub_errors=validate_evidence(contracts['content.strategy.audience-context'],[str(generic_sub.relative_to(ROOT))],BID,rid,phase='subcontract')
        req(any('declared canonical write type' in e for e in sub_errors),f'generic subcontract summary must not satisfy a declared-write contract: {sub_errors}')

        # Regression from the preserved CrewBeacon run: an email sequence cannot prove
        # subject/preview or branching completion when those components are absent.
        old_email=RUNS/rid/'artifacts'/'crewbeacon-style-email.md';write(old_email,"""# Demo nurture sequence

### Email 1: Confirmation
**Headline:** See how the product works.
**Body Copy:** A short confirmation message.
**CTA:** Book a demo

### Email 2: Reminder
**Headline:** Prioritize the work that needs attention.
**Body Copy:** A short reminder message.
**CTA:** Book a demo
""")
        subject_errors=validate_evidence(contracts['marketing.email.subject-preview'],[str(old_email.relative_to(ROOT))],BID,rid,phase='subcontract')
        branch_errors=validate_evidence(contracts['marketing.email.branching'],[str(old_email.relative_to(ROOT))],BID,rid,phase='subcontract')
        req(any('required component' in e and ('subject' in e or 'preview' in e) for e in subject_errors),f'absent subject/preview work must fail: {subject_errors}')
        req(any('required component' in e for e in branch_errors),f'absent branching/suppression work must fail: {branch_errors}')

        integrated=RUNS/rid/'artifacts'/'integrated-email.md';write(integrated,"""# Integrated email package
Email 1 sequence position and message job. Subject line: A useful update. Preview text: What to expect next.
Body copy: useful detail. CTA: Book a demo.
Branch condition: booked demo. Default path: no action. Suppression: exit condition stops the sequence.
""")
        shared_manifest={
            'required_subcontracts':['marketing.email.message-draft','marketing.email.subject-preview'],
            'contracts':{
                cid:{'status':'completed','evidence_refs':[str(integrated.relative_to(ROOT))]}
                for cid in ('marketing.email.message-draft','marketing.email.subject-preview')
            }
        }
        reuse=subcontract_evidence_reuse_errors(shared_manifest,contracts)
        req(any('reuse the same evidence reference set' in e for e in reuse),f'distinct subcontracts must not all point at one undifferentiated file: {reuse}')

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
