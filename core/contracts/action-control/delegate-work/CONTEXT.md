---
id: core.action-control.delegate-work
type: service
version: 1.2.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- ActionPacket
- Opportunity
writes:
- WorkRequest
- AttentionItem
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
Do not delegate merely because another system/subagent exists; keep work local when the current OS owns and can execute it. Do not use delegation as a default response to uncertainty, and do not recursively re-delegate after timeout/failure without first reassessing whether the extra work can still change the outcome.

## Process
1. [AI] Confirm this is delegation rather than an independently valuable second intervention, and that specialization/parallelism is reasonably expected to improve quality or reduce total work/elapsed time versus keeping the task local.
2. [AI] Specify one bounded purpose, required output, originating Opportunity/Action, constraints, success criteria, and context references. Avoid broad multi-domain "research everything" requests.
3. [DETERMINISTIC] Resolve executing system and required capabilities/contracts.
4. [HYBRID] Define return contract, approval constraints, and deadline/priority when material.
5. [DETERMINISTIC] Persist WorkRequest and emit work.requested.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; when user/harness action is actually required, create/update one deduplicated AttentionItem. Do not silently omit required work or create repeated notifications for the same blocker.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.
- If delegated work times out/fails, preserve any usable partial evidence, return the blocker, and reassess value-of-information before retrying. Repeated provider failure is not a reason to multiply subagents.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
