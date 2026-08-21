---
id: customer-optimization.onboarding.escalation
type: playbook
version: 1.3.0
owner_system: customer-optimization
risk: medium
autonomy_ceiling: 2
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
- ActionPacket
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
# Onboarding Escalation Design

## Purpose
Define when stalled onboarding should move from automated guidance to human/technical/customer-success intervention.

## Business Outcome
Help customers before delays become abandonment while avoiding unnecessary high-touch escalation.

## Run When
Run when onboarding contains failure/stall conditions requiring differentiated response.

## Process
1. [DETERMINISTIC] Define stall/failure states from milestone timing, repeated errors, unresolved dependencies, explicit help request, high-value/risk conditions, or technical failure.
2. [AI] Classify likely issue and determine whether self-service, specialist, support, implementation, account/customer-success, or other owner is appropriate.
3. [HYBRID] Avoid escalation based solely on opaque risk score or customer value when customer harm/safety requires support.
4. [DETERMINISTIC] Define escalation priority, context package, owner, response expectation, and duplicate-suppression.
5. [AI] Ensure the receiving human/system gets the exact history, attempted steps, evidence, customer state, and next decision—without making the customer repeat everything.
6. [DETERMINISTIC] Track acceptance, resolution, resumed milestone, and unresolved root cause.
7. [AI] Feed recurring escalations into systemic friction diagnosis.
