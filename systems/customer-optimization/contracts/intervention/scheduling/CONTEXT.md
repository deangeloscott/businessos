---
id: customer-optimization.intervention.scheduling
type: playbook
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
# Scheduling & No-Show Optimization

## Purpose
Make scheduling easy for qualified customers and reduce avoidable no-shows without coercive reminders.

## Business Outcome
Improve customer progression and value realization through scheduling & no-show optimization, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires scheduling & no-show optimization to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Analyze scheduling funnel: availability shown, booking completion, lead time, reschedule/cancel, reminder delivery, attendance, and downstream quality.
2. [AI] Identify friction from availability, timezone, form effort, unclear meeting value, delay, calendar conflict, instructions, or poor qualification.
3. [HYBRID] Use Customer Insights to distinguish motivation/expectation issues from process friction.
4. [AI] Design improvements to availability, confirmation, reminders, preparation, rescheduling, and recovery after missed appointments.
5. [DETERMINISTIC] Define attendance and qualified-outcome guardrails; excessive reminders are not automatically better.
6. [INTEGRATION] Implement workflow changes or delegate reminder messaging to Marketing; verify states and measure.
