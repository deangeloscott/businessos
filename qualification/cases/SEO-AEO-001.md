# SEO-AEO-001 — Competitor Page Analysis

Status: **planned**  
Primary layers: **1 — atomic job quality** and **2 — competitive/field readiness**

## Purpose

Use a narrow, externally observable SEO/AEO job to test whether AURA helps a capable model/harness inspect the live search field, understand why a strong current page is useful/competitive, connect that evidence to AtlasOps, and preserve actionable gaps without unnecessary process ceremony.

Hidden target Workflow:

`seo.intelligence.organic-competition.page-analysis`

The candidate must not be told the target Workflow or shown this file.

## Ordinary business request

> For AtlasOps, analyze one strong current organic page you find for the intent “field service scheduling software for multi-location teams” as preparation for a new or materially differentiated AtlasOps asset. Explain why that page appears useful and competitive in the live search field, what users and search/AI-answer systems are getting from it, and what AtlasOps would need to provide to be more useful and differentiated. Use enough current evidence to establish the pattern, but stop when more research is unlikely to change the analysis. Persist the useful evidence and gaps in AURA. Do not invent rankings, traffic, or competitor performance you cannot verify.

The request defines the business problem while leaving the candidate free to choose legitimate sources, tools, research depth, comparison pages, delegation, and implementation method.

## Candidate environment

Use a capable model/harness with reasonable web/search access. Search/browser availability is an environment condition, not an AURA capability registry or product invariant. The active model/harness decides how to perform the research with the tools it actually has.

AURA should contribute current organizational context and relevant SEO/AEO operating knowledge while the candidate uses minimum-sufficient current research. It does not need to exhaust the web.

## Independent evaluator work

The evaluator should independently inspect the same general search/answer field:

- inspect the current result set for the defined intent or a clearly equivalent query;
- inspect a few strong current pages/results;
- verify that the candidate's selected reference is meaningful enough to learn from;
- note recurring expectations and meaningful differentiators;
- expand only if more evidence could materially change the judgment.

The evaluator is checking whether the candidate's investigation and conclusions were sufficient—not whether it reproduced the evaluator's source set or execution path.

## Success criteria

### Integrity

- required current external evidence was actually inspected;
- evidence/provenance is reconstructable;
- rankings, traffic, authority, tool use, and competitor performance are not invented;
- useful organizational evidence/gaps are persisted normally when doing so helps future work;
- no evaluator-specific files or fake completion artifacts are used to manufacture a pass.

### Method rigor

The material analytical work expressed by the Workflow is present even if the model/harness improves incidental implementation details or uses another equally sound method.

### Professional quality

A competent SEO/AEO practitioner could use the analysis without rebuilding the core investigation.

### Competitive readiness

The analysis explains meaningful mechanisms that make the selected page useful/competitive for the intended search/answer context, distinguishes expected patterns from material differences where relevant, and identifies actionable AtlasOps gaps/opportunities without copying expression or relying on superficial quotas.

## Diagnosis rule

If the result is weak, separate:

- AURA Workflow/operating-knowledge weakness;
- model capability;
- search/web availability;
- missing business context;
- execution error;
- fixture/evaluator limitation;
- normal model variability.

Only a reusable AURA weakness justifies a product change.

## Run sequence

```bash
python3 tests/run_all.py

python3 qualification/prepare_run.py \
  --profile atomic \
  --workflow seo.intelligence.organic-competition.page-analysis \
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

After independent judgment is saved, rerun evaluation and inspect the actual evidence yourself. If the qualification is meaningful and complete, append one minimal record to `qualification/ledger.jsonl`.
