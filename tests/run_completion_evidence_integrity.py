#!/usr/bin/env python3
"""Regression coverage for structural/quality evidence checks independent of Run orchestration."""
from pathlib import Path
import json, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import contract_index, completion_spec, validate_evidence

BID='completion-evidence-integrity';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID

def req(c,m):
    if not c:raise AssertionError(m)
def run(*args):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True)
def write(path,text):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8');return path


def main():
    for p in [BASE,RUNS]:
        if p.exists():shutil.rmtree(p)
    try:
        req(run(S/'init_business.py',BID,'--name','Completion Evidence Integrity').returncode==0,'init failed')
        contracts=contract_index()
        req(completion_spec(contracts['content.production.article'])['profile']=='production','article should use production profile')
        req(completion_spec(contracts['content.qa.pre-publish'])['profile']=='qa','pre-publish should use QA profile')
        req(completion_spec(contracts['content.qa.pre-publish'])['strict_qa_target'] is True,'pre-publish should require exact target Asset/version')
        req(completion_spec(contracts['content.measurement.content-performance'])['profile']=='measurement','content performance should use measurement profile')
        req(completion_spec(contracts['content.research.source-support'])['profile']=='research','source support should use research profile')
        req(completion_spec(contracts['seo.diagnosis.detectors.indexing'])['profile']=='detector','detector profile inference failed')
        req(completion_spec(contracts['content.production.short-video'])['allow_specification_fallback'] is True,'short video should support a truthful production-spec fallback')
        req(completion_spec(contracts['marketing.email.qa'])['strict_qa_target'] is True,'email QA should identify exact tested Asset/version')
        req('required_text_components' not in completion_spec(contracts['marketing.email.message-draft']),'quality must not be magic-phrase matching')
        planning_spec=completion_spec(contracts['marketing.strategy.messaging'])
        req(planning_spec['require_root_write_evidence'] is False,'planning must not manufacture a canonical object just because writes lists possible outputs')
        req(completion_spec(contracts['marketing.email.subject-preview'])['require_subcontract_write_evidence'] is False,'integrated leaf work should not require synthetic writes')

        rid=run(S/'create_run.py',BID,'Produce a real evidence-backed article','--contract-id','content.production.article').stdout.strip()
        req(rid.startswith('run_'),'optional article receipt creation failed')
        req(not (RUNS/rid/'contract-execution.json').exists(),'quality checking recreated a Run execution ledger')

        wrk={'id':f'wrk_{BID}_source','object_type':'WorkRequest','business_id':BID,'extensions':{}}
        wp=BASE/'work'/'request.json';write(wp,json.dumps(wrk,indent=2)+'\n')
        wrong=BASE/'assets'/'article.png';write(wrong,'not actually an article document\n')
        aid=f'ast_{BID}_article';asset={
            'id':aid,'object_type':'Asset','business_id':BID,'owner_system':'content-synthesis','asset_type':'article','business_role':'customer_facing_article','version':'1','status':'draft','lineage':[wrk['id']],
            'location_reference':str(wrong.relative_to(ROOT)),'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{rid}','run_id':rid,'run_contract_id':'content.production.article','run_method_type':'aura_playbook','run_method_ref':'content.production.article','customer_facing':True}}
        }
        ap=BASE/'assets'/f'{aid}.json';write(ap,json.dumps(asset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.article'],[str(wrong.relative_to(ROOT))],BID,rid,phase='root')
        req(any('expected text/document medium' in e for e in errs),f'wrong-medium placeholder must fail: {errs}')
        article_body="""# Field-service implementation transparency

A rollout decision should begin with the current process, the intended improvement, the people affected, and the evidence that would show whether the change helped. Teams should separate observed results from causal claims, state important uncertainty, and define the next reversible step before expanding the change.

That gives operators a practical review they can use without pretending that a longer document is automatically a better one.
"""
        article=BASE/'assets'/'article.md';write(article,article_body);asset['location_reference']=str(article.relative_to(ROOT));write(ap,json.dumps(asset,indent=2)+'\n')
        req(not validate_evidence(contracts['content.production.article'],[str(article.relative_to(ROOT))],BID,rid,phase='root'),'concise lineage-bound article should satisfy structural integrity')
        write(article,'# Deliverable: content.production.article\n\nThis is qualification-facing completion prose, not an article.\n')
        errs=validate_evidence(contracts['content.production.article'],[str(article.relative_to(ROOT))],BID,rid,phase='root')
        req(any('internal contract/qualification identifiers' in e for e in errs),f'internal completion metadata must not pass as customer-facing content: {errs}')
        write(article,article_body)

        # A non-rendered video fallback must be a real production specification, not arbitrary prose.
        vidrid='run_video_fixture';vfile=BASE/'assets'/'video-packet.md';write(vfile,'generic operations guide with no production detail\n')
        vasset={**asset,'id':f'ast_{BID}_video','asset_type':'short-video','location_reference':str(vfile.relative_to(ROOT)),'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{vidrid}','run_id':vidrid,'run_contract_id':'content.production.short-video','run_method_type':'aura_playbook','run_method_ref':'content.production.short-video','customer_facing':True}}}
        vap=BASE/'assets'/f"{vasset['id']}.json";write(vap,json.dumps(vasset,indent=2)+'\n')
        req(validate_evidence(contracts['content.production.short-video'],[str(vfile.relative_to(ROOT))],BID,vidrid,phase='root'),'generic prose must not count as a short-video production specification')
        write(vfile,"""# Short video production specification
Visual plan and duration: 45 seconds. Audio direction supports comprehension.
Scene 1 establishes the dispatch problem; scene 2 shows the workflow; scene 3 delivers proof and CTA.
Shot transitions, on-screen text, captions, final CTA, and rendering notes are specified for production.
""")
        req(not validate_evidence(contracts['content.production.short-video'],[str(vfile.relative_to(ROOT))],BID,vidrid,phase='root'),'concise executable video specification should satisfy graceful-degradation structure')
        fake_mp4=BASE/'assets'/'fake.mp4';write(fake_mp4,'ftyp placeholder mdat without a playable movie index\n'*40);vasset['location_reference']=str(fake_mp4.relative_to(ROOT));write(vap,json.dumps(vasset,indent=2)+'\n')
        errs=validate_evidence(contracts['content.production.short-video'],[str(fake_mp4.relative_to(ROOT))],BID,vidrid,phase='root')
        req(any('structurally decodable' in e for e in errs),f'extension-only fake media must fail: {errs}')

        # QA quality is checked directly; no contract-completion ledger is required.
        bad=RUNS/rid/'artifacts'/'bad-prepublish.json';write(bad,json.dumps({'contract_id':'content.qa.pre-publish','status':'pass'})+'\n')
        errs=validate_evidence(contracts['content.qa.pre-publish'],[str(bad.relative_to(ROOT))],BID,rid,phase='subcontract')
        req(errs,f'bare QA self-attestation must fail: {errs}')
        strings=RUNS/rid/'artifacts'/'string-prepublish.json';write(strings,json.dumps({'contract_id':'content.qa.pre-publish','status':'pass','tested_asset':aid,'tested_version':'1','checks_performed':['checked claims','checked links','checked accessibility'],'blockers':[]})+'\n')
        errs=validate_evidence(contracts['content.qa.pre-publish'],[str(strings.relative_to(ROOT))],BID,rid,phase='subcontract')
        req(any('per-check outcomes' in e for e in errs),f'generic string QA assertions must fail: {errs}')
        good=RUNS/rid/'artifacts'/'good-prepublish.json';write(good,json.dumps({
            'contract_id':'content.qa.pre-publish','status':'pass','tested_asset':aid,'tested_version':'1',
            'checks_performed':[
                {'check':'claims','status':'pass','method':'Compared each material statement with available evidence and claim context','finding':'The article presents a review method rather than a guaranteed business outcome.','target_excerpt':'A rollout decision should begin with the current process'},
                {'check':'links','status':'not_applicable','method':'Inspected the saved Markdown for destination links','finding':'The draft contains no destination links to test.','target_component':'article destination links','reason':'No links are present.'},
                {'check':'structure','status':'pass','method':'Inspected the whole article heading and paragraph structure','finding':'The article has one descriptive heading followed by two concise reader-facing paragraphs.','target_component':'whole article structure'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]},indent=2)+'\n')
        req(not validate_evidence(contracts['content.qa.pre-publish'],[str(good.relative_to(ROOT)),str(article.relative_to(ROOT))],BID,rid,phase='subcontract'),'structured artifact-specific QA should pass without a Run subcontract ledger')

        audience_context=RUNS/rid/'artifacts'/'audience-context.md';write(audience_context,"""# Audience/context decisions
Operations leaders are evaluating implementation effort and need a concise explanation of the rollout path, proof boundary, and next action. The content should reduce uncertainty without implying guaranteed outcomes.
""")
        req(not validate_evidence(contracts['content.strategy.audience-context'],[str(audience_context.relative_to(ROOT))],BID,rid,phase='subcontract'),'planning work should accept genuine integrated evidence without a synthetic canonical write')
        old_email=RUNS/rid/'artifacts'/'integrated-email.md';write(old_email,"""# Demo nurture sequence
Email 1 has a selected subject and preview, finished body copy, a clear next action, and branching/suppression logic tied to recipient state.
""")
        req(not validate_evidence(contracts['marketing.email.subject-preview'],[str(old_email.relative_to(ROOT))],BID,rid,phase='subcontract'),'integrated leaf evidence should not require standalone canonical objects')
        req(not validate_evidence(contracts['marketing.email.branching'],[str(old_email.relative_to(ROOT))],BID,rid,phase='subcontract'),'branching evidence should be usable inside an integrated artifact')

        note=RUNS/rid/'artifacts'/'note.md';write(note,'This file merely says the workflow ran.\n')
        errs=validate_evidence(contracts['content.measurement.content-performance'],[str(note.relative_to(ROOT))],BID,'run_measurement_fixture',phase='root')
        req(any('declared canonical write type' in e for e in errs),f'measurement must require an actual typed result: {errs}')
        result=RUNS/rid/'artifacts'/'evaluation.json';write(result,json.dumps({'id':'eval_fixture','object_type':'OutcomeEvaluation','business_id':BID})+'\n')
        req(not validate_evidence(contracts['content.measurement.content-performance'],[str(result.relative_to(ROOT))],BID,'run_measurement_fixture',phase='root'),'typed measurement result should satisfy structural evidence')

        crawl=RUNS/rid/'artifacts'/'crawl.txt';write(crawl,'index inspection evidence\n')
        nofind=RUNS/rid/'artifacts'/'no-finding.json';write(nofind,json.dumps({'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding','checks_performed':[{'check':'index state comparison','status':'pass'}],'evidence_refs':[str(crawl.relative_to(ROOT))]},indent=2)+'\n')
        req(not validate_evidence(contracts['seo.diagnosis.detectors.indexing'],[str(nofind.relative_to(ROOT))],BID,'run_detector_fixture',phase='root'),'auditable no-finding detector evidence should remain valid')

        print('completion evidence regressions passed: quality structure stays strong without Run execution orchestration')
    finally:
        for p in [BASE,RUNS]:
            if p.exists():shutil.rmtree(p)

if __name__=='__main__':main()
