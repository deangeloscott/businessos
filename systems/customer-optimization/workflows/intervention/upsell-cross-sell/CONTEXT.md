---
id: customer-optimization.intervention.upsell-cross-sell
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes: []
context:
- EconomicContext
- Offer
---
# Upsell / Cross-Sell Optimization

## Purpose
Identify when an additional offer genuinely improves customer outcomes and present it at the right lifecycle moment.

## Business Outcome
Improve customer progression and value realization through upsell / cross-sell optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires upsell / cross-sell optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Map customer achieved/current outcomes to adjacent unmet needs and canonical Offers/products that can credibly help.
2. [DETERMINISTIC] Identify eligibility, usage/success prerequisites, timing signals, historical uptake, margin, and downstream success.
3. [HYBRID] Exclude customers with unresolved core value/support problems or poor fit; expansion should not mask failure.
4. [AI] Define trigger, value rationale, proof, friction, and appropriate channel or real-world handoff.
5. [HYBRID] Use relevant Marketing and Content operating knowledge directly for persuasion and education when those components are useful. Persist a WorkRequest only for a real durable organizational handoff; AURA domains do not delegate to one another as internal services.
6. [DETERMINISTIC] Measure incremental expansion value, adoption/success, churn/refund/support, and cannibalization guardrails when evidence is available.
7. [HYBRID] Preserve a ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
