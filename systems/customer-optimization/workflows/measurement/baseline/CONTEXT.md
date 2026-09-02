---
id: customer-optimization.measurement.baseline
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
# Journey Intervention Baseline

## Purpose
Establish the pre-intervention customer and business state required to evaluate a journey change.

## Business Outcome
Make optimization outcomes interpretable rather than relying on before/after anecdotes.

## Run When
Run before a material Customer Optimization intervention when a suitable baseline is not already available.

## Process
1. [DETERMINISTIC] Define target population, transition/outcome, metric definitions, data sources, period, eligibility, and exclusions.
2. [DETERMINISTIC] Calculate current transition, delay/time-to-value, downstream outcome, quality/guardrail, and volume metrics appropriate to the Opportunity.
3. [AI] Identify seasonality, trend, campaign/offer/product/process changes, cohort mix, and data-quality issues that could change the baseline.
4. [DETERMINISTIC] Preserve cohort/dimension definitions so post-change measurement is comparable.
5. [HYBRID] Use historical/control/range baselines when a single before-period would be misleading.
6. [DETERMINISTIC] Link baseline MetricObservations to the Opportunity/Experiment and state measurement window.
7. [AI] Document what the baseline can/cannot support causally.
