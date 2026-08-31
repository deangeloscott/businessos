---
id: customer-optimization.journey.mapping
type: playbook
version: 1.1.0
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
# Customer Journey Mapping

## Purpose
Create an operational customer progression model with measurable stages/transitions and expected customer/business state.

## Business Outcome
Improve customer progression and value realization through customer journey mapping, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires customer journey mapping to improve a defined customer transition or outcome.

## Process
1. [AI] Define the relevant customer journey boundary for the business model rather than assuming every standard lifecycle stage applies.
2. [HYBRID] Map actual stages from discovery/consideration through purchase/onboarding/value/retention/expansion/referral as applicable.
3. [AI] For each stage define customer job, desired customer state, desired business state, entry/exit conditions, touchpoints, responsible function, and common failure modes.
4. [DETERMINISTIC] Define measurable transitions and canonical metrics/data sources where available.
5. [HYBRID] Reconcile documented process with actual customer behavior and Customer Insights; label uninstrumented assumptions.
6. [DETERMINISTIC] Persist CustomerJourney and known friction references; propose instrumentation gaps.
