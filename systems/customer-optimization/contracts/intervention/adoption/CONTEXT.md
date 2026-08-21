---
id: customer-optimization.intervention.adoption
type: playbook
version: 1.3.0
owner_system: customer-optimization
risk: medium
autonomy_ceiling: 3
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes:
- ActionPacket
- WorkRequest
- ChangeEvent
- Experiment
- MetricObservation
- OutcomeEvaluation
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - crm.contact.update
  - crm.opportunity.read
  - checkout.read
  - checkout.update
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - email.send
  - workflow.update
  - experiment.run
context:
- EconomicContext
- Offer
subcontracts:
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
4. [AI] Design education, in-product/process guidance, success outreach, workflow change, or product escalation accordingly.
5. [HYBRID] Avoid nudging customers into irrelevant features solely to raise adoption metrics.
6. [DETERMINISTIC] Measure value realization, retention, support burden, and customer sentiment guardrails.
