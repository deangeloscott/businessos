---
id: customer-optimization.retention.intervention-plan
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
# Retention Intervention Plan

## Purpose
Design mechanism-specific actions that restore value, resolve friction, or improve fit for customers at genuine churn risk.

## Business Outcome
Improve retention through customer value rather than cancellation obstruction or indiscriminate discounts.

## Run When
Run after a churn/retention risk mechanism is sufficiently diagnosed.

## Process
1. [AI] Restate customer/account state, diagnosed risk mechanism, desired value/recovery state, evidence, urgency, and owner.
2. [AI] Generate interventions targeting root cause: value realization, service recovery, adoption help, product/process fix, expectation reset, contract/term review, customer-success conversation, or appropriate exit.
3. [HYBRID] Reject dark patterns, cancellation friction, guilt, deceptive save offers, or benefits that disadvantage healthy customers unfairly without reason.
4. [AI] Determine when personalized human intervention is required versus scalable workflow.
5. [DETERMINISTIC] Define actions, triggers, suppression, deadline, success/guardrail metrics, and rollback/stop conditions.
6. [AI] Delegate Content/Marketing work only where communication/persuasion is a true component of the intervention.
7. [DETERMINISTIC] Evaluate retention plus customer outcome/complaints/cost and update Learning.
