---
id: core.action-control.delegate-work
type: service
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- ActionPacket
- Opportunity
writes:
- WorkRequest
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
# Delegate Work

## Purpose
Request another operating system to perform specialized execution without duplicating the originating Opportunity.

## Business Outcome
Use specialized production capability while preserving single Opportunity ownership and lineage.

## Run When
When an Action requires another OS semantic/production expertise.

## Do Not Run When
Do not delegate merely because another system exists; keep work local when the current OS owns and can execute it.

## Process
1. [AI] Confirm this is delegation rather than an independently valuable second intervention.
2. [AI] Specify purpose, required output, originating Opportunity/Action, constraints, success criteria, and context references.
3. [DETERMINISTIC] Resolve executing system and required capabilities/contracts.
4. [HYBRID] Define return contract, approval constraints, and deadline/priority when material.
5. [DETERMINISTIC] Persist WorkRequest and emit work.requested.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
