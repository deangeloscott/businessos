---
id: core.coordination.create-initiative
type: playbook
owner_system: core
reads:
- Opportunity
writes:
- Initiative
capabilities:
  required:
  - none
  optional:
  - none
context:
- Objective
---
# Create Initiative

## Purpose
Preserve one durable coordination record when several genuinely distinct Opportunities need to be understood or managed together toward a shared business outcome.

## Business Outcome
Let future work see the shared objective, dependencies, sequencing, and combined measurement context without merging the underlying Opportunities or turning AURA into an orchestrator.

## Run When
Use when multiple independently meaningful Opportunities share enough dependencies, resources, timing, or combined outcome logic that forgetting their coordination would materially hurt future work.

## Do Not Run When
Do not create an Initiative for one Opportunity, ordinary model decomposition, subagent/tool delegation, or a short-lived sequence that does not need durable organizational memory.

## Process
1. [AI] Confirm each included Opportunity is independently meaningful organizational state rather than a runtime task fragment.
2. [AI] Define the shared Objective/outcome and why remembering the coordination adds value.
3. [AI] Record material dependencies, sequencing, milestones, shared constraints, conflicts, or ownership relationships only where they affect future organizational work.
4. [AI] Define combined measurement/evaluation context when it is actually useful, avoiding double counting of underlying Opportunity effects.
5. [DETERMINISTIC] Persist the Initiative and exact canonical references after the model/user has supplied the semantic content.

## Verification
- Referenced Opportunities exist, belong to the same organization, and remain separately inspectable.
- The Initiative adds real durable coordination meaning rather than mirroring runtime execution mechanics.
- No event, permission object, scheduler state, or artificial handoff is created merely because the Initiative exists.

## Failure / Fallback
- If coordination does not need to survive the current work, do not create an Initiative.
- If an unresolved dependency is materially worth remembering, preserve it in the Initiative or another genuinely appropriate durable object; do not manufacture a runtime action object.

## Completion Criteria
- Future organizational work can understand the shared outcome and the material relationships among the included Opportunities without reconstructing them from a prior conversation or execution log.
