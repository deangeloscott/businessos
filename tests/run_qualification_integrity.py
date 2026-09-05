#!/usr/bin/env python3
"""Regression checks that qualification protects real work without becoming a semantic rules engine."""
from pathlib import Path
import json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'qualification'))
from integrity import artifact_similarity_flags,checkpoint_chain_contiguous,event_specific_ref_paths,exact_duplicate_artifact_flags,run_control_flags
from build_suite import build

def req(cond,msg):
    if not cond:raise AssertionError(msg)

def main():
    with tempfile.TemporaryDirectory(prefix='aura-qualification-integrity-') as td:
        root=Path(td);ws=root/'workspace';ws.mkdir();p=ws/'attachments'/'field.json';p.parent.mkdir(parents=True);p.write_text('new evidence\n');before={'workspace':{'files':[]}};after={'workspace':{'digest':'after','files':[{'path':'attachments\\field.json','sha256':'abc'}]}}
        req(event_specific_ref_paths(['attachments/field.json'],before,after,ws),'new event evidence must be auditable as event-specific');req(not event_specific_ref_paths(['attachments/field.json'],{'workspace':{'files':[{'path':'attachments/field.json','sha256':'abc'}]}},after,ws),'unchanged prior evidence must not count as event-specific');req(checkpoint_chain_contiguous({'workspace':{'digest':'same'}},{'workspace':{'digest':'same'}}),'adjacent evaluator checkpoints should remain auditable')
        a=root/'a.md';b=root/'b.md';c=root/'c.md';body='# Deliverable\n\nGeneric operational guidance for the target audience.\n'*12;a.write_text(body);b.write_text(body);c.write_text(body)
        flags=artifact_similarity_flags([{'event_id':'E1','kind':'workflow_acceptance','workflow_id':'one','actual_artifacts':[str(a)]},{'event_id':'E2','kind':'workflow_acceptance','workflow_id':'two','actual_artifacts':[str(b)]},{'event_id':'E3','kind':'workflow_acceptance','workflow_id':'three','actual_artifacts':[str(c)]}],max_examples=1);req(flags.get('E1'),'highly similar cross-job artifacts must still be surfaced for review')
        duplicate=exact_duplicate_artifact_flags([{'event_id':'E1','actual_artifacts':[str(a)]},{'event_id':'E2','actual_artifacts':[str(b)]}]);req(duplicate.get('E1') and duplicate.get('E2'),'byte-identical artifacts at distinct paths must remain an integrity failure signal')
        evolving=exact_duplicate_artifact_flags([{'event_id':'L1','actual_artifacts':[str(a)]},{'event_id':'L2','actual_artifacts':[str(a)]}]);req(not evolving,'the same durable artifact path reused across longitudinal events must not be misclassified as duplicate masquerading')
        scratch=ws/'scratch';scratch.mkdir();ordinary=scratch/'batch_work.py';ordinary.write_text("for event in events: print('complete real work')\n");ordinary_flags=run_control_flags(root,ws);req(not any(x.get('path')==str(ordinary) for x in ordinary_flags),'ordinary batch automation must not be treated as qualification manipulation')
        control_script=scratch/'qualification-control.py';control_script.write_text("for event in events:\n    print('evaluator/suite.json evaluator/queue.json')\n");control=run_control_flags(root,ws);req(any(x.get('type')=='candidate_evaluator_spec_access' and x.get('path')==str(control_script) for x in control),'candidate access to evaluator-private material must remain visible');req(any(x.get('type')=='mass_completion_runner' and x.get('path')==str(control_script) for x in control),'looping over multiple evaluator-private surfaces should remain an integrity signal')

    suite=build();tests=suite['workflow_tests'];universal={'workspace_valid','business_valid','material_result_observed','completion_claim_truthful'}
    req(tests,'qualification must cover authored Workflows')
    req(all(set(t['hard_gates'])==universal for t in tests),'atomic Workflow qualification must use one semantic-neutral deterministic floor')
    req(all(t['rubric_dimensions'] for t in tests),'every Workflow still needs capable professional review')
    req(all(t['candidate_task'] for t in tests),'every Workflow needs an ordinary business task')
    for retired in ('artifact_role','competitive_profile','output_policy','normally_used_workflows','authored_workflow_refs','unknown_workflow_refs'):
        req(all(retired not in t for t in tests),f'qualification cases retained retired semantic/composition field {retired}')
    req(all('capabilities' not in t and 'required_subcontracts' not in t for t in tests),'qualification cases retained retired capability/subcontract ontology')

    integrity=(ROOT/'qualification/integrity.py').read_text()
    for retired_phrase in ('contract-execution.json','required_subcontracts','record_contract_completion.py','structured_prepublish_refs','is_reconstructable_field_snapshot','reconstructable_field_snapshot_paths'):
        req(retired_phrase not in integrity,f'qualification integrity retained deleted execution or benchmark-shaped evidence machinery: {retired_phrase}')
    evaluator=(ROOT/'qualification/evaluate_run.py').read_text();
    for retired_phrase in ('output_policy','competitive_profile','artifact_role','competitive_field_evidence_reconstructable','actual_artifact_exists','expected_sop_process_steps'):
        req(retired_phrase not in evaluator,f'evaluator retained inferred semantic or retired SOP field: {retired_phrase}')
    req('Infer substantive requirements from the ordinary request' in evaluator,'evaluator must explicitly own semantic completeness judgment')
    critical=evaluator.split('critical_types=',1)[1].split(';critical_run_flags',1)[0];req("'mass_completion_runner'" not in critical,'bulk automation must not be an automatic failure when it performs real work');req('EVALUATOR-ERROR' in evaluator,'broken benchmark bookkeeping must be separated from candidate failure')
    controller=(ROOT/'qualification/task_controller.py').read_text();req('matching root AURA Run' not in controller and "'material_result_observed':material_result" in controller,'controller must classify observed business results rather than execution-ledger completion');req('target SOP' not in controller and 'SOP effectiveness' not in controller,'controller retained retired SOP framing');req('candidate_response_ref' in controller and 'canonical_refs or artifact_refs or response_ref' in controller,'controller must recognize useful work delivered directly in the candidate response without requiring a file artifact')
    judge=(ROOT/'qualification/build_judge_prompt.py').read_text().lower();req('do **not** require a particular aura run' in judge,'judge must not reward an AURA Run as universal proof');req('automation is acceptable' in judge,'judge must evaluate automated work by its real result');req('captured candidate-visible response' in judge and 'do not require file creation' in judge,'judge must evaluate conversational business output without manufacturing filesystem ceremony')
    runner=(ROOT/'qualification/run_candidate.py').read_text();req("env['BUSINESSOS_WORKSPACE']=str(run['workspace'])" in runner,'candidate runner must pin every AURA helper to the staged organization workspace');req('candidate-responses' in runner and 'stderr=subprocess.STDOUT' in runner,'candidate runner must preserve the user-visible command output for review');req("blocker_classification='external_capability'" in runner and 'Candidate-process failures are recorded above' in runner,'candidate runner must record harness execution failure without terminating a surrounding batch')
    judge_runner=(ROOT/'qualification/run_judge.py').read_text();req("PROMPT_TOKEN='{judge_prompt}'" in judge_runner and 'exactly this qualification run' in judge_runner,'judge runner must bind professional review to one explicit evaluator run');req('judgment event IDs do not match this run' in judge_runner and "set(actual)!=set(expected)" in judge_runner,'judge runner must reject stale or wrong-run judgments');req('candidate_surface_root' in judge_runner and 'review-packets-to-judge.json' in judge_runner,'judge runner must expose only the current run evidence surfaces needed for review')
    print('qualification real-work integrity regressions passed: deterministic honesty stays small; capable review owns task-specific completeness and quality')
if __name__=='__main__':main()
