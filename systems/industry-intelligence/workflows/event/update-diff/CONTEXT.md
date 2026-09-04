---
id: industry.event.update-diff
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- IndustryEvent
- Observation
- Insight
context:
- Business
- Market
- Objective
---
# Industry Event Update Diff

## Purpose
Identify what materially changed since the last verified real-world IndustryEvent state without treating repeated coverage as new intelligence or emitting AURA runtime events.

## Business Outcome
Keep external-event understanding current while focusing attention on genuinely new facts, corrections, and status changes.

## Run When
When an existing IndustryEvent receives new evidence that may alter the current understanding.

## Process
1. [DETERMINISTIC] Load the prior persisted event state, timeline, and exact new evidence references.
2. [AI] Classify each new evidence item as duplicate/republication, clarification, correction, new fact, status change, scope change, effective-date change, consequence, commentary, or another evidence-supported category.
3. [AI] Identify which prior factual claims are now outdated, contradicted, superseded, or simply more precisely stated.
4. [DETERMINISTIC] Preserve prior versions and source refs; do not erase historical state that remains useful for understanding the change.
5. [AI] State the material delta in the smallest precise form supported by evidence.
6. [AI] Reassess materiality/business impact only when the delta could change a decision or prior durable Insight; do not automatically trigger another workflow.
7. [HYBRID] Update the IndustryEvent status/timeline and any useful next-review date from the resolved semantic delta. Persist an Observation/Insight only when the new evidence or interpretation has durable value. Do not emit an AURA runtime event merely because the external event changed.

## Verification
- The new state is traceable to evidence and the prior state remains inspectable when history matters.
- Repeated reporting without a material delta does not create artificial change.
- Semantic change classification remains a model/user judgment; deterministic helpers preserve exact references/state.

## Completion Criteria
- Future work can tell what actually changed in the real-world event, what did not, and why that distinction is supported without a separate internal event stream.
