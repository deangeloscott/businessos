# Decision Grounding & Inference Policy

Use this policy whenever a Workflow creates or materially updates an `Opportunity` or another canonical decision object.

## Core rule
A verified fact does **not** automatically verify every consequence inferred from that fact. Preserve the boundary between:
- established business/context facts;
- direct observations and measured outcomes;
- derived causal/strategic inference;
- unknown or unmeasured state.

An Opportunity may recommend action under uncertainty, but it should not present unsupported inference as established business, economic, search-performance, customer, or AI-answer truth.

This is semantic guidance for the capable model/user, not a deterministic prose rules engine. Structural validation may verify that references exist and that objects labeled as measured evidence are appropriate evidence types; it should not use keywords or regexes to decide whether natural-language reasoning is correct.

## Reasoning basis
A `qualified`, `prioritized`, `committed`, or `active` Opportunity should preserve a `reasoning_basis` so future work can distinguish:
- `fact_refs`: canonical objects that establish the factual basis for the decision;
- `measured_refs`: the subset that directly measures an outcome/performance state, if any;
- `inferences`: material derived conclusions with `basis_refs`; confidence/uncertainty may be expressed when useful but should not require fake numeric precision;
- `unknowns`: material state that remains unverified/unmeasured.

Use canonical object IDs, not file paths, as reasoning refs. `evidence_links` may still preserve richer provenance/pointers, but it is not a substitute for this boundary.

## Economics and value
Do not infer active-business economics from a service/category label, market convention, or technical importance.

Without business-specific economic evidence, do not present relative economics such as “most profitable,” “highest revenue,” or “highest margin” as established active-business facts. A technically important page/service can still be described as business-relevant, commercial-intent, conversion-path, priority, dependency-critical, or otherwise important when that interpretation is supported by known objectives/context and the observed condition.

When exact economics are unknown, preserve that uncertainty rather than inventing precision. The model may still make a reasoned decision from the best evidence available.

## Performance and causal outcomes
Do not convert prerequisites/signals into downstream measured outcomes.

Examples:
- Observable: a page contains `noindex`.
- Inference: removing an unintended `noindex` is a prerequisite for normal index eligibility.
- Unknown without search-engine observation: current indexed/ranking state and traffic impact.

- Observable: `robots.txt` disallows a resource path.
- Inference: compliant crawlers may be unable to fetch that resource through ordinary crawling, reducing discoverability/usefulness.
- Not established from robots.txt alone: the URL cannot be indexed, no search engine can discover it, or no AI answer system can ever cite/use it.

- Observable: a canonical points to another URL.
- Inference: the configuration signals a preferred/consolidated URL and may impair independent indexing of the source page.
- Not established without search-engine evidence: the source URL is actually deindexed, cannot rank, or has lost traffic.

Use calibrated reasoning when consequences are inferred rather than measured and preserve relevant unknowns. The exact wording and interpretation belong to the active model/user, not a keyword validator.

## Leading signals and measured outcomes
Rankings, search/Maps visibility, AI-answer citations or recommendations, links, impressions, clicks, traffic, engagement, and similar upstream signals can be genuinely valuable because they affect exposure, discovery, attention, and downstream opportunity. They should not be dismissed merely because revenue has not yet been observed.

At the same time, preserve what each signal actually establishes. A ranking gain is evidence of improved search visibility; it is not automatically evidence of incremental revenue. An AI citation can increase exposure/opportunity; it does not by itself prove conversion or profit. Use the strongest relevant evidence available and keep distinct stages of the causal pathway distinct when that distinction matters to the decision.

Claims about actual observed performance should be grounded in evidence appropriate to the claim. If downstream impact is not measured, the model can still reason from leading evidence while stating the remaining uncertainty.

## Priority is still allowed
Incomplete measurement does not prevent prioritization. A deterministic technical defect can be addressed first because of dependency order, reversibility, risk, and alignment with a known Objective without inventing ROI or asserting an unmeasured outcome.

Likewise, the model may prioritize visibility, traffic, authority, or other leading improvements when those are valuable for the current business objective. No universal numeric score or fixed signal hierarchy is required; use context-sensitive judgment.
