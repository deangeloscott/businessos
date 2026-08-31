---
id: core.intelligence.manage-insight
type: service
version: 1.1.0
owner_system: core
reads:
- Observation
- Insight
writes:
- Insight
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - insight.activated
  - insight.updated
  - insight.contradicted
context:
- AudienceSegment
- Market
- Objective
- Offer
---
# Manage Insight

## Purpose
Create, strengthen, narrow, contradict, supersede, or archive an evidence-supported interpretation.

## Business Outcome
Maintain one reusable canonical interpretation instead of repeated reports.

## Run When
When evidence justifies interpreting what observations mean inside a semantic domain.

## Do Not Run When
Do not create an Insight when the statement is merely a direct observation or an unevidenced recommendation.

## Process
1. [AI] Search active Insights for semantic overlap before creating a new one.
2. [AI] Define the exact statement, semantic owner, subjects, scope, and decision relevance.
3. [HYBRID] Attach supporting and contradictory evidence links with reasons; do not suppress disconfirming evidence.
4. [HYBRID] Assess confidence using evidence directness, source authority for the fact type, agreement, sample coverage, freshness, and causal ambiguity.
5. [AI] Decide whether to create, strengthen, narrow, contradict, supersede, or archive the Insight.
6. [DETERMINISTIC] Validate owner, business isolation, evidence references, lifecycle transition, and persist.
7. [DETERMINISTIC] Emit insight.activated/updated/contradicted when material.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- A downstream reader can answer what is believed, why, for whom/where it applies, and how confident the system is.
