# AURA Qualification Principles

This is the durable qualification doctrine for ViralTrac AURA.

## North star

> **When a normal user gives AURA real business work, does AURA help the model/harness/user perform the real work, use appropriate evidence and available capabilities, produce a professionally useful result, and preserve useful organizational meaning without constraining the executing intelligence?**

Qualification is maintainer tooling. It observes AURA; AURA does not optimize itself for the benchmark.

## Three distinct verification surfaces

Keep these separate:

1. **AURA product integrity** — deterministic checks for things AURA itself owns: schemas, references, business isolation, retrieval/state semantics, truth boundaries, packaging, and other architectural invariants. Run with `python3 tests/run_all.py`.
2. **Qualification-harness integrity** — maintainer-only checks that the blind evaluator, checkpoints, recovery, scoring inputs, and staged-product observation are trustworthy. Run with `python3 qualification/self_test.py`. These checks do not count as AURA product tests.
3. **Real-work qualification** — give a capable model/harness an ordinary business task with AURA and judge the actual business result. This is the evidence that AURA is useful.

Do not collapse these into one score or one release-test count.

## Protected invariants

1. **Test normal use, not test-taking.** The candidate receives a normal AURA product/workspace, its real model/harness capabilities, and an ordinary business request. Hidden targets, rubrics, checkpoints, receipts, evaluator research, and scoring stay evaluator-side.
2. **AURA must cooperate with intelligence, not constrain it.** Qualification must not reward AURA for limiting model/harness reasoning, tools, delegation, concurrency, planning, or judgment. Equivalent or improved implementation is allowed when essential business work remains rigorous and truthful.
3. **Test real work, not internal ceremony.** A particular Run, contract-execution ledger, subcontract file, controller receipt, or evaluator-shaped artifact is never universal proof of success. Material results, real evidence, truthful durable state, and actual deliverables matter.
4. **A selected AURA SOP still has substance.** For playbook qualification, the reviewer should judge whether the essential method/quality invariants were actually satisfied. Do this through `method_rigor` and the real work—not by demanding an exact execution graph.
5. **Use minimum-sufficient evidence.** Start with a credible evidence set and expand only when more investigation could materially change the result, confidence, or competitive judgment.
6. **Deterministic gates protect integrity, not taste.** They may verify real evidence, reconstructable provenance, valid state, truthful completion, event-specific artifacts, and supported claims. They must not encode excellence as word counts, slide counts, magic phrases, arbitrary file quotas, or benchmark-shaped passwords.
7. **Professional quality is judged externally.** A human or independent capable model judges accuracy, evidence, method rigor, usefulness, craft, business alignment, and outcome readiness. Current-field comparison is used only when it materially improves the judgment.
8. **Automation is allowed.** A model/harness may automate, delegate, parallelize, or otherwise use its capabilities. Automation fails only when it substitutes generic/fabricated work for the real job or violates another real integrity requirement.
9. **A truthful blocker beats fabricated completion.** Real external capability, permission/scope, data, or service limits should be recorded evaluator-side. AURA should not invent an internal Approval/authority system to represent them.
10. **Outcome readiness is not an observed outcome.** Rankings, citations, leads, conversion, revenue, retention, and similar results require later real-world evidence.
11. **Bad output triggers diagnosis, not automatic product rules.** Separate AURA weaknesses from model, harness, context, fixture, evaluator, execution, and random-variance failures.
12. **A benchmark rule belongs in AURA only when it improves ordinary customer work.** Otherwise it stays evaluator-side or is removed.
13. **Do not test the host as if it were AURA.** Generic abilities such as opening/decoding files, browsing, calling APIs, rendering media, running code, choosing tools, using subagents, or scheduling belong to the active model/harness/environment. Qualification may treat those capabilities as environmental conditions and judge the business result AURA helped produce, but it must not turn generic host competence into an AURA product invariant.

## Integrity floor

The deterministic qualification floor should stay narrow. Typical valid checks include:

