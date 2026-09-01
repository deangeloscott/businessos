---
id: customer-optimization.learning.domain-learning
type: playbook
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
Turn repeated journey/intervention outcomes into scoped reusable guidance about friction mechanisms, progression, time-to-value, retention, and customer-value restoration.

## Business Outcome
Help future customer-journey work improve progression and value realization without turning AURA into an automatic lifecycle-optimization engine.

## Run When
Use when enough comparable OutcomeEvaluations, corrections, failures, or repeated journey work exists to support a reusable pattern. Time passing alone does not trigger a learning cycle.

## Process
1. [HYBRID] Compare progression, retention, value, harm/guardrail, and intervention outcomes across genuinely comparable cohorts/contexts.
2. [HYBRID] Separate customer selection, seasonality, product/offer changes, service capacity, concurrent changes, and other confounders from the intervention mechanism.
3. [AI] Identify recurring friction mechanisms, intervention patterns, time-to-value/retention drivers, and segment/context conditions where they appear useful or harmful.
4. [AI] Keep observed customer behavior distinct from inferred motivation/customer truth unless direct Customer Intelligence evidence supports both.
5. [AI] State applicability, negative cases, customer/business guardrails, contradictory evidence, uncertainty, and what would revise the lesson. Do not turn a learned pattern into an automatic intervention threshold.
6. [HYBRID] Create/update Customer Optimization Learning only when it materially improves future work. Broader Business Learning requires genuinely broader evidence; deterministic helpers validate/persist rather than deciding semantic scope/maturity.

## Verification
- Short-term conversion/progression gains do not override downstream customer-value or harm evidence.
- One successful retention/conversion intervention is not generalized across customer states.
- Learning does not encode scheduler state, automatic customer action, or opaque lifecycle scoring.

## Completion Criteria
- Future customer-journey work can reuse a scoped evidence-backed lesson while the active model/user still chooses whether and how to intervene.
