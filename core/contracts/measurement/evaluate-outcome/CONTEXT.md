---
id: core.measurement.evaluate-outcome
type: service
owner_system: core
reads:
- Opportunity
- ChangeEvent
- VerificationRecord
- MetricObservation
- Experiment
writes:
- OutcomeEvaluation
capabilities:
  required:
  - none
  optional:
  - business.measurement.read
  - business.measurement.evaluate
  - business.data.query
  - business.data.explain
---
# Evaluate Outcome

## Purpose
Determine what happened after an intervention and how confidently the observed result can be attributed, without turning measurement into a runtime routing lifecycle.

## Business Outcome
Convert measurement into reusable decision evidence rather than raw metric reporting or automatic next-action control.

## Run When
When enough relevant post-intervention evidence exists to answer a material outcome question, including a predefined evaluation window or an important guardrail review.

## Do Not Run When
Do not claim causal effect before the required data quality/observation conditions are met unless the result is explicitly provisional and its limitations are preserved.

## Process
1. [HYBRID] Reconstruct the decision question, hypothesis/mechanism when one existed, baseline, relevant metrics, evaluation window, and guardrails from the strongest available organizational evidence.
2. [HYBRID] Assess metric data health, comparable dimensions, source authority, coverage, and evidence class. When an authoritative governed measurement/evaluation source is available, use its result and evidence ceiling as input rather than silently replacing it with model-calculated claims.
3. [HYBRID] Compare baseline/post state using the attribution method actually supported and account for seasonality, demand shifts, concurrent changes, mix, and other material confounders.
4. [AI] Describe observed effect, alternative explanations, and whether the evidence is positive, negative, neutral, mixed, or inconclusive.
5. [HYBRID] Assign causal confidence separately from effect size. Preserve distinctions among implementation receipt, correlation, attribution, modeled estimate, incrementality evidence, experiment result, and causally supported outcome.
6. [AI] State what the evidence suggests the organization should consider next when useful, but do not manufacture a mandatory disposition, route, rollback, expansion, or retest lifecycle.
7. [DETERMINISTIC] Persist the OutcomeEvaluation when the result has durable organizational value. Do not emit an AURA runtime event merely because evaluation completed.

## Verification
- The OutcomeEvaluation is schema-valid and traceable to the actual evidence and target/intervention being evaluated.
- Effect magnitude, causal confidence, data quality, and recommendation remain distinct.

## Failure / Fallback
- If a preferred measurement capability/source is unavailable, use another valid source/method when it can answer the question. Otherwise preserve the limitation or unresolved measurement need instead of creating a Manual Action Packet or fabricating an outcome.

## Completion Criteria
- Future work can understand what happened, what can and cannot be attributed, the material uncertainty, and why the conclusion is justified without requiring an event or next-route object.
