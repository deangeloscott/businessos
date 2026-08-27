# AURA Qualification Principles

This document is the durable north star for qualifying ViralTrac AURA.

Qualification exists to answer one practical question:

> **When a normal user gives AURA real business work, does AURA do the real work, use the right evidence and capabilities, produce a professionally useful result, and—where the field is observable—produce work that is genuinely competitive with strong current alternatives?**

Qualification is maintainer tooling. It must observe normal AURA behavior, not become the objective AURA optimizes for.

## Protected rules

1. **The candidate does not see the test.** The candidate receives a normal staged AURA product, relevant organization workspace, available tools/capabilities, and an ordinary business request. Target contracts, rubrics, scoring, checkpoints, receipts, event IDs, benchmark metadata, evaluator research, and comparison sets remain outside the candidate environment.
2. **Test real business work, not benchmark compliance.** Research should inspect real evidence when required. Production should create the actual usable deliverable when the environment can do so. Technical checks should run actual tools when claimed. QA should inspect a real target. A truthful production specification is a fallback, not a finished artifact.
3. **Use minimum-sufficient research, not exhaustive-by-default research.** Start with the smallest credible evidence set that can support an excellent result. Expand when additional investigation has a reasonable chance of materially changing the output, recommendation, confidence, or competitive judgment. Stop when further research is unlikely to matter.
4. **Deterministic gates protect integrity, not taste.** They may verify that evidence exists, sources resolve, claimed tools really ran, the promised medium is truthful, state is valid, provenance is reconstructable, and completion claims are supported. They must not encode excellence as arbitrary word counts, slide counts, duration targets, magic phrases, or benchmark-shaped output passwords.
5. **Professional quality is judged externally.** A human or independent capable model reviews the actual work for accuracy, specificity, usefulness, craft, business alignment, and outcome readiness. Where current market performance is observable, the evaluator independently samples enough of the current field to establish a credible benchmark.
6. **AURA and the evaluator investigate independently.** Their evidence may overlap, but AURA is not required to reproduce the evaluator's exact source set. The evaluator asks whether AURA's investigation was sufficient and whether its conclusions and output stand up against independently observed reality.
7. **Bad output triggers diagnosis, not automatically a new product rule.** Determine whether the weakness came from AURA methodology, model capability, tool/capability availability, missing business context, execution error, randomness, fixture design, or evaluator error. Change AURA only when the failure reveals a reusable real-world AURA weakness.
8. **A qualification requirement belongs in AURA only if it improves normal customer work.** If a rule mainly makes scoring easier, it stays in maintainer-side qualification or is removed.
9. **Do not overfit one artifact.** Improve the underlying business method, evidence use, capability routing, production specification, or quality standard. Do not convert one disappointing output into a universal format quota.
10. **Outcome readiness is not an observed outcome.** Competitive/readiness qualification may establish that work is professionally strong and plausibly suited to the intended result. Rankings, citations, leads, conversion, revenue, retention, or other outcomes require later real-world evidence.

## Layered qualification model

Use the smallest layer that answers the current question. Progress upward only after lower layers are understood.

### Layer 0 — Software integrity

Prove AURA's deterministic mechanics and operating invariants are intact: distribution, schemas, routing, state, provenance, completion integrity, authorization boundaries, migrations, recovery, and related regressions.

Primary gate: `python3 tests/run_all.py`.

### Layer 1 — Atomic job quality

Run one meaningful playbook/job blind from an ordinary business request. Inspect the actual result. Prove that the individual job is genuinely executable and professionally useful.

### Layer 2 — Competitive / field readiness

When the task depends on a current external field, independently inspect enough strong current alternatives to judge whether AURA understood the field and produced work that is competitive for the intended outcome.

Examples:
- SEO/AEO: current SERPs, leading pages, answer/citation surfaces where observable;
- advertising: transparency libraries, persistent creatives, landing paths, offer/message patterns;
- organic content: visible performance proxies, format/context normalization, recurring mechanisms;
- customer/industry intelligence: evidence quality, source breadth, contradiction handling, decision usefulness.

The evaluator should not require AURA to use the same sources or identical method if AURA reached a well-supported, competitive result through another legitimate path.

### Layer 3 — Composition quality

Test a larger business request that requires multiple playbooks/jobs. Verify that research and state actually compound: upstream evidence informs strategy, strategy informs production, QA inspects the produced target, useful context is reused, semantic ownership remains clean, and the user receives one coherent result rather than disconnected task fragments.

### Layer 4 — Capability and media execution

Test whether AURA uses the capabilities available in the host environment to actually perform the work.

