#!/usr/bin/env python3
"""Representative Content regressions: real output quality without Run/execution ceremony."""
from pathlib import Path
import json,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1];S=ROOT/'scripts';sys.path.insert(0,str(S))
from completion_evidence import completion_spec,contract_index,validate_evidence
from context_plan import build_plan

BID='content-native-execution';BASE=ROOT/'instances'/BID;WORK=BASE/'verification'

def req(condition,message):
    if not condition:raise AssertionError(message)
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text((json.dumps(value,indent=2)+'\n') if not isinstance(value,str) else value,encoding='utf-8');return path
def rel(path):return path.relative_to(ROOT).as_posix()
def asset(aid,contract_id,location,source_id,version='1'):
    obj={'id':aid,'object_type':'Asset','business_id':BID,'owner_system':'content-synthesis','asset_type':contract_id.rsplit('.',1)[-1],'business_role':'customer_facing_production','version':version,'status':'draft','lineage':[source_id],'location_reference':rel(location),'extensions':{'businessos':{'customer_facing':True}}}
    write(BASE/'assets'/f'{aid}.json',obj);return obj

def main():
    if BASE.exists():shutil.rmtree(BASE)
    try:
        cp=subprocess.run([sys.executable,str(S/'init_business.py'),BID,'--name','Content Native Execution'],cwd=ROOT,capture_output=True,text=True)
        req(cp.returncode==0,f'init failed: {cp.stderr+cp.stdout}')
        contracts=contract_index()

        for cid,default in (
            ('content.intelligence.content-performance-analysis','systems/content-synthesis/contracts/intelligence/DEFAULTS.md'),
            ('content.production.podcast','systems/content-synthesis/contracts/production/DEFAULTS.md'),
            ('content.qa.accessibility','systems/content-synthesis/contracts/qa/DEFAULTS.md'),
        ):
            req(default in build_plan(BID,cid)['files'],f'{cid} did not inherit {default}')
        req(completion_spec(contracts['content.intelligence.content-performance-analysis'])['profile']=='intelligence','Content intelligence lost its evidence profile')
        req(completion_spec(contracts['content.qa.accessibility'])['strict_qa_target'] is True,'Asset QA must target an exact existing Asset version')

        source_id=f'src_{BID}_sample';captured=('Practical guide A received 120 qualified actions from 2400 views. Broad trend summary B received 30 qualified actions from 1800 views. Both assets ran on the same platform during the completed measurement window; paid amplification is unknown.')
        write(BASE/'intelligence'/'sources'/f'{source_id}.json',{'id':source_id,'object_type':'SourceRecord','business_id':BID,'source_type':'first_party','source_reference':'local content performance export','status':'active','extensions':{'businessos_evidence':{'capture_status':'captured','capture_method':'text_excerpt','captured_text':captured}}})

        # Intelligence must remain reconstructable rather than merely plausible.
        insight=write(WORK/'intelligence'/'insight.json',{'id':'ins_content_native_sample','object_type':'Insight','business_id':BID,'statement':'Practical guides outperform broad trend summaries.','evidence_links':[]})
        errors=validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight)],BID)
        req(any('work record' in e for e in errors),f'shallow conclusion should fail intelligence evidence: {errors}')
        fabricated=write(WORK/'intelligence'/'fabricated-analysis.json',{'contract_id':'content.intelligence.content-performance-analysis','status':'completed','method':{'selection':'Compared claimed creator results','normalization':'Used a claimed multiplier'},'evidence_sample':[{'ref':source_id,'support_excerpt':'Dispatch Digest achieved 4.2x engagement.','observation':'A named creator allegedly outperformed.'}],'findings':[{'statement':'Copy the named creator pattern.','evidence_refs':[source_id,'src_missing_creator'],'mechanism':'A tactical format allegedly increases attention.'}],'limitations':['No captured creator item was available.'],'recommended_actions':['Capture the real item before deciding.']})
        errors=validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight),rel(fabricated)],BID)
        req(any('literal support_excerpt' in e and 'unresolved' in e for e in errors),f'fabricated/unresolved support should fail: {errors}')
        record=write(WORK/'intelligence'/'analysis.json',{'contract_id':'content.intelligence.content-performance-analysis','status':'completed','method':{'selection':'Compared same-platform assets in the completed measurement window','normalization':'Compared qualified actions per view'},'evidence_sample':[{'ref':source_id,'support_excerpt':'Practical guide A received 120 qualified actions from 2400 views.','observation':'The export contains item-level views and qualified actions.'}],'findings':[{'statement':'Practical implementation content is the stronger candidate for the next matched test.','evidence_refs':[source_id],'mechanism':'Concrete workflow detail may reduce evaluation uncertainty for operations buyers.'}],'limitations':['The bounded sample cannot establish causality and paid amplification is unknown.'],'recommended_actions':['Run a matched practical-guide versus trend-summary test with aligned distribution.']})
        req(not validate_evidence(contracts['content.intelligence.content-performance-analysis'],[rel(insight),rel(record)],BID),'compact auditable intelligence should pass without a Run')

        # Production checks reject keyword shells and false production claims, not brevity.
        podcast=write(WORK/'production'/'podcast.md','# Strategic Production Deliverable\nRequired elements: audio, segment, script. Alternative elements: edit, timing, show notes.\nThis file merely says those things exist.\n')
        asset('ast_content_native_podcast','content.production.podcast',podcast,source_id)
        req(validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID),'podcast keyword shell should fail')
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
Use clean room tone and one short transition cue. Future mastering target: -16 LUFS after audio exists.
## Show notes
Episode summary, evidence limitation, and the matched-test next step.
"""
        write(podcast,valid_podcast);req(not validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID),'real concise podcast specification should pass without Run provenance')
        write(podcast,valid_podcast.replace('Episode length: 8 minutes.','Episode length: 5 minutes.'));req(validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID),'self-contradictory duration should fail')
        write(podcast,valid_podcast.replace('Future mastering target: -16 LUFS after audio exists.','Mastered to -16 LUFS.'));req(validate_evidence(contracts['content.production.podcast'],[rel(podcast)],BID),'text fallback must not claim nonexistent mastered audio')
        write(podcast,valid_podcast)

        slides=write(WORK/'production'/'presentation.md','# Strategic Production Deliverable\nRequired elements: slide, audience, duration. Alternative elements: speaker notes, visual.\nThis file describes a future presentation without building it.\n')
        asset('ast_content_native_presentation','content.production.presentation',slides,source_id)
        req(validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID),'presentation keyword shell should fail')
        write(slides,"""# Five-slide decision presentation
