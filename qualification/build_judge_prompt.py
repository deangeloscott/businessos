#!/usr/bin/env python3
from pathlib import Path
import argparse
from common import read_json

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('run_dir'); a=ap.parse_args(); rd=Path(a.run_dir).expanduser().resolve()
    packets=read_json(rd/'evaluator/review-packets.json')
    if packets is None: raise SystemExit('review-packets.json missing; run evaluate_run.py first')
    out=rd/'evaluator/JUDGE-INSTRUCTIONS.md'
    out.write_text(f'''# Independent AURA Business-Quality Review

You are judging AURA's actual business work, not grading how eloquently the candidate explained itself. Review all {len(packets)} packets in `{rd/'evaluator/review-packets.json'}`.

For each event:
1. Inspect the packet, actual artifacts, cited evidence/source records, candidate receipt, relevant before/after state diff and Run/contract-execution records in `{rd/'evaluator/hard-and-merged-results.json'}`.
2. Where the packet concerns a competitive field, inspect the captured/current comparison field as necessary: current SERP/AI answers for SEO/AEO, ad transparency/creative centers and landing paths for marketing, visible performance/baselines for organic content, or the domain-appropriate alternative set.
3. Score **every listed rubric dimension** from 0–5 using the score scale in the packet. Do not omit dimensions and do not reward mere artifact existence or contract compliance if the work is shallow.
4. Outcome-readiness means the work did what a strong practitioner could reasonably do now to maximize the intended business result; it does not mean an unobserved ranking, citation, conversion, or profit result already occurred.
5. Treat ad longevity, views, shares, engagement, and repeated creative families as proxies of differing strength unless direct outcome data exists. Reward explicit calibration of uncertainty.
6. For "better" work, judge fit to the intended audience/task and competitive environment; more words, more slides, or more detail are not automatically better.

Write a JSON array to `{rd/'evaluator/judgments.json'}`. Each item must be:

```json
{{
  "event_id":"...",
  "scores":{{"dimension_from_packet":4}},
  "notes":"Concise evidence-based justification, including important defects or competitive strengths."
}}
```

Do not modify AURA state or candidate artifacts while judging.
''',encoding='utf-8')
    print(out)
if __name__=='__main__': main()
