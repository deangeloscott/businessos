---
id: customer-optimization.diagnosis.root-cause
type: playbook
version: 1.3.0
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
# Journey Root-Cause Diagnosis

## Purpose
Determine why a journey transition is failing, delayed, or producing poor customer outcomes before designing an intervention.

## Business Outcome
Solve the actual cause instead of adding messages or automation around a broken process.

## Run When
Run after a material bottleneck/friction condition is identified.

## Process
1. [DETERMINISTIC] Resolve the affected transition, cohort, before/after states, instrumentation, Customer Insights, support/sales/product evidence, and recent changes.
2. [AI] Generate plausible cause classes: customer understanding, persuasion, fit, product/service capability, process steps, ownership/handoff, technical failure, policy/terms, timing, price, data/instrumentation, or external condition.
3. [AI] Map observable evidence that supports or falsifies each cause and retrieve/collect the highest-information evidence first.
4. [DETERMINISTIC] Compare successful versus failed/slow cases and relevant segments while controlling obvious confounders where possible.
5. [AI] Identify primary/contributing causes and causal uncertainty; do not convert correlation into motive or cause.
6. [HYBRID] Route foreign-domain causes to Marketing, Customer Intelligence, Product/Sales/human owner rather than hiding them inside Customer Optimization.
7. [AI] Publish a Journey Insight and only then qualify an intervention Opportunity.
