---
id: customer-optimization.intervention.qualification
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
---
# Lead Qualification Optimization

## Purpose
Improve how the right prospects are identified and progressed while minimizing false rejection and wasted effort.

## Business Outcome
Improve customer progression and value realization through lead qualification optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires lead qualification optimization to improve a defined customer transition or outcome.

## Process
1. [AI] Define what “qualified” means from business economics, Offer fit, capacity, customer success, and sales/process constraints.
2. [DETERMINISTIC] Analyze current qualification rules, fields, scores, routing, acceptance/rejection, downstream win/value, and false-positive/negative evidence.
3. [HYBRID] Identify redundant questions, missing predictive evidence, bias/leakage, gaming, and qualification-stage friction.
4. [AI] Design simpler rules/questions/signals with transparent rationale; avoid using sensitive/prohibited attributes improperly.
5. [DETERMINISTIC] Backtest proposed rules on historical cohorts where valid and define customer/business guardrails.
6. [INTEGRATION] When the user wants implementation and the active harness has the real capability and permissions, change the external qualification/routing system directly and verify the result. Otherwise return the precise design or real durable handoff needed by the actual executor; do not manufacture internal AURA routing state.
7. [HYBRID] Preserve a ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred and future work benefits from remembering it.
