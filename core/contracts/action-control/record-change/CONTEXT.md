---
id: core.action-control.record-change
type: service
version: 2.0.0
owner_system: core
reads: []
writes:
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
# Record Material Change

## Purpose
Preserve a concise organization-owned record of a material change when future work benefits from knowing what changed, where, when, and with what evidence or result.

## Business Outcome
Retain useful operational history without forcing every mutation through an AURA authorization, ActionPacket, or verification lifecycle.

## Run When
Use this only when the change itself is durable organizational knowledge: for example a production configuration change, important published update, pricing change, campaign launch, account-setting change, or other state transition that future work may need to understand.

## Do Not Run When
- Do not create a ChangeEvent for every tool call or routine edit.
- Do not require an ActionPacket, Approval, Opportunity, or VerificationRecord before a change can be remembered.
- Do not use ChangeEvent as runtime execution machinery; the current harness/tool owns execution mechanics and receipts.

## Process
1. [AI] Decide whether remembering the change will materially improve future organizational continuity, troubleshooting, measurement, attribution, or decision-making.
2. [HYBRID] Record a clear summary, affected targets, when it occurred, and the executor/actor when known.
3. [HYBRID] Preserve before/after state, rollback information, evidence references, result references, related decisions, or related WorkRequests only when they are useful and actually known.
4. [DETERMINISTIC] Validate the persisted ChangeEvent and its references. Never invent a before-state, receipt, decision, verification, or result merely to make the record look complete.

## Verification
- Schema/reference integrity applies to the record itself.
- Independent change verification is required only when the selected SOP/task actually calls for it.

## Completion Criteria
- The record contains enough truthful information for future work to understand the material change without needing the original conversation or execution transcript.
