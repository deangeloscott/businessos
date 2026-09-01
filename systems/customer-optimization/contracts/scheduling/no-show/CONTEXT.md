---
id: customer-optimization.scheduling.no-show
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
capabilities:
  required:
  - analytics.read
  optional:
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - checkout.read
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - experiment.run
  - workflow.update
  - email.send
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Appointment No-Show Optimization

## Purpose
Reduce avoidable missed appointments while preserving easy rescheduling/cancellation and customer respect.

## Business Outcome
Increase completed qualified appointments without coercive reminders or artificially restrictive scheduling.

## Run When
Run when scheduled calls/appointments have material no-show, late-cancel, or scheduling friction.

## Process
1. [DETERMINISTIC] Measure booking→attendance, lead time, reschedule/cancel, source, time/day/timezone, reminder delivery, qualification, and downstream quality.
2. [AI] Identify causes using customer feedback/behavior: forgotten, unclear value, long lead time, timezone/confusion, poor fit, changed need, scheduling difficulty, or process issue.
3. [AI] Test operational fixes first: immediate calendar confirmation, easy reschedule/cancel, timezone clarity, shorter lead time, appropriate availability, preparation/expectation setting.
4. [HYBRID] Delegate persuasion reminder content to Marketing when motivation/value is the issue, but avoid escalating reminder frequency blindly.
5. [DETERMINISTIC] Define reminder cadence based on actual lead time and consent/channel; suppress after cancel/reschedule/attendance.
6. [DETERMINISTIC] Test attendance and downstream quality, not only booking volume.
7. [AI] Learn which causes/interventions apply by segment/source.
