---
id: core.action-control.record-change
type: service
version: 1.8.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- ActionPacket
- Approval
writes:
- ChangeEvent
capabilities:
  required:
  - none
  optional:
  - business.action.governed.propose
  - business.action.governed.preview
  - business.action.governed.execute
  - business.action.receipt.read
events:
  consumes:
  - none
  emits:
  - core.object.updated
---
# Record Change Event

## Purpose
Record what external state was intentionally changed and how.

## Business Outcome
Preserve auditability, rollback, verification, and attribution.

## Run When
When an authorized Action mutates external business state.

## Do Not Run When
Do not create for read-only analysis.

## Process
1. [DETERMINISTIC] Capture target references, executor, action packet, approval, and intended change before mutation where practical.
2. [INTEGRATION] Execute or receive evidence of the authorized mutation through the assigned executor. When an available governed action surface supports the specific target action, use its proposal/preview/confirmation/execution semantics and preserve the provider/external-execution receipt; otherwise use the target-specific executor directly.
3. [DETERMINISTIC] Capture after-state/action response, receipt/effect status, and failure details without treating provider acceptance, delivery, or an execution receipt as independent verification of the later business outcome.
4. [HYBRID] Record rollback path/state where practical.
5. [DETERMINISTIC] Persist ChangeEvent and route to verification.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
