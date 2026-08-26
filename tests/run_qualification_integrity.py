#!/usr/bin/env python3
from pathlib import Path
import json, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'qualification'))
from integrity import (
    artifact_similarity_flags, event_specific_ref_paths, is_structured_prepublish_record,
    run_control_flags, selector_types,
)
from build_suite import build


def req(cond,msg):
    if not cond: raise AssertionError(msg)


def main():
    req(selector_types(['Asset',{'type':'Observation'},{'object_type':'Learning'}])=={'Asset','Observation','Learning'},'write selector normalization failed')

    with tempfile.TemporaryDirectory(prefix='aura-qualification-integrity-') as td:
        root=Path(td); ws=root/'workspace'; ws.mkdir(); p=ws/'attachments'/'field.json'; p.parent.mkdir(parents=True); p.write_text('new evidence\n')
        before={'workspace':{'files':[]}}
        after={'workspace':{'files':[{'path':'attachments/field.json','sha256':'abc'}]}}
        req(event_specific_ref_paths(['attachments/field.json'],before,after,ws),'new event field snapshot must be recognized')
        same_before={'workspace':{'files':[{'path':'attachments/field.json','sha256':'abc'}]}}
        req(not event_specific_ref_paths(['attachments/field.json'],same_before,after,ws),'unchanged recycled field snapshot must not count as event-specific evidence')

        bad=root/'bad-qa.json'; bad.write_text(json.dumps({'contract_id':'content.qa.pre-publish','status':'passed','notes':'QA passed'}))
        req(not is_structured_prepublish_record(bad),'self-attested QA must not pass structural pre-publish evidence check')
        good=root/'good-qa.json'; good.write_text(json.dumps({'contract_id':'content.qa.pre-publish','status':'pass','checks_performed':[{'check':'links','passed':True}],'blockers':[],'tested_asset':'ast_1','tested_version':'1.0'}))
        req(is_structured_prepublish_record(good),'structured pre-publish evidence should pass')

        a=root/'a.md'; b=root/'b.md'
        a.write_text('# Deliverable\n\n## Context\nGeneric operational guidance for the target audience.\n\n## Steps\n1. Review the workflow.\n2. Apply the process.\n3. Validate the result.\n'*5)
        b.write_text('# Deliverable\n\n## Context\nGeneric operational guidance for the target audience.\n\n## Steps\n1. Review the workflow.\n2. Apply the process.\n3. Validate the result.\n'*5)
        results=[{'event_id':'E1','kind':'contract_acceptance','contract_id':'content.production.article','actual_artifacts':[str(a)]},{'event_id':'E2','kind':'contract_acceptance','contract_id':'content.production.animation','actual_artifacts':[str(b)]}]
        flags=artifact_similarity_flags(results)
        req('E1' in flags and 'E2' in flags,'highly similar artifacts across distinct contracts must be flagged')

        runner=root/'run_remaining_queue.py'; runner.write_text('print("mass runner")\n')
        req(run_control_flags(root),'candidate-authored run control script must be surfaced as integrity warning')

    suite=build(); customer=[t for t in suite['contract_tests'] if t.get('artifact_role')=='customer_facing_production_root']
    req(customer and all('prepublish_or_required_qa_recorded' in t['hard_gates'] for t in customer),'customer-facing roots must require structured QA evidence')
    competitive=[t for t in suite['contract_tests'] if t.get('competitive_profile') in {'search_live_field','paid_and_persuasion_field','organic_attention_field'}]
    req(competitive and all('competitive_field_evidence_event_specific' in t['hard_gates'] for t in competitive),'competitive tests must require event-specific field evidence')
    req(all('generic' in t['candidate_task'].lower() or not t['output_policy'].get('artifact_required') for t in suite['contract_tests']),'artifact tasks must explicitly reject generic substitutes')

    print('qualification adversarial integrity regressions passed')

if __name__=='__main__': main()
