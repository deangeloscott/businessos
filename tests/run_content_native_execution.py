#!/usr/bin/env python3
"""Representative family regressions derived from Content Calibration F."""
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

        # Family defaults are inherited automatically through the portable context plan.
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

        # Intelligence: a one-statement canonical Insight reproduces F and is not the analysis.
        irun='run_intelligence_fixture'
        insight=write(RUNS/irun/'artifacts'/'insight.json',{
            'id':'ins_content_native_sample','object_type':'Insight','business_id':BID,
            'statement':'Practical guides outperform broad trend summaries.','evidence_links':[]
        })
        errors=validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight)],BID,irun)
        req(any('work record' in e for e in errors),f'shallow canonical conclusion should fail intelligence completion: {errors}')
        fabricated=write(RUNS/irun/'artifacts'/'fabricated-analysis-work-record.json',{
            'contract_id':'content.intelligence.content-performance-analysis','status':'completed',
            'analysis_scope':{'decision':'Choose a creator tactic','period':'current window'},
            'method':{'selection':'Compared claimed creator results','normalization':'Used a claimed multiplier'},
            'evidence_sample':[{'ref':source_id,'support_excerpt':'Dispatch Digest achieved 4.2x engagement.','observation':'A named creator allegedly outperformed.'}],
            'comparisons':[{'baseline':'claimed average','result':'claimed 4.2x result'}],
            'findings':[{'statement':'Copy the named creator pattern.','evidence_refs':[source_id,'src_missing_creator'],
                'mechanism':'A tactical format allegedly increases attention.','alternative_explanations':['Audience size may differ.']}],
            'limitations':['No captured creator item was available.'],'recommended_actions':['Capture the real item before deciding.']
        })
        errors=validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight),rel(fabricated)],BID,irun)
        req(any('literal support_excerpt' in e and 'unresolved' in e for e in errors),f'fabricated/unresolved intelligence support should fail: {errors}')
        record=write(RUNS/irun/'artifacts'/'analysis-work-record.json',{
            'contract_id':'content.intelligence.content-performance-analysis','status':'completed',
            'analysis_scope':{'decision':'Choose the next content mechanism','period':'Last completed measurement window','population':'Comparable practical and trend articles'},
            'method':{'selection':'Included same-platform assets with aligned objectives and measurement windows','normalization':'Compared qualified actions per view within format cohorts'},
            'evidence_sample':[{'ref':source_id,'support_excerpt':'Practical guide A received 120 qualified actions from 2400 views.',
                'observation':'The captured export contains item-level reach and qualified actions for the practical guide.'}],
            'comparisons':[{'baseline':'Within-format median qualified actions per view','result':'Practical guides exceeded the broad-trend cohort while paid status remained unknown.'}],
            'findings':[{'statement':'Practical implementation content is the stronger candidate for the next test.','evidence_refs':[source_id],
                'mechanism':'Concrete workflow detail may reduce evaluation uncertainty for operations buyers.',
                'alternative_explanations':['Distribution mix and topic timing may explain part of the observed difference.']}],
            'limitations':['The bounded sample cannot establish causality and paid amplification is not known for every item.'],
            'recommended_actions':['Run a matched practical-guide versus trend-summary test with the same distribution window.']
        })
        req(not validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight),rel(record)],BID,irun),
            'auditable intelligence work record plus canonical result should satisfy the structural floor')

        # Production: Calibration-F-style keyword shells fail the promised-medium floor.
        prun='run_podcast_fixture';podcast=write(RUNS/prun/'artifacts'/'podcast.md',"""# Strategic Production Deliverable

## Overview & Business Context
This audience-facing deliverable presents the complete operational strategy and production execution.

## Production Packet Specification
- Required Elements: audio, segment, script.
- Alternative Elements: edit, timing, show notes, talking points.

## Execution Summary & Technical Quality
Grounded in source evidence and aligned with business goals.
""")
        asset('ast_content_native_podcast',prun,'content.production.podcast',podcast,source_id)
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(any('complete production packet' in e for e in errors),f'podcast keyword shell should fail: {errors}')
        write(podcast,('# Podcast packet\nListener promise and audience context. Segment script with timing, audio direction, edit direction, source notes, CTA, and show notes. '
            'The host explains a concrete operating problem, repeats the setup, and promises transitions without supplying timecodes or actual cues. ')*22)
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(any('complete production packet' in e for e in errors),f'long podcast prose without concrete timecodes/cues should fail: {errors}')
        segment_body=('The host explains one concrete operating problem, connects it to the source evidence, gives a worked example, '
            'states what remains uncertain, and hands the listener to the next idea with a natural transition. ')*5
        write(podcast,f"""# The operating signal hidden in routine work
Listener promise: operations leaders will learn how to distinguish a useful workflow signal from a vanity metric.
Audience and listening context: a focused solo episode for an operations commute. Episode length: 8 minutes.

## Cold Open — 00:00
Script: Start with the decision the listener must make this week. {segment_body}

## Segment 1 — 01:00
Script: Establish the comparison and define the baseline. {segment_body}

## Segment 2 — 03:00
Script: Walk through the mechanism and the strongest alternative explanation. {segment_body}

## Segment 3 — 05:30
Script: Turn the finding into a bounded test and explain the stopping condition. {segment_body}

## Close — 07:30
Script: Summarize the decision. Call to action: review one matched content cohort before choosing the next format.

## Research notes and source notes
Use the local content-performance source record; qualify causal language and verify every quantitative statement before recording.

## Edit, timing, and audio direction
Use clean room tone, short pauses between segments, and one audible transition. Remove repeated setup during the edit.

## Show notes
Episode summary, three decision points, the evidence limitation, and the next-step checklist. Episode notes include the source attribution.
""")
        req(not validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun),'complete podcast recording packet should satisfy the structural fallback floor')
        valid_podcast=podcast.read_text(encoding='utf-8')
        write(podcast,valid_podcast.replace('Episode length: 8 minutes.','Episode length: 18 minutes.').replace('07:30','17:30'))
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(any('complete production packet' in e for e in errors),f'podcast timing claim inconsistent with its script length should fail: {errors}')
        write(podcast,valid_podcast.replace('Use clean room tone','Mastered to -16 LUFS. Use clean room tone'))
        errors=validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID,prun)
        req(any('complete production packet' in e for e in errors),f'text fallback must not claim nonexistent mastered audio: {errors}')

        srun='run_presentation_fixture';slides=write(RUNS/srun/'artifacts'/'presentation.md',"""# Strategic Production Deliverable

Required elements: slide, audience, duration. Alternative elements: speaker notes, visual, chart, diagram.
This file describes a future presentation.
""")
        asset('ast_content_native_presentation',srun,'content.production.presentation',slides,source_id)
        errors=validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID,srun)
        req(any('complete production packet' in e for e in errors),f'presentation keyword shell should fail: {errors}')
        thin_slide=('Visible copy: one short message. Visual direction: use a simple diagram. Speaker notes: explain the point. ')
        write(slides,"# Five-slide presentation\nAudience: operators. Objective: decide. Duration: twelve minutes. Source attribution and CTA next step.\n\n"+
            '\n'.join(f'## Slide {i}: Topic\n{thin_slide}' for i in range(1,6)))
        errors=validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID,srun)
        req(any('complete production packet' in e for e in errors),f'five thin slides without numeric complete build detail should fail: {errors}')
        slide_detail=('Visible copy states one decision-relevant message with a concrete example and a short qualifier. '
            'Visual direction uses a simple diagram rather than decorative stock imagery. Speaker notes explain the evidence, transition, and audience question. ')*3
        write(slides,"""# Presentation production specification
Audience: operations leaders. Setting: live review. Objective: choose a matched content test. Duration: 12 minutes.
Source and proof attribution: use the local source record and label the causal limitation. Decision close: approve or reject the bounded test.

"""+'\n'.join(f"## Slide {i}: Decision step {i}\n{slide_detail}\nSpeaker notes: connect slide {i} to the next decision and retain the evidence qualifier.\n" for i in range(1,7))+
            "\n## CTA / next step\nChoose the test owner, measurement window, and stopping condition.\n")
        req(not validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID,srun),'complete slide-by-slide packet should satisfy the structural fallback floor')

        # QA: a boilerplate pass aimed at its own wrapper Asset fails; concrete checks on
        # an existing production Asset/version pass the reusable QA evidence floor.
        qrun='run_qa_fixture';badqa=write(RUNS/qrun/'artifacts'/'qa.json',{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_qa_wrapper','tested_version':'1',
            'checks_performed':[{'check':'compliance_validation','passed':True,'result':'Verified full compliance for contract content.qa.accessibility.'},
                {'check':'quality_assurance','passed':True,'result':'Quality assurance passed all criteria for asset ast_qa_wrapper.'}],
            'blockers':[]
        })
        asset('ast_qa_wrapper',qrun,'content.qa.accessibility',badqa,source_id)
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun)
        req(any('non-self target Asset' in e for e in errors),f'canned/self-targeted QA should fail: {errors}')
        write(badqa,{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1',
            'checks_performed':[{'check':'diagram alt text','status':'pass','method':'Inspected every diagram and its alt text',
                'finding':'Every diagram has descriptive alt text.','target_excerpt':'Diagram: roast profile comparison'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]
        })
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun)
        req(any('structured JSON QA pass record' in e for e in errors),f'QA claim about absent target content should fail: {errors}')
        write(badqa,{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1',
            'checks_performed':[{'check':'readability score','status':'pass','method':'Automated Flesch-Kincaid scanner over the complete script',
                'finding':'The automated scan confirmed the target reading level.','target_excerpt':'Listener promise: operations leaders'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]
        })
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun)
        req(any('structured JSON QA pass record' in e for e in errors),f'automated QA claim without saved tool output should fail: {errors}')
        tool_output=write(RUNS/qrun/'artifacts'/'readability-scan.txt','Flesch-Kincaid grade: 8.2\nTarget: complete podcast script\n')
        automated=json.loads(badqa.read_text(encoding='utf-8')); automated['checks_performed'][0]['tool_output_ref']=rel(tool_output); write(badqa,automated)
        req(not validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun),'automated QA with resolvable saved tool output should satisfy the evidence requirement')
        write(badqa,{
            'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1',
            'checks_performed':[
                {'check':'transcript availability','status':'pass','method':'Compared the recording packet with the transcript section','finding':'The complete spoken script is present in ordered segments and can serve as the recording transcript.','target_excerpt':'Script: Start with the decision the listener must make this week.'},
                {'check':'audio-only information','status':'pass','method':'Reviewed each segment for unexplained visual references','finding':'No segment depends on a chart, gesture, or visual-only distinction to convey its main point.','target_excerpt':'The host explains one concrete operating problem'},
                {'check':'language clarity','status':'pass','method':'Reviewed headings, transitions, and CTA for listener comprehension','finding':'The episode defines its baseline before analysis and states one explicit next action in the close.','target_excerpt':'Call to action: review one matched content cohort'}
            ],
            'issues_found':[],'corrections_made':[],'limitations':['Rendered-audio loudness and timing require recheck after recording.'],'blockers':[]
        })
        req(not validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID,qrun),'target-specific substantive QA should satisfy the structural floor')

        print('representative Content native-execution family regressions passed')
    finally:
        for path in (BASE,RUNS):
            if path.exists():shutil.rmtree(path)

if __name__=='__main__':main()
