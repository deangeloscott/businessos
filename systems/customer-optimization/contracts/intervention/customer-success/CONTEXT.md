---
id: customer-optimization.intervention.customer-success
type: playbook
version: 1.1.0
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
---
# Customer Success Process Optimization

## Purpose
Improve proactive success processes that help customers achieve defined outcomes with appropriate human/automated support.

## Business Outcome
Improve customer progression and value realization through customer success process optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires customer success process optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define success outcomes/milestones by segment and offer, plus early signals of progress/risk.
2. [DETERMINISTIC] Map current success touchpoints, ownership, cadence, alerts, playbooks, response times, and outcome coverage.
3. [HYBRID] Identify gaps such as reactive support dependence, generic cadence, missing outcome tracking, handoff loss, or late risk detection.
4. [AI] Design segment/value-based success motions and escalation paths with clear customer purpose for each touchpoint.
5. [HYBRID] Determine what can be automated without degrading trust or missing high-context needs.
6. [INTEGRATION] Implement workflow/alerts/tasks when authorized; verify and measure outcomes/cost-to-serve.