Preferred order:
1. create/run the real thing when the current environment can;
2. use an already-authorized compatible capability when appropriate;
3. when final rendering/execution is genuinely unavailable, produce a portable production specification that another tool, model, agent, or person can execute accurately.

A portable production specification should preserve the intent needed to recreate the deliverable: objective, audience, message, source facts, structure/composition, brand constraints, required content/media, dimensions/format where relevant, exclusions, acceptance criteria, and any other material requirements. Tool-specific prompts/instructions may be saved as execution provenance, but the durable source of truth should remain provider/tool agnostic.

Never call a storyboard a video, a script mastered audio, a Markdown outline a rendered presentation, or a proposed technical check an executed audit.

### Layer 5 — Domain and cross-domain missions

Give AURA larger outcome-oriented problems and judge routing, prioritization, evidence reuse, planning, cross-domain coordination, execution, QA, persistence, measurement design, and judgment about when to stop or ask for help.

### Layer 6 — Reliability

Repeat important workflows enough to distinguish a robust capability from a lucky run. Use multiple runs and, where material, more than one capable model/harness. Do not multiply every contract across every model by default. Sampling depth should reflect risk, importance, variability, and what decision the test needs to support.

### Layer 7 — Observed real-world outcomes

Use real organizations and authorized live work to measure what happened after deployment or publication. Preserve causal uncertainty. Community/customer evidence can strengthen AURA's evidence base and support case studies, but one organization's result must not silently become a universal rule.

## Competitive evaluation: keep it small and useful

Use external comparison only when it helps answer whether the work is competitive.

- Sample a small number of strong current references first—often 2–3 is enough for an artifact comparison, while some SEO/AEO tasks may reasonably inspect several leading results to understand intent and recurring patterns.
- Expand only when the field is ambiguous, results materially disagree, risk is higher, or another sample could change the judgment.
- Prefer blind or source-masked pairwise comparison for customer-facing artifacts when practical: compare AURA's artifact against a strong reference for the same audience/objective without telling the judge which is AURA's.
- Do not turn pairwise judging into a tournament or mandatory step for jobs where it adds little value.

## Minimal qualification ledger

`qualification/ledger.jsonl` is the append-only longitudinal record of meaningful completed qualification runs. Keep it deliberately small.

A record should contain only what is needed to answer: what was tested, on what AURA version, with what environment, how it performed, where the evidence is, and whether later field outcomes exist.

Recommended fields:

```json
{
  "date": "YYYY-MM-DD",
  "aura_version": "1.8.4",
  "playbook_or_mission": "seo.intelligence.organic-competition.page-analysis",
  "layer": 2,
  "scenario": "AtlasOps",
  "model_harness": "<model / harness>",
  "important_capabilities": ["search.serp.read", "research.web.read"],
  "integrity_verdict": "PASS",
  "quality_verdict": "COMPETITIVE",
  "competitive_result": "optional short result",
  "evidence_location": "<run/report/artifact path>",
  "known_limitations": ["optional limitation"],
  "observed_outcome": null
}
```

Do not add fields merely because they could be measured. Add them only when repeated qualification decisions genuinely need them.

## Community and field evidence

Community contributions may include:
- process improvements;
- stronger Skills/templates/prompts/tool integrations;
- execution examples;
- measured field outcomes;
- failure reports and limitations.

Treat contributions as evidence with provenance and scope. Promote Learning only as broadly as the evidence supports. High-quality repeated evidence may justify AURA updates, public case studies, qualification claims, or recommended process extensions; it does not automatically rewrite universal AURA behavior.

## Claims qualification may support

Use narrow truthful language tied to evidence, for example:

> "This workflow has been qualification-tested for professional readiness."

or, when independently benchmarked:

> "This workflow has been qualification-tested for competitive readiness."

If useful, include supporting details such as AURA version, number of runs, environments/models tested, benchmark method, known limitations, or field case studies. Do not imply observed business outcomes that have not occurred.

## Change-control rule

Before changing qualification or changing AURA because of a qualification result, read this document.

A proposed change should answer:

1. What real-world business weakness did the test expose?
2. Why is the weakness attributable to AURA rather than the model, tools, missing context, fixture, randomness, or evaluator?
3. How does the proposed change improve normal customer work?
4. Could the fix instead create benchmark-shaped behavior, arbitrary output constraints, exhaustive research, or duplicated bureaucracy?
5. What fresh run will show that the underlying business result improved?

Changing these principles should be explicit and rare. The justification must explain why the change improves real-world AURA operation—not merely why it makes qualification easier to score.
