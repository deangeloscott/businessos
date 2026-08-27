#!/usr/bin/env python3
"""Representative Content regressions: enforce real work without benchmark-shaped output rules."""
from pathlib import Path
import json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import completion_spec, contract_index, validate_evidence
from context_plan import build_plan

BID='content-native-execution';BASE=ROOT/'instances'/BID;RUNS=ROOT/'runtime'/'runs'/BID

def req(condition,message):
    if not condition:raise AssertionError(message)

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text((json.dumps(value,indent=2)+'\n') if not isinstance(value,str) else value,encoding='utf-8')
    return path

def rel(path):return path.relative_to(ROOT).as_posix()

def asset(aid,run_id,contract_id,location,source_id,version='1'):
    obj={
        'id':aid,'object_type':'Asset','business_id':BID,'owner_system':'content-synthesis',
        'asset_type':contract_id.rsplit('.',1)[-1],'business_role':'customer_facing_production',
        'version':version,'status':'draft','lineage':[source_id],'location_reference':rel(location),
        'extensions':{'businessos':{'run_ref':f'runtime/runs/{BID}/{run_id}','run_id':run_id,
            'run_contract_id':contract_id,'customer_facing':True,'contract_chain':[contract_id]}},
    }
    write(BASE/'assets'/f'{aid}.json',obj)
    return obj

