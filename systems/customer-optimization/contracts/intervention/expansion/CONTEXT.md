---
id: customer-optimization.intervention.expansion
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes: []
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
3. [HYBRID] Validate with relevant Customer/success evidence so usage alone is not mistaken for intent.
4. [AI] Map stakeholders, value proof, use-case expansion, procurement/process needs, and likely objections.
5. [HYBRID] Design the real customer/sales process and use relevant Marketing/Sales operating knowledge directly for commercial communication. Persist a WorkRequest only when a real organizational handoff needs to survive the current session or actor.
6. [DETERMINISTIC] Measure incremental profitable expansion plus adoption/retention guardrails when evidence is available.
7. [HYBRID] Preserve a ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
