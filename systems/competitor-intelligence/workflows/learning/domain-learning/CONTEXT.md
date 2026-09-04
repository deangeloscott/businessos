---
id: competitor.learning.domain-learning
type: workflow
owner_system: competitor-intelligence
reads:
- OutcomeEvaluation
- Insight
- Learning
- MetricObservation
writes:
- Learning
---
# Competitor Intelligence Learning

## Purpose
Turn repeated competitive-research outcomes into scoped reusable guidance about source usefulness, change detection, tactic interpretation, comparison, and strategic inference.

## Business Outcome
Help future competitive decisions use better evidence and avoid repeatedly confusing visible competitor activity with effectiveness.

## Run When
Use when enough later evidence, corrections, OutcomeEvaluations, or repeated competitor research exists to support a reusable methodological/interpretive pattern. Do not run merely because a periodic learning cycle is due.

## Process
1. [AI] Review material Competitor Insights against later competitor behavior, independent evidence, active-business outcomes, and corrections.
2. [HYBRID] Identify which source classes/signals were useful for specific fact types/contexts and which produced noise, lag, duplication, or misleading inference. Do not create a universal source-reliability score.
3. [AI] Capture recurring competitive mechanisms, research failure modes, and conditions where tactic/strategy inference proved more or less reliable.
4. [AI] Keep observed competitor behavior, inferred strategy, and evidence of effectiveness separate; one competitor's apparent success never becomes a broad best practice by itself.
5. [AI] State applicability, negative cases, contradictory evidence, uncertainty, and what would revise the lesson.
6. [HYBRID] Create/update Competitor Learning only when future work materially benefits. Deterministic helpers validate/persist rather than deciding semantic maturity or applicability.

## Verification
- Source usefulness is scoped by fact type/context.
- Visible activity/proxy performance is not promoted into effectiveness without supporting evidence.
- Learning does not encode monitoring scheduler state, routing thresholds, or deterministic semantic promotion.

## Completion Criteria
- Future competitor research can reuse a scoped evidence-backed lesson that improves judgment without inheriting a hidden monitoring or inference-control loop.
