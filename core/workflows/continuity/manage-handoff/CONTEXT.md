---
id: core.continuity.manage-handoff
type: workflow
owner_system: core
reads:
- Business
- WorkRequest
- AttentionItem
- Asset
- Observation
writes:
- WorkRequest
- AttentionItem
- Asset
- Observation
context:
- Business
---
# Manage Durable Handoff

## Purpose
Preserve a useful organizational handoff when work needs to survive across people, models, sessions, or time. A `WorkRequest` is organizational memory for coordination, not execution authority.

## Business Outcome
Let another capable actor continue important work without reconstructing the objective, material context, current state, constraints, or useful results from runtime chatter.

## Run When
Use this only when a durable handoff materially improves continuity. If one capable actor can simply do the work and nothing important would be lost later, do the work directly and do not create a `WorkRequest`.

## Process
1. [AI] Decide whether the work genuinely benefits from durable cross-actor or cross-session continuity. Do not create a `WorkRequest` merely because tools, subagents, retries, or multiple internal steps are involved.
2. [HYBRID] Record the objective in business language together with only the constraints, material inputs, and acceptance checks another capable actor would need.
3. [AI] Preserve links to relevant evidence, observations, assets, prior decisions, or other durable organization state rather than copying transient execution detail into the handoff.
4. [HYBRID] Keep the same `WorkRequest` current as the durable handoff moves through `open`, `in_progress`, `blocked`, `completed`, or `cancelled`; the status describes organizational continuity, not permission to act.
5. [HYBRID] When completed, link the material deliverables or results worth finding later. When blocked, preserve only blocker context needed to continue intelligently.
6. [AI] Create or retain an `AttentionItem` only when a material unresolved condition genuinely deserves organizational attention beyond the current work.

## Verification
- The handoff corresponds to real work whose continuity matters.
- A future capable actor can understand what is being pursued, what materially happened, and what remains without reading tool logs or hidden reasoning.
- The record does not encode provider selection, orchestration, retries, concurrency, permission tiers, or other runtime mechanics as organizational state.

## Boundary
Do not create `WorkRequest` objects for internal subagents, tool calls, provider selection, retries, concurrency, or other runtime mechanics. The active human, model, and harness decide how to perform the work.

Do not use this Workflow as a gate before work can begin. Its value is continuity, not permission or orchestration.

## Completion Criteria
The durable handoff accurately reflects what another capable actor would need to understand the objective, relevant context, material status/results, and any unresolved next work worth carrying forward.
