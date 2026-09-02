---
id: customer-optimization.intervention.repeat-purchase
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
# Repeat Purchase Optimization

## Purpose
Increase appropriate repeat purchases by making replenishment/reuse timing and value clear without over-contacting.

## Business Outcome
Improve customer progression and value realization through repeat purchase optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires repeat purchase optimization to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Analyze purchase intervals, product/category replenishment cycles, customer cohorts, usage/consumption proxies, and repeat rates.
2. [AI] Identify why customers do/do not return: timing, satisfaction, awareness, convenience, price, alternatives, changed need, or product fit.
3. [HYBRID] Define eligible moments and suppression rules; avoid prompting repurchase when likely unnecessary/inappropriate.
4. [AI] Design reminders, reorder convenience, bundles, education, loyalty/value communication, or service interventions as appropriate. Use relevant Marketing/Content operating knowledge directly when communication quality matters rather than creating an internal domain handoff.
5. [DETERMINISTIC] Measure incremental profitable repeat purchases, unsubscribes/complaints, discount cost, and long-term value when evidence is available.
6. [HYBRID] If real workflow or communication changes are implemented, verify them when practical. Preserve a WorkRequest, ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