- evaluator bookkeeping is intact enough to trust the comparison;
- the AURA workspace/business remains structurally valid;
- claimed completion corresponds to an observed material result;
- a promised deliverable actually exists and is event-specific;
- current-field work has reconstructable current evidence when current external reality matters;
- customer-facing claims/state remain truthful;
- exact duplicate reuse does not masquerade as distinct completed jobs;
- the candidate did not access hidden evaluator material or mutate the staged product.

Missing evaluator bookkeeping is an **evaluator error**, not evidence that AURA failed.

## Method rigor

For an AURA SOP under test, distinguish:

- **essential invariant** — necessary business work/quality requirement;
- **useful default** — normally helpful but adaptable;
- **incidental implementation** — tool/order/delegation detail the model/harness may improve;
- **artificial ceremony** — remove from both qualification and, where applicable, AURA.

The reviewer should penalize skipped essential work, not intelligent adaptation.

## Competitive / field evaluation

Use external comparison only where it helps answer whether the work is strong enough for the intended field.

Start small. A few strong current references are often enough. Expand when the field is ambiguous, sources materially disagree, stakes are higher, or another sample could change the judgment.

Do not require AURA to use the evaluator's exact sources or method. Compare the sufficiency and correctness of the resulting evidence and work.

Visible proxies such as ad longevity, views, shares, engagement, or repeated creative families are signals—not direct proof of profitability or business outcomes unless first-party evidence establishes that.

## Layered real-work qualification

### Layer 0 — AURA product integrity
Schemas, references, business isolation, persistence, routing/selection, migrations, packaging, and other deterministic AURA invariants. This is the separate `tests/run_all.py` product gate, not a model/harness benchmark.

### Layer 1 — Atomic job quality
One meaningful job from an ordinary request. Inspect the actual result.

### Layer 2 — Competitive / field readiness
Where relevant, independently compare against enough strong current alternatives to judge whether the work is competitive.

### Layer 3 — Composition quality
Test whether multiple jobs/SOPs and organizational memory compound into one coherent result rather than disconnected fragments.

### Layer 4 — Medium-specific outcome quality
When a business job naturally calls for a particular medium or artifact, judge whether the AURA-assisted result is useful and appropriate for that medium. Do **not** benchmark generic host abilities such as parsing a PDF, decoding an image, rendering a video, or using a particular tool. If a required host capability is genuinely unavailable, record the external limitation truthfully rather than scoring AURA as though it owned that capability.

### Layer 5 — Domain and cross-domain missions
Test larger outcome-oriented problems, evidence reuse, prioritization, coordination, persistence, and judgment.

### Layer 6 — Reliability
Repeat important workflows across runs and, where meaningful, capable models/harnesses. Do not multiply every test across everything by default.

### Layer 7 — Observed real-world outcomes
Use authorized real organizations/work to measure what happened later while preserving causal uncertainty.

## Diagnosis before product change

Before modifying AURA because of a qualification failure, answer:

1. What real customer-facing weakness occurred?
2. Is it attributable to AURA rather than model/harness capability, missing context, execution error, randomness, fixture design, or evaluator error?
3. What first-principles AURA responsibility would improve by changing the product—organizational memory, operational knowledge, continuity, truth, measurement, Learning, retrieval, or integrity?
4. Could the proposed fix constrain intelligence, duplicate runtime responsibility, create bureaucracy, or optimize for the benchmark instead of the user?
5. What fresh real-work run would demonstrate improvement?

If those questions do not support the change, do not add the mechanism.

## Minimal qualification evidence

Keep `qualification/ledger.jsonl` deliberately small. Preserve enough to know what was tested, AURA version, model/harness and important capabilities, integrity/quality verdicts, evidence location, meaningful limitations, and later real-world outcomes where available.

Community/customer reports are evidence with provenance and scope. Repeated strong evidence may justify Learning or SOP evolution; one organization's result must never silently become universal truth.

## Final invariant

> **Qualification should make us confident that AURA helps capable intelligence produce excellent real business work. It must never make AURA less capable, less portable, more bureaucratic, or more hostile to the model/harness/user in order to make scoring easier.**
