---
id: customer-optimization.learning.domain-learning
type: playbook
version: 1.1.0
owner_system: customer-optimization
reads:
- OutcomeEvaluation
- Insight
- Learning
- MetricObservation
writes:
- Learning
capabilities:
  required:
  - none
  optional:
  - none
---
# Customer Optimization Learning

## Purpose
Improve journey definitions, friction diagnosis, intervention timing, lifecycle thresholds, and progression strategies from verified outcomes.

## Business Outcome
Improve customer progression and value realization through customer optimization learning, while protecting customer and business guardrails.

## Run When
Run during periodic learning cycles or after sufficient OutcomeEvaluations/corrections accumulate.

## Process
1. [DETERMINISTIC] Compare progression/retention/value outcomes across comparable cohorts and interventions.
2. [HYBRID] Separate customer-selection, seasonality, product/offer changes, and service capacity from intervention effects.
3. [AI] Identify recurring friction mechanisms, intervention patterns, time-to-value/retention drivers, and segment-specific conditions.
4. [HYBRID] Distinguish customer behavior Learning from Customer Intelligence motivations unless direct evidence supports both.
5. [DETERMINISTIC] Update domain Learning and propose broader Business Learning when justified.
