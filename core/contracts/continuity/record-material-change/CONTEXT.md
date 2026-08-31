---
name: Record Material Change
id: core.continuity.record-material-change
version: 1.0.0
owner_system: core
stakeholders:
- Business
- ChangeEvent
reads:
- Business
- DecisionRecord
- Asset
- SourceRecord
- WorkRequest
writes:
- ChangeEvent
input_contract:
- Business context
- A real organizational change whose history would materially help later understanding, troubleshooting, measurement, or continuation
output_contract:
- A concise ChangeEvent describing what materially changed, when, where, and the evidence or results worth preserving
capabilities: []
events:
  consumes:
  - none
  emits:
  - none
---

# Purpose

Preserve meaningful organizational change history when remembering the change would improve future understanding, troubleshooting, measurement, or continuity.

# When to use

Create a `ChangeEvent` only for a material change that actually happened or was materially attempted. Do not create one for every file edit, tool call, internal step, or transient runtime action.

Planned work belongs in the organizational object that describes the plan or work itself, such as a `WorkRequest`, `Initiative`, or `DecisionRecord`. A `ChangeEvent` is history, not a workflow state machine.

# Method

1. Identify the organization subject or scope that materially changed.
2. Record a concise business-readable summary of the change.
3. Record when it occurred and the actor when that information is useful and known.
4. Preserve before/after state, source evidence, decisions, work references, or result references only when they help explain the change later.
5. If useful, record the semantic outcome as `applied`, `partial`, `failed`, `rolled_back`, or `unknown`.
6. If the change is later reversed, preserve the rollback relationship or resulting state without rewriting history.

# Verification

A `VerificationRecord` is optional. Create one only when an actual check is performed and preserving the check materially improves organizational truth or continuity. A future need to check something belongs in attention, monitoring intent, or work—not in a pretend verification result.

# Boundary

This SOP does not authorize changes, control execution, prescribe tools, or require a ceremony around ordinary work. The human, model, and harness decide how work is executed; AURA preserves the organizational meaning that remains useful afterward.

# Completion

The record is complete when a future capable actor can understand the material change and its useful evidence or outcome without reconstructing runtime chatter.