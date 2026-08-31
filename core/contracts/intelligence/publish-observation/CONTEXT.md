---
id: core.intelligence.publish-observation
type: service
version: 1.1.0
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
events:
  consumes:
  - none
  emits:
  - core.object.updated
---
# Publish Observation

## Purpose
Capture a direct observation with source provenance without overstating interpretation.

## Business Outcome
Make new evidence reusable and traceable across systems.

## Run When
When any system directly observes a decision-relevant fact, event, statement, or measured condition.

## Do Not Run When
Do not use for interpretations that combine or explain evidence; create/update an Insight instead.

## Process
1. [HYBRID] Confirm the statement is directly supported by the cited source rather than an inference.
2. [DETERMINISTIC] Create/resolve SourceRecord references and preserve retrieval time, access scope, and version/hash where useful.
3. [AI] Select the narrowest accurate observation type and subject references without adding causal language not present in evidence.
4. [DETERMINISTIC] Validate business isolation, required fields, and source references.
5. [DETERMINISTIC] Persist the Observation and emit observation.created.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- The Observation can be traced to at least one valid SourceRecord.
