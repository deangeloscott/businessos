---
id: core.intelligence.publish-observation
type: service
owner_system: core
reads:
- SourceRecord
writes:
- Observation
capabilities:
  required:
  - none
  optional:
  - none
---
# Publish Observation

## Purpose
Capture a direct observation with source provenance without overstating interpretation or creating runtime event traffic.

## Business Outcome
Make material evidence reusable and traceable across organizational work.

## Run When
When a directly observed fact, event, statement, or measured condition has durable value beyond the current task.

## Do Not Run When
Do not create an Observation for transient tool output with no future value, or for interpretations that combine/explain evidence; use an Insight when durable interpretation is warranted.

## Process
1. [HYBRID] Confirm the statement is directly supported by the cited source rather than an inference.
2. [DETERMINISTIC] Create/resolve exact SourceRecord references and preserve retrieval time, access scope, and version/hash where useful.
3. [AI] Select the narrowest accurate observation type and subject references without adding causal or semantic claims not supported by evidence.
4. [DETERMINISTIC] Validate business isolation, required fields, and source references.
5. [DETERMINISTIC] Persist the Observation. Do not emit an AURA runtime event merely because durable evidence was saved.

## Verification
- The Observation is schema-valid and linked to the correct organization and real source evidence.
- Direct observation remains distinct from inference or recommendation.

## Failure / Fallback
- If the evidence cannot be inspected or supported, do not manufacture the Observation. Use another valid host method when available or preserve the unresolved evidence need honestly.

## Completion Criteria
- The material Observation is traceable to valid SourceRecord evidence and can be reused without reconstructing transient execution state.
