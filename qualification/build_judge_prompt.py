#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from common import read_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('run_dir');ap.add_argument('--include-hard-failures',action='store_true',help='Also send deterministic hard-fail events to the quality judge for diagnostic scoring');a=ap.parse_args();rd=Path(a.run_dir).expanduser().resolve();packets=read_json(rd/'evaluator/review-packets.json')
    if packets is None:raise SystemExit('review-packets.json missing; run evaluate_run.py first')
    selected=packets if a.include_hard_failures else [p for p in packets if p.get('hard_pass') is True];packet_out=rd/'evaluator/review-packets-to-judge.json';packet_out.write_text(json.dumps(selected,indent=2,sort_keys=True)+'\n',encoding='utf-8');out=rd/'evaluator/JUDGE-INSTRUCTIONS.md';excluded=len(packets)-len(selected)
    out.write_text(f'''# Independent AURA Business-Quality Review

You are judging AURA's actual business work, not whether it recreated a preferred internal execution ledger. Review all {len(selected)} packets in `{packet_out}`.

{excluded} event(s) were excluded from this normal quality pass because they did not clear the deterministic business-work/integrity floor. Use `--include-hard-failures` only when diagnostic quality scoring is useful.

For each event:
1. Inspect the ordinary business task, expected SOP purpose/process, actual artifacts, cited evidence/source records, durable AURA changes, integrity warnings, and any optional method/work-receipt observations in `{rd/'evaluator/hard-and-merged-results.json'}`.
2. Determine whether the substantive business work was actually performed. A generic template, placeholder, outline, fake tool claim, short surrogate for a different promised medium, or bookkeeping-only file is not completion.
3. For a contract-acceptance event, treat the SOP process steps as the expected **business method and quality invariants**, not as a demand for exact internal files. Equivalent or better implementation may pass; skipping a material research/analysis/production/QA step should reduce `method_rigor`, completeness, and relevant outcome dimensions.
4. Do **not** require a particular Run ID, contract ID in a receipt, subcontract ledger, checkpoint-shaped artifact, provider, model, or tool-routing trace as proof of quality. Optional method provenance can help reconstruct what happened but is not the business result.
5. Automation is acceptable—even extensive automation—when it performs the real work. A mass runner is a warning only. Penalize it when it produced repeated generic artifacts, fabricated evidence, shallow boilerplate, false completion, or otherwise substituted machinery for the promised work.
6. QA must be substantive. Do not reward a self-attested “passed” file; inspect whether the actual target was checked, material issues were considered, corrections/limitations are credible, and the final deliverable reflects the review.
7. Where the task concerns a competitive field, inspect the event-specific current evidence as necessary: SERP/AI answers for SEO/AEO, ad transparency/creative centers and landing paths for marketing, visible performance/baselines for organic content, or the domain-appropriate alternatives. Several normal SourceRecords are valid evidence; do not require one synthetic benchmark-shaped “field snapshot.”
8. Score **every listed rubric dimension** from 0–5 using the packet scale. Do not reward mere artifact existence or schema compliance if the business work is shallow.
9. Treat **5 as rare**. A 5 means exceptional expert-level execution with no meaningful unsupported claim, material omission, unresolved contradiction, or competitive weakness in that dimension.
10. Distinguish relevance from proof. Do not call a company a top-ranking result, market leader, winning ad, profitable tactic, direct page read, or observed outcome unless the evidence establishes that claim.
11. A score of 3 means a competent professional could actually use the result without rebuilding the missing core work. If the promised medium or material method is absent, relevant dimensions should ordinarily be 0–2.
12. `state_integrity` means the organization can truthfully continue from what AURA persisted. Do not reward extra objects, Runs, receipts, or lifecycle ceremony that add no future organizational value.
13. Outcome-readiness means the work did what a strong practitioner could reasonably do now to maximize the intended result; it does not mean an unobserved ranking, citation, conversion, or profit already occurred.
14. Treat ad longevity, views, shares, engagement, and repeated creative families as proxies of differing strength unless direct outcome data exists. Reward explicit calibration of uncertainty.
15. For "better" work, judge fit to the intended audience/task and competitive environment; more words, more slides, or more detail are not automatically better.
16. For timed audio/video fallbacks, compare actual spoken-word volume/cues with claimed duration; timecode labels alone do not make a script long enough. A text fallback cannot truthfully claim nonexistent media was recorded, mixed, mastered, rendered, or exported.

Write a JSON array to `{rd/'evaluator/judgments.json'}`. Each item must be:

```json
{{
  "event_id":"...",
  "scores":{{"dimension_from_packet":4}},
  "notes":"Concise evidence-based justification, including important defects or competitive strengths."
}}
```

Write `judgments.json` as UTF-8. Do not modify AURA state or candidate artifacts while judging.
''',encoding='utf-8');print(json.dumps({'instructions':str(out),'packets':str(packet_out),'events_to_judge':len(selected),'hard_failures_excluded':excluded},indent=2))
if __name__=='__main__':main()
