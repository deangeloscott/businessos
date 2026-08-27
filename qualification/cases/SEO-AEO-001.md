# SEO-AEO-001 — Competitor Page Analysis

Status: **planned**  
Primary layers: **1 — atomic job quality** and **2 — competitive/field readiness**

## Why this is first

This is a narrow, externally observable SEO/AEO job with a clear real-world standard. It lets us verify that AURA can inspect the live search field, understand why a strong page is competitive, connect that evidence to the active business, and persist useful gaps without yet introducing the extra variables of full content production.

Target playbook (evaluator-side only):

`seo.intelligence.organic-competition.page-analysis`

The candidate must not be told the target contract or given this file.

## Candidate experience

Prepare the normal blind atomic run with the maintainer-authored ordinary request below. Give the candidate only the staged AURA product/workspace plus the request printed by `task_controller.py start`.

The candidate should have a capable model/harness and reasonable web/search access. The required contract capability is `search.serp.read`; general web reading and AI-answer observation are useful when available.

AURA should use minimum-sufficient current research. It does not need to exhaust the web. It should inspect enough of the live field to establish that the chosen page is a meaningful strong reference, understand the relevant intent and competitive pattern, and identify material gaps for AtlasOps; it should expand only if more evidence could materially change the analysis.

## Ordinary business request

> For AtlasOps, analyze one strong current organic page you find for the intent “field service scheduling software for multi-location teams” as preparation for a new or materially differentiated AtlasOps asset. Explain why that page appears useful and competitive in the live search field, what users and search/AI-answer systems are getting from it, and what AtlasOps would need to provide to be more useful and differentiated. Use enough current evidence to establish the pattern, but stop when more research is unlikely to change the analysis. Persist the useful evidence and gaps in AURA. Do not invent rankings, traffic, or competitor performance you cannot verify.

This task is deliberately specific enough to define the intent while still leaving AURA free to choose its sources, research depth, comparison page, and analysis method.

## Evaluator investigation

Independently inspect the same general search/answer field without copying AURA's research path.

Start small:
- inspect the current result set for the defined intent or a clearly equivalent query formulation;
- inspect a few strong current results/pages;
- verify that AURA's selected reference is genuinely relevant/strong enough to learn from;
- note recurring expectations and meaningful differentiators;
- inspect additional results only if the field remains ambiguous or another sample could materially change the judgment.

The evaluator is checking whether AURA's evidence set and conclusions were sufficient—not whether AURA found the evaluator's exact sources.

## What counts as success

### Integrity
- current external evidence was actually inspected where required;
- sources/provenance are reconstructable;
- AURA does not invent rankings, traffic, authority, tool use, or competitor facts;
- useful results are persisted through normal AURA state/Run mechanics.

### Professional quality
A competent SEO/AEO practitioner could use the analysis without rebuilding the core investigation.

### Competitive readiness
The analysis correctly explains important mechanisms that make the selected strong current page useful/competitive for the intended search/answer context, distinguishes expected/common patterns from meaningful differences where relevant, and identifies material gaps/opportunities for AtlasOps without copying expression or relying on superficial word counts.

## Minimal external comparison

Do not run a tournament. The evaluator should normally need only a few strong references to establish the field.

If there is a directly comparable analysis or recommendation artifact, use at most a small blind pairwise check when it adds signal. Pairwise comparison is optional for this intelligence job; it becomes more useful in the later content-production composition.

## Diagnosis rule

If the result is weak, classify the cause before changing AURA:
- AURA process/method;
- model capability;
- search/web capability;
- missing business context;
- execution error;
- fixture limitation;
- evaluator error;
- normal model variability.

Only a reusable AURA weakness justifies a product change.

## Next composition after this passes

Use the intelligence to test:

`seo.planning.organic-content-requirements`

then route the resulting WorkRequest into Content Synthesis to create an actual SEO/AEO-oriented asset. That larger run should test whether the competitive research truly influences the content requirements and finished artifact, then use minimal blind comparison against strong current pages for the same audience/intent.

## Run sequence

```bash
python3 tests/run_all.py

python3 qualification/prepare_run.py \
  --profile atomic \
  --contract seo.intelligence.organic-competition.page-analysis \
  --request 'For AtlasOps, analyze one strong current organic page you find for the intent “field service scheduling software for multi-location teams” as preparation for a new or materially differentiated AtlasOps asset. Explain why that page appears useful and competitive in the live search field, what users and search/AI-answer systems are getting from it, and what AtlasOps would need to provide to be more useful and differentiated. Use enough current evidence to establish the pattern, but stop when more research is unlikely to change the analysis. Persist the useful evidence and gaps in AURA. Do not invent rankings, traffic, or competitor performance you cannot verify.'

python3 qualification/task_controller.py start /path/to/run
```

Give the candidate only the printed product path, workspace path, and `candidate_message`.

After the candidate finishes:

```bash
python3 qualification/task_controller.py finish /path/to/run
python3 qualification/evaluate_run.py /path/to/run
python3 qualification/build_judge_prompt.py /path/to/run
```

After independent judgment is saved, rerun evaluation and inspect the actual evidence/artifact yourself.

If the qualification is meaningful and complete, append one minimal record to `qualification/ledger.jsonl`.
