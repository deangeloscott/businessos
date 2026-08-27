# Content Intelligence Defaults

Content intelligence must leave an auditable analysis, not only a concise canonical conclusion. An `Observation`, `Insight`, or `Learning` is the durable decision object; it does not replace the work that supports it.

## Native execution floor

- Define the decision, scope, population/sample, platforms, period, comparison basis, and metric/proxy meanings before interpreting results. Unknown distribution, paid amplification, audience size, or measurement conditions remain explicit.
- Inspect actual evidence items. Preserve a bounded sample or reconstructable references with enough item-level context to audit selection, deduplication, and comparison. A search result, list of names, or unsupported summary is discovery—not analysis.
- Compare like with like where possible. Use creator/account/content baselines, cohorts, rates, distributions, or explicitly justified qualitative comparison. Never let raw reach or one winner stand in for normalized effectiveness.
- Decompose the content mechanism: topic, hook, tension, sequence, proof/demo, visual grammar, pacing, payoff, CTA, interaction, and distribution context as applicable. Separate reusable mechanism from protected expression, creator identity, audience advantage, and platform effects.
- Test the leading interpretation against counterexamples and plausible alternatives. State limitations, uncertainty, applicability, non-applicability, and what additional evidence could change the conclusion.
- End with the business implication and a bounded recommended action or experiment. Do not promote a durable Learning beyond the maturity supported by the evidence.

## Auditable work record

For completed analysis that writes `Observation`, `Insight`, or `Learning`, save a Run-local JSON work record alongside the canonical objects. Use this portable shape:

- `contract_id`, `status`, and `analysis_scope`;
- `method`, including selection and comparison/normalization logic;
- `evidence_sample`, with reconstructable local/canonical references and item-level observations;
- `comparisons`, including baselines or criteria actually applied;
- `findings`, each with a statement, evidence references, mechanism, and alternative explanations;
- `limitations` and unresolved uncertainty;
- `recommended_actions` and the decision each action serves.

A valid no-finding record uses `status: "no_finding"`, still records the inspected sample/method/comparisons/limitations, and does not manufacture a finding. Canonical state and the work record should reference the same evidence chain.
