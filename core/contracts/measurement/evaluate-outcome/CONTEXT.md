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
Determine what happened after an intervention and how confidently it can be attributed.

## Business Outcome
Convert measurement into decision-quality evidence rather than raw metric reporting.

## Run When
When a predefined evaluation condition/window closes or a severe guardrail warrants early review.

## Do Not Run When
Do not evaluate causal effect before required data quality/minimum observation conditions unless reporting an explicitly provisional result.

## Process
1. [HYBRID] Reconstruct hypothesis, expected mechanism, baseline, target metrics, evaluation window, and guardrails.
2. [DETERMINISTIC] Validate metric data health, comparable dimensions, source authority, coverage, and evidence class. When an authoritative governed measurement/evaluation source is available, use its result and evidence ceiling as input rather than silently replacing it with model-calculated claims.
3. [HYBRID] Compare baseline/post state using the declared attribution method and account for seasonality, demand shifts, concurrent changes, mix, and other confounders.
4. [AI] Describe observed effect, alternative explanations, and whether the result is positive, negative, neutral, or inconclusive.
5. [HYBRID] Assign causal confidence separately from effect size. Preserve distinctions among execution receipt, correlation, attribution, modeled estimate, incrementality evidence, experiment result, and causally supported outcome.
6. [HYBRID] Recommend continue, expand, modify, rollback, retest, or no decision.
7. [DETERMINISTIC] Persist OutcomeEvaluation and emit evaluation.completed.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
