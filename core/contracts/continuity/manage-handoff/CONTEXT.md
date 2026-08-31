---
name: Manage Durable Handoff
id: core.continuity.manage-handoff
version: 1.0.0
owner_system: core
stakeholders:
- Business
- WorkRequest
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
input_contract:
- Business context
- Work whose continuity across actors or time would materially help
output_contract:
- A concise durable handoff with enough context to understand the objective, constraints, acceptance checks, inputs, status, and material results later
capabilities: []
events:
  consumes:
  - none
  emits:
  - none
---

# Purpose

Preserve a useful organizational handoff when work needs to survive across people, models, sessions, or time. A `WorkRequest` is organizational memory for coordination, not execution authority.

# When to use

Use this only when a durable handoff materially improves continuity. If one capable actor can simply do the work and nothing important would be lost later, do the work directly and do not create a `WorkRequest`.

# Method

1. Record the objective in business language.
2. Preserve only constraints and inputs that materially affect the work.
3. State acceptance checks that make the intended result understandable.
4. Keep the same `WorkRequest` current as the durable handoff moves through `queued`, `in_progress`, `blocked`, `completed`, or `cancelled`.
5. When completed, link the material deliverables or results worth finding later.
6. When blocked, preserve only blocker context that another capable actor would need to continue intelligently.
7. Use an `AttentionItem` only when a material unresolved condition genuinely deserves organizational attention.

# Boundary

Do not create `WorkRequest` objects for internal subagents, tool calls, provider selection, retries, concurrency, or other runtime mechanics. The active human, model, and harness decide how to perform the work.

Do not use this SOP as a gate before work can begin. Its value is continuity, not permission or orchestration.

# Completion

The handoff is complete when its durable state accurately reflects what another capable actor would need to understand what was requested, what materially happened, and what—if anything—remains.