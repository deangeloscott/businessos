---
id: customer-optimization.intervention.design
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
# Customer Journey Intervention Design

## Purpose
Design the smallest intervention likely to remove the diagnosed cause while protecting customer quality and downstream outcomes.

## Business Outcome
Improve the journey mechanism rather than adding unnecessary complexity.

## Run When
Run after root-cause diagnosis identifies an addressable Customer Optimization Opportunity.

## Process
1. [AI] Restate the diagnosed cause, affected customer state, desired next state, mechanism, and constraints.
2. [AI] Generate intervention options beginning with removing unnecessary steps, delay, ambiguity, handoff, or failure before adding reminders/content/automation.
3. [AI] Evaluate each option for customer effort, accessibility, operational burden, fit/qualification, risk, reversibility, dependencies, and expected downstream effect.
4. [HYBRID] Identify delegated needs: Marketing for persuasion, Content for communication, Customer Intelligence for unknown motive, other domain/human for product/sales/legal/finance causes.
5. [AI] Select the smallest viable change or controlled test capable of validating the mechanism.
6. [DETERMINISTIC] Define exact actions, success criteria, guardrails, baseline, verification, rollback, and measurement window.
7. [AI] Create ActionPacket/WorkRequests with ordered dependencies.
