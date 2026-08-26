#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from common import read_json


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('run_dir')
    ap.add_argument('--include-hard-failures',action='store_true',help='Also send deterministic hard-fail events to the quality judge for diagnostic scoring')
    a=ap.parse_args(); rd=Path(a.run_dir).expanduser().resolve()
    packets=read_json(rd/'evaluator/review-packets.json')
    if packets is None: raise SystemExit('review-packets.json missing; run evaluate_run.py first')

    if a.include_hard_failures:
        selected=packets
    else:
        selected=[p for p in packets if p.get('hard_pass') is True]

    packet_out=rd/'evaluator/review-packets-to-judge.json'
    packet_out.write_text(json.dumps(selected,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    out=rd/'evaluator/JUDGE-INSTRUCTIONS.md'
    excluded=len(packets)-len(selected)
    out.write_text(f'''# Independent AURA Business-Quality Review

You are judging AURA's actual business work, not grading how eloquently the candidate explained itself and not trusting a mechanical hard-pass as proof of quality. Review all {len(selected)} packets in `{packet_out}`.

{excluded} event(s) were excluded from this normal quality pass because they already failed deterministic hard gates; their final verdict remains FAIL without spending judge capacity on them. Use `--include-hard-failures` when building these instructions only if diagnostic quality scores for those failures are specifically needed.

For each event:
1. Inspect the packet's **actual contract process steps and completion-evidence requirement**, then inspect the actual artifacts, cited evidence/source records, candidate receipt, relevant before/after state diff, integrity flags, and Run/contract-execution records in `{rd/'evaluator/hard-and-merged-results.json'}`.
2. Determine whether the candidate actually performed the contract-specific business work. A generic template, placeholder, outline, short Markdown surrogate for a different promised medium, or a file whose main purpose is to satisfy qualification bookkeeping is not completion unless the contract explicitly promises that exact artifact.
3. Treat candidate-authored mass-runner/control scripts as a review warning, not automatic failure. Automation is acceptable only when it performs the real business work. Penalize any event where automation substituted generic artifacts, generic subcontract files, fabricated evidence, or self-attested completion for contract-specific execution.
4. QA must be substantive. A JSON file that merely says `status: passed` is not evidence that editorial/fact/accessibility/platform/brand/pre-publish checks were actually performed. Inspect the checks, tested Asset/version, blockers, evidence, and resulting corrections.
5. Where the packet concerns a competitive field, inspect the event-specific captured/current comparison field as necessary: current SERP/AI answers for SEO/AEO, ad transparency/creative centers and landing paths for marketing, visible performance/baselines for organic content, or the domain-appropriate alternative set. Reusing an unrelated earlier field snapshot is not current competitive research for a new event.
6. Score **every listed rubric dimension** from 0–5 using the score scale in the packet. Do not omit dimensions and do not reward mere artifact existence or schema/contract compliance if the business work is shallow.
7. A score of 3 means a competent professional could actually use the result without rebuilding the missing core work. If the promised medium or material contract steps are absent, relevant dimensions should ordinarily be 0–2 even if files/checkpoints/Runs exist.
8. Outcome-readiness means the work did what a strong practitioner could reasonably do now to maximize the intended business result; it does not mean an unobserved ranking, citation, conversion, or profit result already occurred.
9. Treat ad longevity, views, shares, engagement, and repeated creative families as proxies of differing strength unless direct outcome data exists. Reward explicit calibration of uncertainty.
10. For "better" work, judge fit to the intended audience/task and competitive environment; more words, more slides, or more detail are not automatically better.

Write a JSON array to `{rd/'evaluator/judgments.json'}`. Each item must be:

```json
{{
  "event_id":"...",
  "scores":{{"dimension_from_packet":4}},
  "notes":"Concise evidence-based justification, including important defects, qualification-shortcut evidence, or competitive strengths."
}}
```

Do not modify AURA state or candidate artifacts while judging.
''',encoding='utf-8')
    print(json.dumps({'instructions':str(out),'packets':str(packet_out),'events_to_judge':len(selected),'hard_failures_excluded':excluded},indent=2))

if __name__=='__main__': main()
