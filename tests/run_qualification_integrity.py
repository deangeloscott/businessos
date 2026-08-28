#!/usr/bin/env python3
from pathlib import Path
import json, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qualification'))
from integrity import (
    artifact_similarity_flags, checkpoint_chain_contiguous, declared_write_absence_justified,
    event_specific_ref_paths, is_structured_prepublish_record, integrity_hard_failure,
    is_reconstructable_field_snapshot, run_control_flags, selector_types,
)
from build_suite import build


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def main():
    req(selector_types(['Asset',{'type':'Observation'},{'object_type':'Learning'}])=={'Asset','Observation','Learning'},'write selector normalization failed')

    with tempfile.TemporaryDirectory(prefix='aura-qualification-integrity-') as td:
        root=Path(td); ws=root/'workspace'; ws.mkdir(); p=ws/'attachments'/'field.json'; p.parent.mkdir(parents=True); p.write_text('new evidence\n')
        before={'workspace':{'files':[]}}
        after={'workspace':{'digest':'after-digest','files':[{'path':'attachments\\field.json','sha256':'abc'}]}}
        req(event_specific_ref_paths(['attachments/field.json'],before,after,ws),'new event field snapshot must be recognized')
        same_before={'workspace':{'files':[{'path':'attachments/field.json','sha256':'abc'}]}}
        req(not event_specific_ref_paths(['attachments/field.json'],same_before,after,ws),'unchanged recycled field snapshot must not count as event-specific evidence')
        req(checkpoint_chain_contiguous({'workspace':{'digest':'same'}},{'workspace':{'digest':'same'}}),'matching adjacent checkpoint digests should be contiguous')
        req(not checkpoint_chain_contiguous({'workspace':{'digest':'prior'}},{'workspace':{'digest':'mutated'}}),'between-event workspace mutation must break checkpoint continuity')

        bad_field=root/'bad-field.json';bad_field.write_text(json.dumps({'captured_at':'2026-08-26T00:00:00Z','competitive_set':[{'name':'Industry benchmark'},{'name':'Category competitor'}]}))
        req(not is_reconstructable_field_snapshot(bad_field,ws),'unnamed/source-free synthetic field evidence must not be reconstructable')
        placeholder_field=root/'placeholder-field.json';placeholder_field.write_text(json.dumps({'captured_at':'2026-08-26T00:00:00Z','query':'field service software','sources':[{'name':'A','source_url':'https://example.invalid/a'},{'name':'B','source_url':'https://example.invalid/b'}]}))
        req(not is_reconstructable_field_snapshot(placeholder_field,ws),'reserved placeholder URLs must not count as reconstructable field evidence')
        good_field=root/'good-field.json';good_field.write_text(json.dumps({'captured_at':'2026-08-26T00:00:00Z','query':'field service software','sources':[{'name':'A','source_url':'https://www.servicetitan.com/'},{'name':'B','source_url':'https://www.housecallpro.com/'}]}))
        req(is_reconstructable_field_snapshot(good_field,ws),'source-linked field evidence should be reconstructable')

        canonical=root/'canonical-source-record.json';canonical.write_text(json.dumps({
            'id':'src_atlasops_field','object_type':'SourceRecord','schema_version':'1.0.0','business_id':'atlasops',
            'source_type':'web_research','source_reference':'https://www.vonigo.com/product/franchise-service-software/',
            'retrieved_at':'2026-08-27T22:00:00Z','access_scope':'public',
            'extensions':{
                'query':'field service scheduling software for multi-location teams',
                'results':[
                    {'name':'Vonigo','url':'https://www.vonigo.com/product/franchise-service-software/'},
                    {'name':'ServiceTitan','url':'https://www.servicetitan.com/commercial'}
                ]
            }
        }))
        req(is_reconstructable_field_snapshot(canonical,ws),'canonical SourceRecord evidence with query context and two real locators should be reconstructable')
        canonical_one=root/'canonical-one-source.json';canonical_one.write_text(json.dumps({
            'id':'src_atlasops_one','object_type':'SourceRecord','schema_version':'1.0.0','business_id':'atlasops',
            'source_type':'web_research','source_reference':'https://www.vonigo.com/product/franchise-service-software/',
            'retrieved_at':'2026-08-27T22:00:00Z','access_scope':'public',
            'extensions':{'query':'field service scheduling software for multi-location teams'}
        }))
        req(not is_reconstructable_field_snapshot(canonical_one,ws),'canonical SourceRecord with only one real source must still fail reconstructability')

        atlasops_shape=root/'atlasops-shape.json';atlasops_shape.write_text(json.dumps({
            'id':'src_atlasops_serp_multiloc_20260827','object_type':'SourceRecord','schema_version':'1.0.0','business_id':'atlasops',
            'source_type':'webpage','source_reference':'[https://www.vonigo.com/](https://www.vonigo.com/)',
            'retrieved_at':'2026-08-27T22:59:30Z','access_scope':'public',
            'extensions':{
                'target_intent':'field service scheduling software for multi-location teams',
                'analyzed_urls':[
                    '[https://www.vonigo.com/](https://www.vonigo.com/)',
                    '[https://www.servicetitan.com/blog/multi-location-field-service-management](https://www.servicetitan.com/blog/multi-location-field-service-management)',
                    '[https://buildops.com/](https://buildops.com/)'
                ],
                'businessos_evidence':{'capture_status':'captured','acquisition_method':'direct_page_read'}
            }
        }))
        req(is_reconstructable_field_snapshot(atlasops_shape,ws),'canonical SourceRecord target_intent/analyzed_urls aliases and Markdown-wrapped URLs should remain reconstructable')
        atlasops_duplicate=root/'atlasops-duplicate.json';atlasops_duplicate.write_text(json.dumps({
            'id':'src_atlasops_dup','object_type':'SourceRecord','schema_version':'1.0.0','business_id':'atlasops',
            'source_type':'webpage','source_reference':'[https://www.vonigo.com/](https://www.vonigo.com/)',
            'retrieved_at':'2026-08-27T22:59:30Z','access_scope':'public',
            'extensions':{
                'target_intent':'field service scheduling software for multi-location teams',
                'analyzed_urls':['https://www.vonigo.com/','[Vonigo](https://www.vonigo.com/)']
            }
        }))
        req(not is_reconstructable_field_snapshot(atlasops_duplicate,ws),'different wrappers around one URL must not fake the two-distinct-source requirement')

        first_party_a=ws/'attachments'/'performance.json'; first_party_a.write_text('{}')
        first_party_b=ws/'instances'/'business'/'intelligence'/'sources'/'source.json'; first_party_b.parent.mkdir(parents=True); first_party_b.write_text('{}')
        alias_field=root/'alias-field.json';alias_field.write_text(json.dumps({'captured_at':'2026-08-26T00:00:00Z','market_context':{'category':'field service'},'source_references':['attachments/performance.json','instances/business/intelligence/sources/source.json']}))
        req(is_reconstructable_field_snapshot(alias_field,ws),'first-party field snapshot aliases with two resolvable sources should be reconstructable')

        bad=root/'bad-qa.json'; bad.write_text(json.dumps({'contract_id':'content.qa.pre-publish','status':'passed','notes':'QA passed'}))
        req(not is_structured_prepublish_record(bad),'self-attested QA must not pass structural pre-publish evidence check')
        good=root/'good-qa.json'; good.write_text(json.dumps({'contract_id':'content.qa.pre-publish','status':'pass',
            'checks_performed':[{'check':'destination links','passed':True,'method':'Requested every saved destination URL','finding':'Both destination URLs returned successful HTTP responses.'}],
            'issues_found':[],'corrections_made':[],'limitations':[],'blockers':[],'tested_asset':'ast_1','tested_version':'1.0'}))
        req(is_structured_prepublish_record(good),'structured pre-publish evidence should pass')
        req(declared_write_absence_justified('qa',[good]),'clean substantive QA should justify not creating a ceremonial declared corrective object')

        a=root/'a.md'; b=root/'b.md'; c=root/'c.md'
        body='# Deliverable\n\n## Context\nGeneric operational guidance for the target audience.\n\n## Steps\n1. Review the workflow.\n2. Apply the process.\n3. Validate the result.\n'*5
        a.write_text(body); b.write_text(body); c.write_text(body)
        results=[
            {'event_id':'E1','kind':'contract_acceptance','contract_id':'content.production.article','actual_artifacts':[str(a)]},
            {'event_id':'E2','kind':'contract_acceptance','contract_id':'content.production.animation','actual_artifacts':[str(b)]},
            {'event_id':'E3','kind':'contract_acceptance','contract_id':'content.production.carousel','actual_artifacts':[str(c)]},
        ]
        flags=artifact_similarity_flags(results,max_examples=1)
        req('E1' in flags and 'E2' in flags and 'E3' in flags,'highly similar artifacts across distinct contracts must be flagged')
        req(len(flags['E1'])==1 and flags['E1'][0]['type']=='high_artifact_similarity','similarity matches must be compressed to one warning per event')
        req(flags['E1'][0]['match_count']==2 and len(flags['E1'][0]['examples'])==1,'compressed similarity warning must preserve match count and bounded strongest examples')
        req(integrity_hard_failure(flags['E1']),'mass-similar artifacts across distinct contracts must fail qualification integrity')

        runner=root/'run_remaining_queue.py'; runner.write_text('print("mass runner")\n')
        req(run_control_flags(root),'candidate-authored run control script must be surfaced as integrity warning')
        scratch=ws/'scratch';scratch.mkdir()
        mass=scratch/'run_gauntlet.py';mass.write_text("queue='queue.json'\nfor event in events:\n print('checkpoint.py', 'complete_run.py', 'record_contract_completion.py', 'candidate-results', 'receipt_path')\n")
        control=run_control_flags(root,ws)
        req(any(x.get('type')=='mass_completion_runner' and Path(x['path'])==mass for x in control),f'workspace mass-completion runner must be a critical integrity flag: {control}')
        logs=root/'candidate-logs';logs.mkdir()
        log=logs/'candidate.stdout.log';log.write_text('{"tool":"python private/scratch/run_event.py 0"}\nProcessing Event 1/69\nCreated AURA Run: run_fake\nqualification/evaluate_run.py\n')
        logged=run_control_flags(root,ws)
        req(any(x.get('type')=='mass_completion_runner' and x.get('source')=='captured_tool_log' for x in logged),f'private-harness mass runner must be detected from canonical logs: {logged}')
        req(any(x.get('type')=='candidate_evaluator_spec_access' for x in logged),f'evaluator invocation must be detected from canonical logs: {logged}')
        log.write_text(json.dumps({'event':'step_update','step_update':{'tool_info':{'name':'find_by_name','parameters':{'SearchDirectory':str(root)},'output':'evaluator/suite.json\nevaluator/hidden-fixtures'}}})+'\n')
        listed=run_control_flags(root,ws)
        req(not any(x.get('type')=='candidate_evaluator_spec_access' for x in listed),f'a filename returned by directory listing is not evaluator-spec access: {listed}')
        log.write_text(json.dumps({'event':'step_update','step_update':{'tool_info':{'name':'view_file','parameters':{'AbsolutePath':str(root/'evaluator/suite.json')}}}})+'\n')
        accessed=run_control_flags(root,ws)
        req(any(x.get('type')=='candidate_evaluator_spec_access' for x in accessed),f'an explicit evaluator-spec read must remain a critical integrity flag: {accessed}')

    suite=build(); customer=[t for t in suite['contract_tests'] if t.get('artifact_role')=='customer_facing_production_root']
    evaluator=(ROOT/'qualification/evaluate_run.py').read_text()
    req("gates['root_completion_evidence_valid']" in evaluator and "gates['required_subcontract_evidence_valid']" in evaluator,'qualification evaluator must independently revalidate completed Run evidence')
    req(customer and all('prepublish_or_required_qa_recorded' in t['hard_gates'] for t in customer),'customer-facing roots must require structured QA evidence')
    competitive=[t for t in suite['contract_tests'] if t.get('competitive_profile') in {'search_live_field','paid_and_persuasion_field','organic_attention_field'}]
    req(competitive and all({'competitive_field_evidence_event_specific','competitive_field_evidence_reconstructable'} <= set(t['hard_gates']) for t in competitive),'competitive tests must require event-specific reconstructable field evidence')
    artifact_tasks=[t for t in suite['contract_tests'] if t['output_policy'].get('artifact_required')]
    req(artifact_tasks and all('actual_artifact_exists' in t['hard_gates'] and 'artifact_referenced_by_receipt' in t['hard_gates'] for t in artifact_tasks),'artifact tasks must enforce real artifact evidence through evaluator gates rather than candidate prompt coaching')

    print('qualification adversarial integrity regressions passed')

if __name__=='__main__': main()
