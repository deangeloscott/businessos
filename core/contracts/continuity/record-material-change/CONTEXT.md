---
id: core.continuity.record-material-change
type: playbook
owner_system: core
reads:
- Business
- DecisionRecord
- Asset
- SourceRecord
- WorkRequest
writes:
- ChangeEvent
capabilities:
  required:
  - none
  optional:
  - none
context:
- Business
---
# Record Material Change

## Purpose
Preserve meaningful organizational change history when remembering the change would improve future understanding, troubleshooting, measurement, or continuity.

## Business Outcome
Give future humans and AI a concise, evidence-aware record of important changes without turning ordinary execution into a universal mutation ceremony or runtime event log.

## Run When
Use this when a real organizational change occurred or was materially attempted and remembering it later would improve understanding, troubleshooting, measurement, or continuation. Do not create a `ChangeEvent` for every file edit, tool call, internal step, or transient runtime action.

## Process
1. [AI] Determine whether the change is materially worth remembering. Planned work belongs in the organizational object that describes the plan or work itself; a `ChangeEvent` records meaningful history, not a workflow state machine.
2. [HYBRID] Identify the organization subject or scope that materially changed and record a concise business-readable summary of what happened.
3. [HYBRID] Record when the change occurred and the actor when that information is useful and known; do not invent missing execution details.
4. [AI] Preserve before/after state, source evidence, decisions, work references, or result references only when they materially help explain the change later.
5. [AI] When useful, record the semantic outcome as `applied`, `partial`, `failed`, `rolled_back`, or `unknown`, matching what the evidence actually supports.
6. [HYBRID] If the change is later reversed or superseded, preserve the relationship or resulting state without rewriting the historical record.

## Verification
- The `ChangeEvent` corresponds to a real material change or material attempted change.
- Its claims are supported by the available organizational evidence at the level of certainty recorded.
- A `VerificationRecord` is created only when an actual check was performed and preserving that check materially improves organizational truth or continuity.
- A future need to check something is represented as attention, monitoring intent, or work rather than a pretend verification result.

## Boundary
This SOP does not authorize changes, control execution, prescribe tools, or require a ceremony around ordinary work. The human, model, and harness decide how work is executed; AURA preserves only the organizational meaning that remains useful afterward.

## Completion Criteria
A future capable actor can understand the material change, its relevant evidence or result, and any meaningful relationship to prior or subsequent organizational state without reconstructing runtime chatter.
