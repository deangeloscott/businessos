---
id: core.action-control.return-work
type: playbook
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- WorkRequest
- Asset
- VerificationRecord
- ActionPacket
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
Complete a WorkRequest by returning valid outputs and execution evidence to the originating system without transferring Opportunity ownership.

## Business Outcome
Return delegated work with complete lineage, status, outputs, and unresolved dependencies so the originating Opportunity can continue cleanly.
## Run When
When the executing system finishes or cannot finish delegated work.

## Process
1. [DETERMINISTIC] Confirm returned outputs correspond to the WorkRequest success criteria and active business.
2. [HYBRID] Record output references, execution/QA evidence, deviations, unresolved constraints, and whether the request is completed, partial, blocked, or failed.
3. [DETERMINISTIC] Validate returned canonical objects and lineage to the originating WorkRequest.
4. [AI] Identify any newly discovered independent domain Opportunity separately; do not hide it inside the delegated return.
5. [DETERMINISTIC] Update WorkRequest status and emit work.returned.
6. [HYBRID] Originating system retains responsibility for final domain verification/Opportunity outcome.
