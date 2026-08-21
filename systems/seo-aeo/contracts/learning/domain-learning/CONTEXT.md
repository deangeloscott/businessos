---
id: seo.aeo.learning.domain-learning
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
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
Convert verified organic-discovery outcomes into better future diagnosis, thresholds, intervention selection, and measurement.

## Business Outcome
Improve valuable organic discovery through seo/aeo domain learning, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during periodic learning cycles or after sufficient OutcomeEvaluations/corrections accumulate.

## Process
1. [AI] Group comparable SEO interventions by mechanism, surface, demand type, market, asset type, and business context.
2. [HYBRID] Separate intervention effect from demand/algorithm/competitor/seasonality/concurrent changes using available causal evidence.
3. [AI] Identify stable domain-specific thresholds, response patterns, failure modes, and intervention conditions.
4. [HYBRID] Keep broad business conclusions outside SEO Learning and propose Business Learning only when cross-domain evidence supports it.
5. [DETERMINISTIC] Promote, contradict, or deprecate SEO Learning under Core rules.
