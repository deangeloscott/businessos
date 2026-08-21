---
id: customer-optimization.intervention.retention
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
  - customer-optimization.retention.risk-segmentation
  - customer-optimization.retention.intervention-plan
---
# Retention Optimization

## Purpose
Increase sustained customer value/continuation by improving the experience and outcomes that drive durable retention.

## Business Outcome
Improve customer progression and value realization through retention optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires retention optimization to improve a defined customer transition or outcome.

## Process
1. [HYBRID] Define retention period/state appropriate to business model and segment, including what constitutes healthy retained value.
2. [DETERMINISTIC] Cohort retention by acquisition, offer, activation, usage/service milestones, customer experience, and economic attributes.
3. [AI] Identify likely retention drivers and failure mechanisms using Customer Insights and Optimization evidence.
4. [HYBRID] Prioritize interventions that improve underlying value realization over temporary lock-in or discounting.
5. [AI] Design lifecycle, success, education, product/process, service, or expectation interventions and delegate components appropriately.
6. [DETERMINISTIC] Measure incremental retention, LTV/margin, satisfaction/support, and future expansion guardrails.
