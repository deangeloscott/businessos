#!/usr/bin/env python3
"""Regression coverage for reusable structural evidence checks, independent of execution receipts."""
from pathlib import Path
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import contract_index,completion_spec,validate_evidence

BID='completion-evidence-integrity';BASE=ROOT/'instances'/BID;WORK=BASE/'verification'

def req(c,m):
    if not c:raise AssertionError(m)
def run(*args):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True)
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text((json.dumps(value,indent=2)+'\n') if not isinstance(value,str) else value,encoding='utf-8');return path
def rel(path):return path.relative_to(ROOT).as_posix()

def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        req(run(S/'init_business.py',BID,'--name','Completion Evidence Integrity').returncode==0,'init failed')
        contracts=contract_index()
        req(completion_spec(contracts['content.production.article'])['profile']=='production','article profile lost')
        req(completion_spec(contracts['content.qa.pre-publish'])['profile']=='qa','QA profile lost')
        req(completion_spec(contracts['content.qa.pre-publish'])['strict_qa_target'] is True,'QA must target exact Asset/version')
        req(completion_spec(contracts['content.measurement.content-performance'])['profile']=='measurement','measurement profile lost')
        req(completion_spec(contracts['content.research.source-support'])['profile']=='research','research profile lost')
        req(completion_spec(contracts['seo.diagnosis.detectors.indexing'])['profile']=='detector','detector profile lost')
        req(completion_spec(contracts['content.production.short-video'])['allow_specification_fallback'] is True,'short video should support truthful production specifications')
        req(completion_spec(contracts['marketing.strategy.messaging'])['require_root_write_evidence'] is False,'planning must not manufacture canonical output')
        req(completion_spec(contracts['marketing.email.subject-preview'])['require_subcontract_write_evidence'] is False,'leaf work must not require synthetic subcontract writes')

        # Text production: wrong medium and internal completion paperwork fail; concise real work passes.
        wrong=write(WORK/'article.png','not actually an article document\n')
        errs=validate_evidence(contracts['content.production.article'],[rel(wrong)],BID)
        req(any('expected text/document medium' in e for e in errs),f'wrong medium should fail: {errs}')
        article=write(WORK/'article.md','# Field-service implementation transparency\n\nA rollout decision should begin with the current process, intended improvement, affected people, and evidence that would show whether the change helped. Separate observed results from causal claims, state uncertainty, and define the next reversible step.\n')
        req(not validate_evidence(contracts['content.production.article'],[rel(article)],BID),'concise real article should pass structural verification')
        write(article,'# Deliverable: content.production.article\n\nThis is qualification-facing completion prose, not an article.\n')
        errs=validate_evidence(contracts['content.production.article'],[rel(article)],BID)
        req(any('internal contract/qualification identifiers' in e for e in errs),f'internal completion prose must fail: {errs}')

        # Rendered-media checks must reject extension-only fakes; a detailed textual spec is valid only where the method allows it.
        spec=write(WORK/'video-spec.md','generic operations guide with no production detail\n')
        req(validate_evidence(contracts['content.production.short-video'],[rel(spec)],BID),'generic prose must not count as video production specification')
        write(spec,'# Short video production specification\nVisual plan and duration: 45 seconds. Audio direction supports comprehension.\nScene 1 establishes the problem; scene 2 shows the workflow; scene 3 delivers proof and CTA.\nShot transitions, on-screen text, captions, final CTA, and rendering notes are specified.\n')
        req(not validate_evidence(contracts['content.production.short-video'],[rel(spec)],BID),'executable video specification should pass')
        fake=write(WORK/'fake.mp4','ftyp placeholder mdat without a playable movie index\n'*40)
        errs=validate_evidence(contracts['content.production.short-video'],[rel(fake)],BID)
        req(any('structurally decodable' in e for e in errs),f'fake media should fail: {errs}')

        # Planning accepts a genuine result directly; no synthetic canonical object is necessary.
        planning=write(WORK/'audience-context.md','# Audience/context decisions\nOperations leaders need a concise explanation of rollout path, proof boundary, and next action. The content should reduce uncertainty without implying guaranteed outcomes.\n')
        req(not validate_evidence(contracts['content.strategy.audience-context'],[rel(planning)],BID),'planning result should pass without bookkeeping writes')

        # Durable measurement requires a real typed result rather than arbitrary prose.
        note=write(WORK/'measurement-note.md','This file merely says the workflow ran.\n')
        errs=validate_evidence(contracts['content.measurement.content-performance'],[rel(note)],BID)
        req(any('declared canonical write type' in e for e in errs),f'measurement should require typed durable result: {errs}')
        result=write(WORK/'evaluation.json',{'id':'eval_fixture','object_type':'OutcomeEvaluation','business_id':BID})
        req(not validate_evidence(contracts['content.measurement.content-performance'],[rel(result)],BID),'typed measurement result should pass structural verification')

        # A detector may truthfully find nothing when the no-finding record is auditable.
        crawl=write(WORK/'crawl.txt','index inspection evidence\n')
        nofind=write(WORK/'no-finding.json',{'contract_id':'seo.diagnosis.detectors.indexing','status':'completed','result':'no_finding','checks_performed':[{'check':'index state comparison','status':'pass'}],'evidence_refs':[rel(crawl)]})
        req(not validate_evidence(contracts['seo.diagnosis.detectors.indexing'],[rel(nofind)],BID),'auditable no-finding should remain valid')

        req(not (ROOT/'runtime'/'runs'/BID).exists(),'structural evidence verification created Run state')
        print('structural evidence regressions passed without Run/execution orchestration')
    finally:
        if BASE.exists():shutil.rmtree(BASE)

if __name__=='__main__':main()
