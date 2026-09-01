---
id: customer-optimization.journey.transition-analysis
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- type: Insight
  owner_system: customer-intelligence
- Observation
- MetricObservation
writes:
- CustomerJourney
- Observation
- Insight
- Opportunity
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - support.ticket.read
  - checkout.read
  - billing.read
  - customer_success.read
context:
- AudienceSegment
- Objective
- Offer
---
# Journey Transition Analysis

## Purpose
Quantify where customers fail, delay, regress, or succeed between journey states.

## Business Outcome
Improve customer progression and value realization through journey transition analysis, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires journey transition analysis to improve a defined customer transition or outcome.

## Process
1. [DETERMINISTIC] Define cohort, stage/transition, eligibility, observation window, denominator, and comparable segment dimensions.
2. [INTEGRATION] Retrieve canonical events/states and validate identity stitching/data completeness.
3. [DETERMINISTIC] Calculate conversion, abandonment, delay/time-to-transition, repeat attempts, regression, and downstream outcome rates.
4. [DETERMINISTIC] Compare by segment, source, offer, cohort, device/location/channel, and relevant operational dimensions while guarding small samples.
5. [AI] Identify material anomalies/bottlenecks and sequence relationships, not causal conclusions yet.
6. [HYBRID] Join relevant Customer Insights and operational observations to prioritize diagnosis targets.
7. [DETERMINISTIC] Publish Journey Observations and candidate Optimization Insights.
