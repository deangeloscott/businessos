# Content Intelligence Defaults

Content intelligence must leave auditable support for material conclusions, not only a concise canonical summary. An `Observation`, `Insight`, or `Learning` is durable decision state; it does not replace the work that supports it.

## Native execution floor

- Define the decision and the scope needed to answer it. Record population/sample, platform, period, comparison basis, and metric/proxy meanings when those details materially affect interpretation. Unknown distribution, paid amplification, audience size, or measurement conditions remain explicit.
- Inspect actual evidence items. Preserve a bounded sample with a canonical/local reference and a literal `support_excerpt` present in the captured evidence for every sampled item. Every sample and finding reference must resolve at completion. A URL, search result, list of names, or unsupported summary without captured support is discovery—not analysis; current/public performance claims require item-level captured evidence.
- Compare like with like where comparison is part of the decision. Use creator/account/content baselines, cohorts, rates, distributions, or an explicitly justified qualitative comparison. Never let raw reach or one winner stand in for normalized effectiveness.
- Decompose the content mechanism where relevant: topic, hook, tension, sequence, proof/demo, visual grammar, pacing, payoff, CTA, interaction, and distribution context. Separate reusable mechanism from protected expression, creator identity, audience advantage, and platform effects.
- Test important interpretations against limitations, counterexamples, and plausible alternatives when they could change the decision. Do not add ceremonial uncertainty sections that contribute nothing to the work.
- End with the business implication and a bounded recommended action or experiment. Do not promote a durable Learning beyond the maturity supported by the evidence.

## Proportionate auditable work record

For material analysis that writes `Observation`, `Insight`, or `Learning`, save a compact Run-local JSON work record alongside the canonical objects. The record should preserve what a later reviewer needs to reconstruct the decision without forcing irrelevant fields merely to satisfy a validator.

At minimum preserve:

- `contract_id`, `status`, and the method actually used;
- `evidence_sample`, each item containing a reconstructable local/canonical `ref`, a literal `support_excerpt` from that evidence, and the item-level observation;
- `findings`, each with a substantive statement, evidence references, and mechanism where the workflow is explaining why something appears to work;
- `limitations` / unresolved uncertainty that materially affects the conclusion;
- `recommended_actions` tied to the decision being made.

Add `analysis_scope`, comparisons/baselines/normalization, alternative explanations, counterexamples, or other fields when the task actually requires them. A valid no-finding record uses `status: "no_finding"`, still records the inspected evidence and method, and does not manufacture a finding. Canonical state and the work record should reference the same evidence chain.
