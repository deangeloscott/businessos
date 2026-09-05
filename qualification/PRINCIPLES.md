# AURA Qualification Principles

This is the durable qualification doctrine for ViralTrac AURA.

## North star

> **When a normal user gives AURA real business work, does AURA help the model/harness/user perform the real work, use appropriate evidence and available capabilities, produce a professionally useful result, and preserve useful organizational meaning without constraining the executing intelligence?**

Qualification is maintainer tooling. It observes AURA; AURA does not optimize itself for the benchmark.

## Three distinct verification surfaces

Keep these separate:

1. **AURA product integrity** — deterministic checks for things AURA itself owns: schemas, references, organization isolation, retrieval/state semantics, truth boundaries, packaging, and other architectural invariants. Run with `python3 tests/run_all.py`.
2. **Qualification-harness integrity** — maintainer-only checks that realistic cases, blind isolation, checkpoints, recovery, scoring inputs, candidate-result observation, and staged-product protection are trustworthy. Run with `python3 qualification/self_test.py`. These checks do not count as AURA product tests.
3. **Real-work qualification** — give a capable model/harness an ordinary business task with AURA and judge the actual business result. This is the evidence that AURA is useful.

Do not collapse these into one score or one release-test count.

## Protected invariants

1. **Test normal use, not test-taking.** The candidate receives a normal AURA product/workspace, its real model/harness capabilities, and an ordinary business request. Hidden targets, judge guidance, rubrics, checkpoints, evaluator observations, and scoring stay evaluator-side.
2. **AURA must cooperate with intelligence, not constrain it.** Qualification must not reward AURA for limiting model/harness reasoning, tools, delegation, concurrency, planning, or judgment. Equivalent or improved implementation is allowed when essential business work remains rigorous and truthful.
3. **Test real work, not internal ceremony.** No particular internal execution record, receipt, checkpoint-shaped artifact, or method trace is universal proof of success. Material results, real evidence, truthful durable state, and actual deliverables matter.
4. **A selected AURA Workflow still has substance.** When a specific Workflow is deliberately isolated for diagnosis, the reviewer should judge whether its essential business method and quality invariants were actually satisfied. Do this through professional review, not an execution graph.
5. **Use minimum-sufficient evidence.** Start with a credible evidence set and expand only when more investigation could materially change the result, confidence, or competitive judgment.
6. **Deterministic gates protect universal integrity, not task semantics or taste.** They may verify evaluator integrity, valid AURA/workspace state, whether a material result was actually observed, truthful completion, and other facts that are safe to decide mechanically. They must not infer from Workflow names that a particular artifact, source count, field-research shape, word count, slide count, magic phrase, or benchmark-specific file is mandatory.
7. **Professional quality and task-specific completeness are judged externally.** A human or independent capable model judges accuracy, evidence, method rigor, usefulness, craft, business alignment, outcome readiness, and whether the actual job required an artifact, current research, implementation, QA, measurement, or another material step.
8. **Automation is allowed.** A model/harness may automate, delegate, parallelize, or otherwise use its capabilities. Automation fails only when it substitutes generic/fabricated work for the real job or violates another real integrity requirement.
9. **A truthful blocker beats fabricated completion.** Real external capability, permission/scope, data, or service limits should be recorded evaluator-side. AURA should not invent an internal Approval/authority system to represent them.
10. **Outcome readiness is not an observed outcome.** Rankings, citations, leads, conversion, revenue, retention, and similar results require later real-world evidence.
11. **Bad output triggers diagnosis, not automatic product rules.** Separate AURA weaknesses from model, harness, context, fixture, evaluator, execution, and random-variance failures.
12. **A benchmark rule belongs in AURA only when it improves ordinary customer work.** Otherwise it stays evaluator-side or is removed.
13. **Do not test the host as if it were AURA.** Generic abilities such as opening/decoding files, browsing, calling APIs, rendering media, running code, choosing tools, using subagents, or scheduling belong to the active model/harness/environment.

## Qualification shape

