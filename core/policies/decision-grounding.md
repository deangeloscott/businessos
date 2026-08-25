# Decision Grounding & Inference Policy

Use this policy whenever a workflow creates or materially updates an `Opportunity` or another canonical decision object.

## Core rule
A verified fact does **not** automatically verify every consequence the model infers from that fact. BusinessOS must preserve the boundary between:
- established business/context facts;
- direct observations and measured outcomes;
- derived causal/strategic inference;
- unknown or unmeasured state.

An Opportunity may recommend action under uncertainty, but it may not phrase an unsupported inference as established business, economic, search-performance, customer, or AI-answer truth.

## Required reasoning basis
A `qualified`, `prioritized`, `committed`, or `active` Opportunity must include `reasoning_basis`:
- `fact_refs`: canonical objects that establish the factual basis for the decision;
- `measured_refs`: the subset that directly measures an outcome/performance state, if any;
- `inferences`: material derived conclusions, each with `basis_refs` and confidence;
- `unknowns`: material state that remains unverified/unmeasured.

Use canonical object IDs, not file paths, as reasoning refs. `evidence_links` may still preserve richer provenance/pointers, but it is not a substitute for this boundary.

## Economics and value
Do not infer active-business economics from a service/category label, market convention, or technical importance.

Without business-specific economic evidence, do not call a service/page/customer segment:
- highest-value / most valuable;
- most profitable / highest-margin;
- highest-revenue / biggest revenue driver;
- a high-value service **as an active-business economic fact**.

A technical page can still be called **business-relevant**, **commercial-intent**, **conversion-path**, **priority**, or **dependency-critical** when those descriptions are supported by known scope/objectives and the observed condition. If relative economics are unknown, say so.

## Performance and causal outcomes
Do not convert prerequisites/signals into measured outcomes.

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

Use calibrated language such as `may`, `can`, `likely`, `risk`, `suggests`, or explicit `Inference:` framing where the consequence is derived rather than measured. Preserve the relevant unknowns.

## Measured claims
Claims about actual rankings, traffic, impressions, clicks, CTR, leads, conversions, revenue, search demand, competitor visibility, or AI-answer mentions/citations require outcome/performance evidence appropriate to that claim.

If such evidence is absent, convert the statement to a hypothesis/inference or mark the state unknown. Do not manufacture a number, direction, relative position, or causal effect.

## Priority is still allowed
Incomplete measurement does not prevent BusinessOS from prioritizing obvious prerequisite work. A deterministic technical defect can be ranked first because of dependency order, reversibility, risk, and alignment with a known Objective without inventing ROI or asserting an unmeasured outcome.
