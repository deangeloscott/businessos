---
id: seo.measurement.change-evaluation
type: playbook
owner_system: seo-aeo
reads:
- MetricObservation
- Opportunity
- ChangeEvent
- Experiment
writes:
- MetricObservation
- Experiment
- Learning
- OutcomeEvaluation
- Opportunity
- ChangeEvent
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - revenue.read
  - ai_answer.observe
context:
- EconomicContext
- Market
- Objective
- Offer
---
# Change Event Evaluation

## Purpose
Determine whether a specific optimization likely helped, harmed, or was inconclusive.

## Business Outcome
Improve valuable organic discovery through change event evaluation, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run when the configured measurement window closes, a report is due, or **change event evaluation** evidence becomes decision-relevant.

## Process
1. [HYBRID] Load the Change Event hypothesis, affected asset/query/topic, before state, expected metrics, guardrails, and measurement plan.
2. [HYBRID] Wait until the predefined minimum observation condition/window unless an early severe negative guardrail triggers review.
3. [INTEGRATION] Retrieve post-change business/search/AI/local/technical observations and validate data health.
4. [DETERMINISTIC] Normalize for demand, position, seasonality, concurrent changes, market/device mix, and other confounders defined in the plan.
5. [AI] Classify outcome as positive, negative, neutral, or inconclusive with effect size/range and confidence.
6. [HYBRID] Write learning back to the Change Event/Opportunity and route harmful results to rollback/replanning.

## Decisions / Routing
- Route → SEO Domain Learning / Core Business Learning as justified by outcome evidence.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