Keep the qualification surface small.

### Real-world use cases

This is the primary proof. Use a compact but broad library of realistic business jobs. A case may exercise one Workflow, many Workflows, multiple operating areas, or several sessions over time. Hidden coverage metadata describes what we think the case exercises; it never becomes an execution requirement.

### Focused Workflow diagnostics

When actual evidence points to one specific body of operating knowledge, isolate that Workflow with an explicit benchmark organization and an ordinary request. This is a debugging microscope, not a release requirement to execute every Workflow individually.

### Repetition and field outcomes

Repeat important cases only when needed to distinguish model variance from systematic weakness. Where authorized real-world work exists, later field outcomes are the strongest evidence and should be preserved with causal uncertainty intact.

There is no separate generated all-Workflow suite, mission taxonomy, profile hierarchy, or mandatory composition benchmark. If a realistic case already tests the meaningful business outcome, qualification should not recreate the same test under another abstraction.

## Integrity floor

The deterministic qualification floor should stay narrow and universal. Typical valid checks include:

- evaluator bookkeeping is intact enough to trust the comparison;
- the AURA workspace/business remains structurally valid;
- claimed completion corresponds to an observed material result;
- completion is not claimed when no material result was observed;
- exact duplicate artifact reuse is surfaced when it could masquerade as distinct completed work;
- the candidate did not access hidden evaluator material or mutate the staged product.

Whether a particular task needed a finished deliverable, current external evidence, rendered QA, implementation, a larger sample, or a specific kind of provenance is a **semantic quality judgment** made from the ordinary request, relevant Workflow expertise, business context, actual result, and professional standards.

Missing evaluator bookkeeping is an **evaluator error**, not evidence that AURA failed.

## Method rigor

For an AURA Workflow under focused diagnosis, distinguish:

- **essential invariant** — necessary business work/quality requirement;
- **useful default** — normally helpful but adaptable;
- **incidental implementation** — tool/order/delegation detail the model/harness may improve;
- **artificial ceremony** — remove from both qualification and, where applicable, AURA.

The reviewer should penalize skipped essential work, not intelligent adaptation.

## Competitive / field evaluation

Use external comparison only where it helps answer whether the work is strong enough for the intended field.

Start small. A few strong current references are often enough. Expand when the field is ambiguous, sources materially disagree, stakes are higher, or another sample could change the judgment.

Do not require AURA to use the evaluator's exact sources or method. Compare the sufficiency and correctness of the resulting evidence and work.

Visible proxies such as ad longevity, views, shares, engagement, or repeated creative families can be meaningful visibility, attention, distribution, or persistence signals when those outcomes matter. They are not automatically direct proof of profitability, conversion, retention, or causal effectiveness without evidence that supports those stronger conclusions.

## Diagnosis before product change

Before modifying AURA because of a qualification failure, answer:

1. What real customer-facing weakness occurred?
2. Is it attributable to AURA rather than model/harness capability, missing context, execution error, randomness, fixture design, or evaluator error?
3. What first-principles AURA responsibility would improve by changing the product—organizational memory, operating knowledge, continuity, truth, measurement, Learning, retrieval, or integrity?
4. Could the proposed fix constrain intelligence, duplicate runtime responsibility, create bureaucracy, or optimize for the benchmark instead of the user?
5. What fresh real-work run would demonstrate improvement?

If those questions do not support the change, do not add the mechanism.

## Minimal qualification evidence

Keep `qualification/ledger.jsonl` deliberately small. Preserve enough to know what was tested, AURA version, model/harness and important capabilities, integrity/quality verdicts, evidence location, meaningful limitations, and later real-world outcomes where available.

Community/customer reports are evidence with provenance and scope. Repeated strong evidence may justify Learning or Workflow evolution; one organization's result must never silently become universal truth.

## Final invariant

> **Qualification should make us confident that AURA helps capable intelligence produce excellent real business work. It must never make AURA less capable, less portable, more bureaucratic, or more hostile to the model/harness/user in order to make scoring easier.**
