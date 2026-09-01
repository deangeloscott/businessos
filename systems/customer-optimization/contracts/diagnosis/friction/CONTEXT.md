---
id: customer-optimization.diagnosis.friction
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
# Customer Friction Diagnosis

## Purpose
Determine why a material customer progression problem occurs before choosing an intervention.

## Business Outcome
Improve customer progression and value realization through customer friction diagnosis, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires customer friction diagnosis to improve a defined customer transition or outcome.

## Process
1. [AI] Define the failing transition and affected population from Journey Observations.
2. [HYBRID] Gather quantitative behavior, customer feedback, support/sales evidence, technical state, process rules, and relevant marketing promises.
3. [AI] Generate cause classes: unclear value/instruction, effort, technical failure, process delay, qualification mismatch, trust/risk, price/payment, missing capability, handoff, expectation mismatch, external constraint.
4. [HYBRID] Test hypotheses against sequence/timing/segment evidence and direct customer evidence; separate correlation from plausible mechanism.
5. [AI] Determine whether primary ownership remains Customer Optimization or actually belongs to Marketing, Customer Intelligence, Product, Sales, or another future domain.
6. [HYBRID] Estimate business/customer impact and intervention leverage; create/update Optimization Insight/Opportunity only when diagnosis is sufficient.
