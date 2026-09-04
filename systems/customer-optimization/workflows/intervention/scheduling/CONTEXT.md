---
id: customer-optimization.intervention.scheduling
type: workflow
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  domain: customer-intelligence
- MetricObservation
writes: []
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
3. [HYBRID] Use relevant Customer evidence to distinguish motivation/expectation issues from process friction.
4. [AI] Design improvements to availability, confirmation, reminders, preparation, rescheduling, and recovery after missed appointments.
5. [DETERMINISTIC] Define attendance and qualified-outcome guardrails; excessive reminders are not automatically better.
6. [INTEGRATION] When requested and supported by the active harness, implement real scheduling/workflow changes directly. Use relevant Marketing operating knowledge directly for reminder/message quality; persist a WorkRequest only for a real durable organizational handoff.
7. [HYBRID] Verify changed states and measure the useful outcome when practical. Preserve a ChangeEvent, Experiment, measurement, evaluation, or Learning only when that meaning actually occurred.
