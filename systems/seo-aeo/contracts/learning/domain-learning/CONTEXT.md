---
id: seo.aeo.learning.domain-learning
type: playbook
owner_system: seo-aeo
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
# SEO/AEO Domain Learning

## Purpose
Turn repeated verified organic-discovery outcomes into scoped reusable guidance for future diagnosis, intervention choice, and measurement.

## Business Outcome
Help future SEO/AEO work make better evidence-based choices for this organization without turning AURA into a self-tuning optimization controller.

## Run When
Use when enough comparable OutcomeEvaluations, corrections, failures, or repeated SEO/AEO work exists to support a reusable pattern. Time passing alone is not a reason to run a learning cycle.

## Process
1. [AI] Group genuinely comparable interventions/outcomes by mechanism, search/answer surface, demand type, market, asset type, audience/business context, and other conditions that could change applicability.
2. [HYBRID] Separate plausible intervention effect from demand, algorithm/platform changes, competitor movement, seasonality, concurrent changes, measurement error, and other confounders using the strongest available causal evidence.
3. [AI] Identify repeatable mechanisms, failure modes, response conditions, and measurement heuristics. Do not create hard thresholds or universal rules unless the evidence actually supports them.
4. [AI] Keep SEO-specific guidance scoped to organic discovery. A broader Business Learning is justified only when evidence across domains supports the broader claim; no automatic cross-domain promotion occurs.
5. [AI] State applies-when, does-not-apply-when, supporting/contradictory evidence, uncertainty, and what would revise the lesson.
6. [HYBRID] Create/update Learning only when forgetting the pattern would materially reduce future quality or efficiency. Deterministic helpers validate/persist the chosen Learning; they do not decide maturity, applicability, promotion, contradiction, or deprecation.

## Verification
- Learning scope does not exceed the supporting outcomes.
- Search/platform correlation is not treated as causal intervention effect without appropriate evidence.
- No scheduler, automatic threshold tuner, tactic router, or deterministic semantic promotion is encoded in Learning.

## Completion Criteria
- Future SEO/AEO work can reuse an evidence-backed conditional lesson that improves judgment without inheriting a hidden optimization loop.
