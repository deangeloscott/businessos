---
id: customer-optimization.intervention.sales-handoff
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
# Sales Handoff Optimization

## Purpose
Reduce delay, context loss, ownership ambiguity, and customer effort when qualified leads move between systems/people.

## Business Outcome
Improve customer progression and value realization through sales handoff optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires sales handoff optimization to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Map trigger → assignment → notification → first contact → context transfer → acceptance/reassignment states.
2. [DETERMINISTIC] Measure latency, failure/reassignment, missing context, duplicate outreach, customer wait, and downstream outcomes.
3. [AI] Review sales/customer evidence for common handoff confusion or expectation mismatch.
4. [HYBRID] Diagnose ownership/routing/process/data problems versus salesperson skill issues outside current scope.
5. [HYBRID] Define service levels, routing rules, context packet, escalation, and fallback ownership.
6. [INTEGRATION] Implement workflow/CRM updates when authorized and verify end-to-end with test records.
