---
id: customer-optimization.intervention.adoption
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
workflows:
  required:
  - customer-optimization.adoption.path-design
---
# Adoption Optimization

## Purpose
Help customers use the capabilities/behaviors necessary to realize ongoing value rather than maximizing feature clicks.

## Business Outcome
Improve customer progression and value realization through adoption optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires adoption optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define desired adoption behaviors from customer outcomes and business value, not feature usage in isolation.
2. [DETERMINISTIC] Segment customers by relevant use-case, maturity, entitlement, tenure, and behavior; identify under-adoption relative to expected value path.
3. [HYBRID] Join customer feedback/support/success evidence to distinguish lack of awareness, relevance, ability, workflow fit, technical constraint, or poor feature value.
4. [AI] Design education, in-product/process guidance, success outreach, workflow change, or product escalation accordingly. Use relevant Content/Marketing operating knowledge directly when communication is part of the solution.
5. [HYBRID] Avoid nudging customers into irrelevant features solely to raise adoption metrics.
6. [DETERMINISTIC] Measure value realization, retention, support burden, and customer sentiment guardrails when evidence is available.
7. [HYBRID] If real changes are implemented, verify them when practical. Preserve a WorkRequest, ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
