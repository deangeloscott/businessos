---
id: core.intelligence.manage-insight
type: workflow
owner_system: core
reads:
- Observation
- Insight
writes:
- Insight
context:
- AudienceSegment
- Market
- Objective
- Offer
---
# Manage Insight

## Purpose
Create, strengthen, narrow, contradict, supersede, or retire an evidence-supported interpretation without turning Insight lifecycle into runtime orchestration.

## Business Outcome
Maintain reusable organization-owned interpretation instead of repeated reports or duplicated conclusions.

## Run When
When evidence justifies preserving what observations mean for future organizational work.

## Do Not Run When
Do not create an Insight when the statement is merely a direct observation, an unevidenced recommendation, or transient reasoning with no durable value.

## Process
1. [AI] Retrieve potentially overlapping current Insights using available indexes/cues. The capable model/user decides semantic equivalence; deterministic AURA must not merge conclusions from lexical overlap alone.
2. [AI] Define the exact statement, relevant scope/subjects, applicability, and decision relevance at the level the evidence supports.
3. [HYBRID] Attach supporting and contradictory evidence links with reasons; do not suppress disconfirming evidence.
4. [HYBRID] Assess confidence using evidence directness, source authority for the fact type, agreement, sample coverage, freshness, and causal ambiguity.
5. [AI] Decide whether to create, strengthen, narrow, contradict, supersede, or retire the Insight based on current evidence and future usefulness.
6. [DETERMINISTIC] Validate business isolation, evidence references, allowed state shape, and persist the chosen durable interpretation. Do not emit an AURA runtime event merely because an Insight changed.

## Verification
- The Insight is schema-valid, evidence-linked, scoped to what the evidence supports, and stored for the correct organization.
- Semantic identity and interpretation remain model/user judgments rather than deterministic text matching.

## Failure / Fallback
- If evidence is insufficient, preserve the uncertainty or unresolved evidence need instead of forcing a durable conclusion.

## Completion Criteria
- A future capable reader can tell what is believed, why, where it applies, what contradicts it, and how certain the evidence supports being.
