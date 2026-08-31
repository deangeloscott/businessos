---
id: core.action-control.return-work
type: service
version: 2.0.0
owner_system: core
reads:
- WorkRequest
- Asset
writes:
- WorkRequest
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
  - work.returned
---
# Return Delegated Work

## Purpose
Record the material result of a durable WorkRequest so future organizational work can continue from what actually happened.

## Business Outcome
Close the loop on a real handoff without requiring ActionPackets, approval state, runtime transcripts, or artificial verification objects.

## Run When
When work represented by a durable WorkRequest is completed, blocked, cancelled, or otherwise produces a material result worth preserving.

## Process
1. [AI] Compare the returned work with the WorkRequest's actual requested output and constraints. Judge quality using the relevant task/SOP requirements rather than generic handoff ceremony.
2. [HYBRID] Record material result references, unresolved issues, and a truthful status: completed, blocked, cancelled, or still in progress.
3. [DETERMINISTIC] Validate persisted references and business ownership. Do not fabricate a result reference merely to close the request.
4. [AI] Preserve genuinely new organizational evidence or observations when they will matter later. Do not store transient execution logs as business memory.
5. [DETERMINISTIC] Update the WorkRequest and emit `work.returned` when the return is materially useful to downstream continuity.

## Verification
- The WorkRequest truthfully reflects what came back and its current status.
- Any persisted result/evidence objects validate independently.

## Completion Criteria
- Future work can discover the requested work, its material result, and any unresolved next step from organization-owned state.
