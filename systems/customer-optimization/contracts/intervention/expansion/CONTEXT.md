---
id: customer-optimization.intervention.expansion
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
  - customer-optimization.expansion.eligibility
---
# Account / Customer Expansion Optimization

## Purpose
Coordinate broader expansion within existing customer relationships based on demonstrated value and new eligible use cases.

## Business Outcome
Improve customer progression and value realization through account / customer expansion optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires account / customer expansion optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define expansion types relevant to the business: seats, locations, volume, tier, use cases, departments, services, or products.
2. [DETERMINISTIC] Identify expansion-ready accounts from success, usage/capacity, organizational signals, contract timing, and unmet needs.
3. [HYBRID] Validate with Customer Intelligence/success evidence so usage alone is not mistaken for intent.
4. [AI] Map stakeholders, value proof, use-case expansion, procurement/process needs, and likely objections.
5. [HYBRID] Design handoff/process and delegate commercial messaging to Marketing/Sales where applicable.
6. [DETERMINISTIC] Measure incremental profitable expansion plus adoption/retention guardrails.
