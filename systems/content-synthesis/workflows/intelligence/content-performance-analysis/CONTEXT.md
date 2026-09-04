---
id: content.intelligence.content-performance-analysis
type: workflow
owner_system: content-synthesis
reads:
- Asset
- MetricObservation
- OutcomeEvaluation
- Insight
- Learning
- PlatformProfile
writes:
- Observation
- Insight
- Learning
context:
- AudienceSegment
- Objective
---
# Content Performance Pattern Analysis

## Purpose
Learn which topics, formats, hooks, structures, depths, and creative mechanisms work for this business while separating content quality from distribution and commercial effects.

## Business Outcome
Improve future content decisions using observed business-specific performance rather than platform folklore or isolated winners.

## Run When
Run after enough comparable content performance accumulates, after a meaningful content experiment, or when an existing Content Learning needs reevaluation.

## Process
1. [DETERMINISTIC] Define comparable Assets by platform, audience, objective, format, time period, distribution conditions, and measurement window; exclude incomparable items or mark limitations.
2. [INTEGRATION] Retrieve content metrics and relevant OutcomeEvaluations, preserving metric definitions and whether reach was organic, paid, boosted, partner-driven, or unknown.
3. [AI] Distinguish attention, consumption, engagement, audience quality, downstream action, and commercial contribution instead of using one metric as universal success.
4. [DETERMINISTIC] Compare performance against each Asset's appropriate baseline and group-level distribution, not only absolute winner counts.
5. [AI] Identify recurring topic/format/hook/structure/proof/pacing patterns and generate alternative explanations involving distribution, timing, audience size, external events, or offer differences.
6. [HYBRID] Test candidate patterns against counterexamples, different audiences, and existing Content Learning; narrow applicability rather than forcing a broad rule.
7. [HYBRID] Publish Content Insights and promote/update Learning only when evidence supports reusable future guidance; preserve causal uncertainty.
