---
id: core.coordination.create-initiative
type: playbook
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Opportunity
writes:
- Initiative
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
context:
- Objective
---
# Create Initiative

## Purpose
Coordinate genuinely distinct domain Opportunities toward one shared business outcome.

## Business Outcome
Enable sequencing and combined evaluation without merging domain ownership.

## Run When
When multiple independently valid Opportunities must be coordinated because sequencing, shared resources, claims, or combined outcome matter.

## Do Not Run When
Do not create an Initiative for simple delegated work or a single Opportunity.

## Process
1. [AI] Confirm each included Opportunity represents a distinct intervention with its own owner.
2. [AI] Define the shared objective and why coordination is necessary.
3. [HYBRID] Map dependencies, sequencing, milestones, shared constraints, and conflicts.
4. [HYBRID] Define combined business case and Initiative-level success metrics without double counting Opportunity effects.
5. [DETERMINISTIC] Create Initiative references; do not change domain ownership.
6. [DETERMINISTIC] Emit initiative.created.

## Verification
- Validate written objects against their schemas and preserve source/lineage references.

## Failure / Fallback
- If a required capability is unavailable, create a human-executable Manual Action Packet for the missing step; do not silently omit required work.
- If evidence is insufficient, record the unresolved knowledge gap and avoid overstating confidence.

## Completion Criteria
- Required outputs exist and validate.
- Material uncertainty, contradictions, and unresolved dependencies are explicit.
- Any required next route is represented by a canonical reference or event rather than an informal note.
