---
id: core.action-control.delegate-work
type: service
version: 2.0.0
owner_system: core
reads: []
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
Create a durable organizational handoff only when future continuity benefits from recording that one person, team, system, or workstream is responsible for returning a bounded result.

## Business Outcome
Coordinate real work without turning model subagents, tool calls, or internal routing into organizational bureaucracy.

## Run When
Use this only when a durable handoff materially helps the organization remember what was requested, why it matters, who or what owns the return, and what result came back.

## Do Not Run When
- Do not create a WorkRequest merely because the current model invokes a subagent, tool, provider, or another internal execution mechanism.
- Do not require an Opportunity or ActionPacket before work can be delegated.
- Do not persist routine ephemeral coordination that the current harness can complete inside the same work session.

## Process
1. [AI] Decide whether a durable organizational handoff is actually useful. Prefer direct execution when the current worker/harness can complete the work without losing continuity.
2. [AI] Define the smallest useful handoff: purpose, requested output, relevant context references, real constraints, and an assignee/owner only when one is actually known.
3. [AI] Add a due date only when a real deadline exists. Do not manufacture timing, priority, capability requirements, or a return protocol for bookkeeping.
4. [DETERMINISTIC] Persist one WorkRequest when the handoff should survive the current session. The runtime/harness remains responsible for tools, subagents, retries, concurrency, and current capability resolution.
5. [HYBRID] If progress is materially blocked and future organizational attention would help, create or update one deduplicated AttentionItem describing the real unresolved condition.

## Verification
- Validate any persisted WorkRequest or AttentionItem against its schema.
- Preserve references to material organizational context/results rather than execution transcripts.

## Completion Criteria
- The organization can understand what work was handed off and what result is expected without needing the originating conversation.
- No WorkRequest was created solely to mirror runtime orchestration.
