#!/usr/bin/env python3
"""Regression coverage for AURA's narrow structural-evidence boundary."""
from pathlib import Path
import json,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import completion_spec,validate_evidence

BID='completion-evidence-integrity';BASE=ROOT/'instances'/BID;WORK=BASE/'verification'


def req(condition,message):
    if not condition:raise AssertionError(message)

def run(*args):return subprocess.run([sys.executable,*map(str,args)],cwd=ROOT,capture_output=True,text=True)

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((json.dumps(value,indent=2)+'\n') if not isinstance(value,str) else value,encoding='utf-8')
    return path

def rel(path):return path.relative_to(ROOT).as_posix()


def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        req(run(S/'init_business.py',BID,'--name','Completion Evidence Integrity').returncode==0,'init failed')

        # Workflow ids/names are not semantic routing rules.
        looks_like_qa={'id':'content.qa.looks-like-qa'}
        spec=completion_spec(looks_like_qa)
        req(spec['profile']=='generic','Workflow id must not infer a QA profile')
        req(spec['selection_authority'] is False and spec['semantic_authority'] is False,'structural helper gained semantic authority')

        # Production checks verify medium/decodability, not writing quality or keyword templates.
        article_workflow={'id':'fixture.article','completion_evidence':{'profile':'production','medium':'article'}}
        wrong=write(WORK/'article.png','not a text/document artifact\n')
        errors=validate_evidence(article_workflow,[rel(wrong)],BID)
        req(any('wrong medium' in e for e in errors),f'wrong medium should fail: {errors}')
        article=write(WORK/'article.md','A concise real document exists here. Substantive quality belongs to model-based review, not this helper.\n')
        req(not validate_evidence(article_workflow,[rel(article)],BID),'existing text/document evidence should pass structural verification')

        # A fallback may be explicitly allowed, but this helper does not score whether it is creatively sufficient.
        video_workflow={'id':'fixture.video','completion_evidence':{'profile':'production','medium':'short-video','allow_specification_fallback':True}}
        video_spec=write(WORK/'video-spec.md','Source/production specification supplied because rendering is unavailable.\n')
        req(not validate_evidence(video_workflow,[rel(video_spec)],BID),'explicit textual fallback should pass structural verification')
        fake=write(WORK/'fake.mp4','ftyp placeholder without a movie index\n'*80)
        errors=validate_evidence(video_workflow,[rel(fake)],BID)
        req(any('structurally decodable' in e for e in errors),f'fake media should fail: {errors}')

        # Durable-object requirements exist only when explicitly requested.
        measurement={'id':'fixture.measurement','writes':[{'type':'OutcomeEvaluation'}],'completion_evidence':{'require_root_write_evidence':True}}
        note=write(WORK/'measurement-note.md','Measurement discussion without a durable measurement object.\n')
        errors=validate_evidence(measurement,[rel(note)],BID)
        req(any('durable write type' in e for e in errors),f'explicit durable-write check should fail: {errors}')
        evaluation=write(WORK/'evaluation.json',{'id':'eval_fixture','object_type':'OutcomeEvaluation','business_id':BID})
        req(not validate_evidence(measurement,[rel(evaluation)],BID),'declared durable object should pass structural verification')

        # QA structure can prove the target/version and references are real without judging semantic QA quality.
        asset=write(BASE/'assets'/'ast_fixture.json',{
            'id':'ast_fixture','object_type':'Asset','business_id':BID,'owner_system':'content-synthesis',
            'asset_type':'article','business_role':'customer_facing_production','version':'1','status':'draft',
            'lineage':[],'location_reference':rel(article)
        })
        qa_workflow={'id':'fixture.qa','completion_evidence':{'profile':'qa','strict_qa_target':True}}
        bad_qa=write(WORK/'qa-missing-target.json',{'checks_performed':[{'check':'reviewed'}]})
        errors=validate_evidence(qa_workflow,[rel(bad_qa)],BID)
        req(any('exact tested version' in e for e in errors),f'QA without exact target should fail: {errors}')
        qa=write(WORK/'qa.json',{
            'tested_asset':'ast_fixture','tested_version':'1',
            'checks_performed':[{'check':'reviewed target','outcome':'pass'}]
        })
        req(not validate_evidence(qa_workflow,[rel(qa)],BID),'QA with real target/version should pass structural verification')
        payload=json.loads(qa.read_text());payload['checks_performed'][0]['tool_output_ref']='instances/missing/tool-output.txt';write(qa,payload)
        errors=validate_evidence(qa_workflow,[rel(qa)],BID)
        req(any('unresolved reference' in e for e in errors),f'QA must not cite missing evidence: {errors}')

        errors=validate_evidence({'id':'fixture.generic'},['instances/missing/nope.txt'],BID)
        req(any('unresolved or empty reference' in e for e in errors),f'missing evidence reference should fail: {errors}')
        req(not (ROOT/'runtime'/'runs'/BID).exists(),'structural evidence verification created Run state')
        print('structural evidence boundary regressions passed')
    finally:
        if BASE.exists():shutil.rmtree(BASE)


if __name__=='__main__':main()