Audience: operations leaders. Objective: choose whether to run a matched content test.
## Slide 1: The decision
Visible copy: Choose the next test, not a permanent winner. Visual direction: two-path decision diagram. Speaker notes: frame the evidence limit.
## Slide 2: What we observed
Visible copy: Practical guide A: 120/2,400. Trend summary B: 30/1,800. Visual direction: side-by-side rates. Speaker notes: paid amplification is unknown.
## Slide 3: What it may mean
Visible copy: Concrete workflow detail is the stronger mechanism candidate. Visual direction: mechanism chain. Speaker notes: separate hypothesis from causality.
## Slide 4: What could change our mind
Visible copy: Distribution mix, timing, and audience differences remain alternatives. Visual direction: uncertainty panel. Speaker notes: state disconfirming evidence.
## Slide 5: Next step
Visible copy: Run one matched practical-guide vs. trend-summary test. Visual direction: compact experiment card. Speaker notes: close with the decision.
Source attribution: local content-performance SourceRecord. CTA: approve or reject the matched test.
""")
        req(not validate_evidence(contracts['content.production.presentation'],[rel(slides)],BID),'legitimate five-slide specification must not fail an arbitrary count rule')

        # QA validates the actual target Asset/version without any receipt relationship.
        badqa=write(WORK/'qa'/'qa.json',{'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_qa_wrapper','tested_version':'1','checks_performed':[{'check':'compliance_validation','passed':True,'result':'Verified full compliance.'}],'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]})
        asset('ast_qa_wrapper','content.qa.accessibility',badqa,source_id)
        errors=validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID);req(any('non-self target Asset' in e for e in errors),f'self-targeted QA should fail: {errors}')
        write(badqa,{'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1','checks_performed':[{'check':'diagram alt text','status':'pass','method':'Inspected every diagram and its alt text','finding':'Every diagram has descriptive alt text.','target_excerpt':'Diagram: roast profile comparison'}],'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]})
        req(validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID),'QA claim about absent target content should fail')
        write(badqa,{'contract_id':'content.qa.accessibility','status':'pass','tested_asset':'ast_content_native_podcast','tested_version':'1','checks_performed':[{'check':'readability score','status':'pass','method':'Automated Flesch-Kincaid scanner over the complete script','finding':'The automated scan confirmed the target reading level.','target_excerpt':'Listener promise: operations leaders'}],'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[]})
        req(validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID),'automated QA without saved tool output should fail')
        tool_output=write(WORK/'qa'/'readability-scan.txt','Flesch-Kincaid grade: 8.2\nTarget: complete podcast script\n');automated=json.loads(badqa.read_text());automated['checks_performed'][0]['tool_output_ref']=rel(tool_output);write(badqa,automated)
        req(not validate_evidence(contracts['content.qa.accessibility'],[rel(badqa)],BID),'automated QA with real tool output should pass')

        req(not (ROOT/'runtime'/'runs'/BID).exists(),'Content quality regression created Run state')
        print('representative Content quality regressions passed without Run/execution ceremony')
    finally:
        if BASE.exists():shutil.rmtree(BASE)

if __name__=='__main__':main()
