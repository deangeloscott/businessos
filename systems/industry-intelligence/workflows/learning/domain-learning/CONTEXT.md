---
id: industry.learning.domain-learning
type: workflow
owner_system: industry-intelligence
reads:
- OutcomeEvaluation
- Insight
- Learning
- MetricObservation
writes:
- Learning
---
# Industry Intelligence Learning

## Purpose
Turn repeated evidence about external-intelligence usefulness into scoped reusable guidance about what sources, event types, evidence patterns, and response approaches help this organization make better decisions.

## Business Outcome
Make future Industry Intelligence more relevant and efficient without converting outcomes into an internal alert/routing optimization system.

## Run When
Use when enough OutcomeEvaluations, corrections, misses, or repeated Industry work exists to support a reusable pattern. AURA does not run a background learning cycle merely because time passed.

## Process
1. [HYBRID] Review material and non-material findings, missed developments, corrections, decision timing, evidence quality, and how the resulting intelligence actually affected later business decisions or outcomes.
2. [AI] Identify source classes, evidence combinations, event/mechanism types, or research approaches that repeatedly proved useful or misleading in a defined context.
3. [AI] State the reusable pattern conditionally: where it applies, where it does not, what evidence supports it, contradictory cases, uncertainty, and what future evidence would revise it.
4. [AI] Capture context-specific relationships between external developments and customer/competitor/channel/business effects only at the scope the evidence supports; do not convert correlation into a universal rule.
5. [HYBRID] Create/update a Learning only when forgetting the pattern would materially reduce future quality or efficiency. Keep current IndustryEvent/Insight facts separate from reusable methodological guidance.

## Verification
- Learning scope does not exceed the supporting outcomes/evidence.
- Misses and negative cases are considered, not only successes.
- Source usefulness for one fact type/context is not treated as universal credibility.
- Learning does not encode alert thresholds, routing authority, scheduler state, or provider/runtime configuration.

## Completion Criteria
- A future model can use the Learning to do Industry Intelligence better in the applicable context without inheriting a hidden classifier, alert lifecycle, or orchestration rule.
