---
id: customer-optimization.intervention.qualification
type: playbook
version: 1.1.0
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes:
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
# Lead Qualification Optimization

## Purpose
Improve how the right prospects are identified/routed while minimizing false rejection and wasted effort.

## Business Outcome
Improve customer progression and value realization through lead qualification optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires lead qualification optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define what “qualified” means from business economics, Offer fit, capacity, customer success, and sales/process constraints.
2. [DETERMINISTIC] Analyze current qualification rules, fields, scores, routing, acceptance/rejection, downstream win/value, and false-positive/negative evidence.
3. [HYBRID] Identify redundant questions, missing predictive evidence, bias/leakage, gaming, and qualification-stage friction.
4. [AI] Design simpler rules/questions/signals with transparent rationale; avoid using sensitive/prohibited attributes improperly.
5. [DETERMINISTIC] Backtest proposed rules on historical cohorts where valid and define guardrails.
6. [INTEGRATION] Implement/experiment when authorized; verify routing and monitor downstream customer quality.
