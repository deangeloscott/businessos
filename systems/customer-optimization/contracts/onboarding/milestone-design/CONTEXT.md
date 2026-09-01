---
id: customer-optimization.onboarding.milestone-design
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
# Onboarding Milestone Design

## Purpose
Define the minimum customer states/milestones required to reach meaningful value and how progress is verified.

## Business Outcome
Create an onboarding path organized around value rather than internal tasks.

## Run When
Run when building or redesigning onboarding/implementation.

## Process
1. [AI] Define the meaningful value milestone and customer prerequisites/constraints.
2. [AI] Work backward to identify only necessary setup, decision, data, integration, training, configuration, or handoff milestones.
3. [AI] For each milestone define customer purpose, owner, input, completion evidence, dependencies, expected timing, and failure states.
4. [AI] Remove internal/admin steps from the customer-facing path where the business can perform them itself.
5. [HYBRID] Keep required safety/compliance/quality/qualification steps even if they add time.
6. [DETERMINISTIC] Define milestone events/instrumentation and escalation conditions.
7. [AI] Update CustomerJourney/onboarding Action plan with the minimal value path.
