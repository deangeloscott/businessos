---
id: customer-optimization.measurement.cohort-retention
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
# Cohort Retention Analysis

## Purpose
Compare retention/renewal behavior across cohorts and lifecycle experiences to locate durable drivers and risks.

## Business Outcome
Identify actionable retention patterns without confusing cohort composition with causal intervention effects.

## Run When
Run when retention/churn trends must be understood beyond a single aggregate rate.

## Process
1. [DETERMINISTIC] Define retention event/window, cohort start, eligibility, censored cases, plan/segment dimensions, and metric denominator consistently.
2. [DETERMINISTIC] Build cohort curves/tables and compare renewal/churn timing rather than only a final aggregate percentage.
3. [AI] Identify material differences by acquisition, onboarding/activation, usage/value, support, product/offer, tenure, and customer segment where relevant.
4. [AI] Test for cohort-mix, seasonality, pricing/product changes, and survivorship effects.
5. [HYBRID] Treat associations as hypotheses until mechanism/evidence supports causal claims.
6. [AI] Link Customer Insights/churn reasons to behavioral patterns where appropriate.
7. [AI] Produce Journey Insights and prioritized diagnostic questions/interventions.