def main():
    for path in (BASE,RUNS):
        if path.exists():shutil.rmtree(path)
    try:
        cp=subprocess.run([sys.executable,str(S/'init_business.py'),BID,'--name','Content Native Execution'],cwd=ROOT,capture_output=True,text=True)
        req(cp.returncode==0,f'init failed: {cp.stderr+cp.stdout}')
        contracts=contract_index()

        for cid,default in (
            ('content.intelligence.content-performance-analysis','systems/content-synthesis/contracts/intelligence/DEFAULTS.md'),
            ('content.production.podcast','systems/content-synthesis/contracts/production/DEFAULTS.md'),
            ('content.qa.accessibility','systems/content-synthesis/contracts/qa/DEFAULTS.md'),
        ):
            plan=build_plan(BID,cid)
            req(default in plan['files'],f'{cid} did not inherit {default}')
        req(completion_spec(contracts['content.intelligence.content-performance-analysis'])['profile']=='intelligence','Content intelligence must use the shared intelligence evidence profile')
        req(completion_spec(contracts['content.qa.accessibility'])['strict_qa_target'] is True,'Asset QA must target an existing exact Asset version')

        source_id=f'src_{BID}_sample'
        captured=('Practical guide A received 120 qualified actions from 2400 views. '
            'Broad trend summary B received 30 qualified actions from 1800 views. '
            'Both assets ran on the same platform during the completed measurement window; paid amplification is unknown.')
        write(BASE/'intelligence'/'sources'/f'{source_id}.json',{
            'id':source_id,'object_type':'SourceRecord','business_id':BID,'source_type':'first_party',
            'source_reference':'local content performance export','status':'active',
            'extensions':{'businessos_evidence':{'capture_status':'captured','capture_method':'text_excerpt','captured_text':captured}}
        })

        # Intelligence still requires real, reconstructable support rather than a plausible conclusion.
        irun='run_intelligence_fixture'
        insight=write(RUNS/irun/'artifacts'/'insight.json',{
            'id':'ins_content_native_sample','object_type':'Insight','business_id':BID,
            'statement':'Practical guides outperform broad trend summaries.','evidence_links':[]
        })
        errors=validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight)],BID,irun)
        req(any('work record' in e for e in errors),f'shallow canonical conclusion should fail intelligence completion: {errors}')
        fabricated=write(RUNS/irun/'artifacts'/'fabricated-analysis-work-record.json',{
            'contract_id':'content.intelligence.content-performance-analysis','status':'completed',
            'method':{'selection':'Compared claimed creator results','normalization':'Used a claimed multiplier'},
            'evidence_sample':[{'ref':source_id,'support_excerpt':'Dispatch Digest achieved 4.2x engagement.','observation':'A named creator allegedly outperformed.'}],
            'findings':[{'statement':'Copy the named creator pattern.','evidence_refs':[source_id,'src_missing_creator'],'mechanism':'A tactical format allegedly increases attention.'}],
            'limitations':['No captured creator item was available.'],'recommended_actions':['Capture the real item before deciding.']
        })
        errors=validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight),rel(fabricated)],BID,irun)
        req(any('literal support_excerpt' in e and 'unresolved' in e for e in errors),f'fabricated/unresolved intelligence support should fail: {errors}')
        record=write(RUNS/irun/'artifacts'/'analysis-work-record.json',{
            'contract_id':'content.intelligence.content-performance-analysis','status':'completed',
            'method':{'selection':'Compared same-platform assets in the completed measurement window','normalization':'Compared qualified actions per view'},
            'evidence_sample':[{'ref':source_id,'support_excerpt':'Practical guide A received 120 qualified actions from 2400 views.','observation':'The export contains item-level views and qualified actions for the practical guide.'}],
            'findings':[{'statement':'Practical implementation content is the stronger candidate for the next matched test.','evidence_refs':[source_id],'mechanism':'Concrete workflow detail may reduce evaluation uncertainty for operations buyers.'}],
            'limitations':['The bounded sample cannot establish causality and paid amplification is unknown.'],
            'recommended_actions':['Run a matched practical-guide versus trend-summary test with aligned distribution.']
        })
        req(not validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight),rel(record)],BID,irun),'compact but auditable intelligence work should satisfy the structural floor')

        # Podcast: reject a keyword shell and false production claims, not legitimate brevity.
        prun='run_podcast_fixture';podcast=write(RUNS/prun/'artifacts'/'podcast.md',"""# Strategic Production Deliverable
Required elements: audio, segment, script. Alternative elements: edit, timing, show notes, talking points.
This file merely says those things exist.
""")
        asset('ast_content_native_podcast',prun,'content.production.podcast',podcast,source_id)
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(errors,f'podcast keyword shell should fail: {errors}')
        valid_podcast="""# The operating signal hidden in routine work
Listener promise: operations leaders will learn how to distinguish a useful workflow signal from a vanity metric.
Audience and listening context: a focused solo episode. Episode length: 8 minutes.

## Cold Open — 00:00
Script: Start with the decision the listener must make this week and define the evidence boundary.

## Segment 1 — 01:30
Script: Compare the practical guide with the trend summary, explain the observed rates, and state that paid amplification is unknown.

## Segment 2 — 04:00
Script: Explain why concrete workflow detail is worth testing without turning the observation into a causal claim.

## Close — 07:30
Script: Summarize the decision. Call to action: run one matched content test before choosing the next format.

## Source notes
Use the local content-performance source record and verify quantitative statements before recording.

## Edit, timing, and audio direction
Use clean room tone and one short transition cue between sections. Future mastering target: -16 LUFS after audio exists.

## Show notes
Episode summary, evidence limitation, and the matched-test next step.
"""
        write(podcast,valid_podcast)
        req(not validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun),'real concise podcast recording packet should satisfy structural integrity')
        write(podcast,valid_podcast.replace('Episode length: 8 minutes.','Episode length: 5 minutes.'))
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(errors,f'podcast whose own final timecode exceeds its claimed duration should fail: {errors}')
        write(podcast,valid_podcast.replace('Future mastering target: -16 LUFS after audio exists.','Mastered to -16 LUFS.'))
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(errors,f'text fallback must not claim nonexistent mastered audio: {errors}')
        write(podcast,valid_podcast)

        # Presentation: a shell fails, but an appropriate five-slide presentation does not
        # fail merely because a prior bad calibration also happened to have five slides.
        srun='run_presentation_fixture';slides=write(RUNS/srun/'artifacts'/'presentation.md',"""# Strategic Production Deliverable
Required elements: slide, audience, duration. Alternative elements: speaker notes, visual, chart, diagram.
This file describes a future presentation without building it.
""")
        asset('ast_content_native_presentation',srun,'content.production.presentation',slides,source_id)
        errors=validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID,srun)
        req(errors,f'presentation keyword shell should fail: {errors}')
        write(slides,"""# Five-slide decision presentation
Audience: operations leaders. Objective: choose whether to run a matched content test.

## Slide 1: The decision
Visible copy: We need to choose the next content test, not declare a permanent winner.
Visual direction: simple two-path decision diagram.
Speaker notes: frame the decision and the evidence limit.

## Slide 2: What we observed
Visible copy: Practical guide A: 120 qualified actions / 2,400 views. Trend summary B: 30 / 1,800.
Visual direction: side-by-side rate comparison with the raw counts visible.
Speaker notes: explain normalization and that paid amplification is unknown.

## Slide 3: What it may mean
Visible copy: Concrete workflow detail is the stronger mechanism candidate.
Visual direction: mechanism chain from specificity to reduced evaluation uncertainty.
Speaker notes: separate the mechanism hypothesis from causality.

## Slide 4: What could change our mind
Visible copy: Distribution mix, topic timing, and audience differences remain plausible alternatives.
Visual direction: three-column uncertainty panel.
Speaker notes: state what additional evidence would change the decision.

## Slide 5: Next step
Visible copy: Run one matched practical-guide vs. trend-summary test with aligned distribution.
Visual direction: compact experiment card with owner, window, and decision rule placeholders.
Speaker notes: close with the approval decision and next action.

Source attribution: local content-performance SourceRecord. CTA / decision close: approve or reject the matched test.
""")
        req(not validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID,srun),'legitimate five-slide production specification must not fail an arbitrary six-slide rule')

        # QA: fake/self-targeted checks and claimed automation without tool output still fail.
        qrun='run_qa_fixture';badqa=write(RUNS/qrun/'artifacts'/'qa.json',{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_qa_wrapper','tested_version':'1',
            'checks_performed':[{'check':'compliance_validation','passed':True,'result':'Verified full compliance for contract content.qa.accessibility.'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]
        })
        asset('ast_qa_wrapper',qrun,'content.qa.accessibility',badqa,source_id)
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun)
        req(any('non-self target Asset' in e for e in errors),f'canned/self-targeted QA should fail: {errors}')
        write(badqa,{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1',
            'checks_performed':[{'check':'diagram alt text','status':'pass','method':'Inspected every diagram and its alt text','finding':'Every diagram has descriptive alt text.','target_excerpt':'Diagram: roast profile comparison'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]
        })
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun)
        req(errors,f'QA claim about absent target content should fail: {errors}')
        write(badqa,{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1',
            'checks_performed':[{'check':'readability score','status':'pass','method':'Automated Flesch-Kincaid scanner over the complete script','finding':'The automated scan confirmed the target reading level.','target_excerpt':'Listener promise: operations leaders'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]
        })
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun)
        req(errors,f'automated QA claim without saved tool output should fail: {errors}')
        tool_output=write(RUNS/qrun/'artifacts'/'readability-scan.txt','Flesch-Kincaid grade: 8.2\nTarget: complete podcast script\n')
        automated=json.loads(badqa.read_text(encoding='utf-8')); automated['checks_performed'][0]['tool_output_ref']=rel(tool_output); write(badqa,automated)
        req(not validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun),'automated QA with resolvable saved tool output should satisfy the evidence requirement')
        write(badqa,{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1',
            'checks_performed':[
                {'check':'transcript availability','status':'pass','method':'Inspected the complete recording packet for a usable spoken transcript','finding':'The spoken script is present in ordered sections and can serve as the recording transcript.','target_component':'complete spoken-script structure'},
                {'check':'audio-only information','status':'pass','method':'Reviewed each section for unexplained visual dependencies','finding':'No section depends on an unseen chart, gesture, or visual-only distinction.','target_component':'whole episode script'},
                {'check':'language clarity','status':'pass','method':'Reviewed the listener promise, transitions, and close for comprehension','finding':'The episode defines its evidence boundary and ends with one explicit next action.','target_excerpt':'Call to action: run one matched content test'}
            ],
            'issues_found':[],'corrections_made':[],'limitations':['Rendered-audio loudness requires recheck after recording.'],'blockers':[]
        })
        req(not validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun),'target-specific substantive QA may use concrete whole-asset components instead of ceremonial excerpts')

        print('representative outcome-first Content execution regressions passed')
    finally:
        for path in (BASE,RUNS):
            if path.exists():shutil.rmtree(path)

if __name__=='__main__':main()
