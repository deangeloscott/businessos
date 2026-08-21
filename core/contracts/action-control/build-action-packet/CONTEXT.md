---
id: core.action-control.build-action-packet
type: service
version: 1.8.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Opportunity
- Initiative
- CapabilityBinding
writes:
- ActionPacket
capabilities:
  required:
  - none
  optional:
  - business.action.governed.propose
  - business.action.governed.preview
events:
  consumes:
  - none
  emits:
  - core.object.updated
---
# Build Action Packet

## Purpose
Convert a committed Opportunity into explicit executable Actions.

## Business Outcome
Make business intent executable without losing why each action exists.

## Run When
When an Opportunity is committed or an authorized Incident requires action.

## Do Not Run When
Do not create an ActionPacket merely to record research with no external/operational action.

## Process
1. [AI] Decompose the intervention into the minimum complete ordered Actions.
2. [HYBRID] Assign the correct executor type to each Action; use deterministic/integration work where reasoning is unnecessary.
3. [DETERMINISTIC] Resolve required/optional capabilities and identify unavailable actions.
4. [HYBRID] Define inputs, expected outputs, dependencies, success criteria, risk, reversibility, autonomy ceiling, approvals, verification, and fallback for every material Action. When a governed action broker/provider is available, mark eligible Actions for proposal/preview handoff without assuming the generic handoff can execute the target-specific mutation.
5. [HYBRID] Convert unavailable automated actions into human-executable work rather than removing them.
6. [DETERMINISTIC] Validate action graph for missing dependencies/cycles and persist.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
