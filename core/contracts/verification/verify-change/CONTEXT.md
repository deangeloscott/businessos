---
id: core.verification.verify-change
type: service
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- ChangeEvent
- ActionPacket
writes:
- VerificationRecord
- ChangeEvent
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
# Verify Change

## Purpose
Independently determine whether intended external state exists and guardrails remain acceptable.

## Business Outcome
Prevent false success from tool responses and unsafe unintended changes.

## Run When
After a ChangeEvent reaches applied, or after manual evidence is returned.

## Do Not Run When
Do not substitute measurement of business outcome for implementation verification.

## Process
1. [HYBRID] Translate Action success criteria into explicit observable assertions.
2. [INTEGRATION] Re-read independent post-state through the best available capability or human evidence.
3. [DETERMINISTIC] Compare expected and observed state exactly where possible.
4. [HYBRID] Evaluate unintended effects and guardrails.
5. [HYBRID] Classify passed, partial, failed, or inconclusive and identify remediation/rollback if needed.
6. [DETERMINISTIC] Persist VerificationRecord, update ChangeEvent state, emit change.verified or verification.failed.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
