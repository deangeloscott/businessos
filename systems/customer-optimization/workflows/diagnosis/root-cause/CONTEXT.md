---
id: customer-optimization.diagnosis.root-cause
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
6. [HYBRID] When a cause is primarily about persuasion, customer understanding, product, sales, operations, or another area, use the relevant operating knowledge or real organizational expertise directly rather than routing it through an internal AURA domain service.
7. [AI] Preserve a scoped Journey Insight when a durable interpretation will help future work, and qualify an intervention Opportunity when a distinct intervention is justified. The model/user may do either in the order the evidence and real decision require; an Insight is not a universal prerequisite for an Opportunity.
