---
id: customer-optimization.retention.intervention-plan
type: workflow
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
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Retention Intervention Plan

## Purpose
Design mechanism-specific actions that restore value, resolve friction, or improve fit for customers at genuine churn risk.

## Business Outcome
Improve retention through customer value rather than cancellation obstruction or indiscriminate discounts.

## Run When
Run after a churn/retention risk mechanism is sufficiently diagnosed.

## Process
1. [AI] Restate customer/account state, diagnosed risk mechanism, desired value/recovery state, evidence, urgency, and real organizational owner where one exists.
2. [AI] Generate interventions targeting root cause: value realization, service recovery, adoption help, product/process fix, expectation reset, contract/term review, customer-success conversation, or appropriate exit.
3. [HYBRID] Reject dark patterns, cancellation friction, guilt, deceptive save offers, or benefits that disadvantage healthy customers unfairly without reason.
4. [AI] Determine when personalized human intervention is required versus scalable workflow.
5. [DETERMINISTIC] Define concrete intervention steps, triggers, suppression, deadline, success/guardrail metrics, and rollback/stop conditions in the real operating process.
6. [AI] Use relevant Content or Marketing operating knowledge directly when communication/persuasion is a true component of the intervention. Create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
7. [DETERMINISTIC] When outcome evidence becomes available, evaluate retention plus customer outcome/complaints/cost and preserve Learning only when the evidence supports a reusable lesson.
