---
id: customer.research.plan
type: workflow
owner_system: customer-intelligence
reads:
- Insight
- SourceRecord
- Observation
writes: []
context:
- AudienceSegment
- Objective
---
# Customer Research Plan

## Purpose
Turn a business decision, uncertainty, or customer hypothesis into a bounded evidence plan.

## Business Outcome
Collect the minimum sufficient customer evidence needed to make the target decision with known confidence and coverage limits.

## Run When
Run before material customer research when the question, population, evidence needs, or stopping rule is not already explicit.

## Process
1. [AI] State the decision to support, the exact customer question, current hypothesis, and what would change the decision.
2. [AI] Define the relevant population, segments, journey stage, geography, time window, and exclusions.
3. [AI] List the evidence types that can directly answer the question and distinguish first-party, behavioral, and public evidence.
4. [HYBRID] Identify likely biases, missing perspectives, privacy constraints, and evidence that could contradict the working hypothesis.
5. [AI] Select collection methods and sequence them from highest-value existing evidence to new research only where needed.
6. [AI] Define coverage targets, evidence-quality checks, stopping conditions, freshness requirements, and useful outputs proportionate to the decision.
7. [AI] Return the bounded evidence plan. The active model/harness may collect the evidence directly with its available tools; create a `WorkRequest` only when a real durable handoff to another person/team/session must survive beyond the current interaction, not merely because research remains to be done.

## Completion Criteria
- The decision, population, evidence needs, quality checks, stopping rule, and material gaps are explicit enough for the active model/harness or a genuine future handoff to continue without inventing orchestration state.
