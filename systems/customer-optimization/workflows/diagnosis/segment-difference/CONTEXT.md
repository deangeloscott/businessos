---
id: customer-optimization.diagnosis.segment-difference
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
# Journey Segment Difference Analysis

## Purpose
Determine whether journey performance/friction differs meaningfully across customer groups and why.

## Business Outcome
Avoid one-size-fits-all optimization when customer context changes the mechanism.

## Run When
Run when transition performance, churn, activation, renewal, or time-to-value appears heterogeneous.

## Process
1. [DETERMINISTIC] Define comparable cohorts using canonical AudienceSegments and only necessary operational dimensions.
2. [DETERMINISTIC] Calculate transition/outcome differences with sample size/volume, timeframe, and baseline context.
3. [AI] Identify operational/customer/product/offer differences that could explain the observed gap.
4. [AI] Test whether the difference persists after controlling obvious acquisition, tenure, plan, geography, or lifecycle confounders where data permits.
5. [HYBRID] Avoid creating sensitive/inferred profiling segments or overinterpreting small/noisy groups.
6. [AI] Determine whether separate journeys/interventions are justified or one process can serve both with minor variation.
7. [AI] Publish scoped Journey Insights and update Opportunity targeting/guardrails.
