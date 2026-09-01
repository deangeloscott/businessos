# Shared Workspace Coordination

AURA is shared durable organizational memory and operating knowledge, not an agent runtime. One model, sequential models, harness-managed subagents, or different compatible harnesses may operate against the same business instance when they preserve canonical truth, useful provenance, business isolation, and durable continuity.

## Runtime boundary

The harness/runtime owns model selection, worker spawning, scheduling, retries, parallelism, process supervision, delivery channels, credentials, permissions, and its own private/session memory mechanisms. AURA owns durable organizational context, operational knowledge, evidence/provenance, preferences, decisions, material work history, durable handoffs, Learning, validation, and the integrity of persisted organizational state.

A `WorkRequest` is optional durable coordination memory. It does not require AURA itself to spawn another agent or act as an execution queue. A harness may perform the work in the same model/session, a later session, or another capable worker.

## Model and harness memory boundary

A model context window, conversation history, harness memory, Skill state, scratchpad, or provider-specific memory can be useful execution context. Use it when available; AURA should not force the model to reload or duplicate information it already has merely to prove that AURA was consulted.

Those memories are not the organization's portable source of continuity. Material business facts, evidence, preferences, decisions, outputs, outcomes, unresolved work, and Learning that future work may benefit from should be preserved in AURA at the appropriate durable level. Do not persist transcripts, hidden chain-of-thought, every temporary hypothesis, or every tool interaction merely because they existed in the current model context.

When current model/harness memory conflicts with current grounded AURA organizational state, do not silently let stale private memory overwrite the durable record. Resolve the conflict from current explicit user/organization information and evidence, then update durable organizational state when appropriate. Likewise, new explicit information in the current interaction may supersede stale AURA state; AURA is durable memory, not immutable memory.

The practical rule is: use host memory as working memory, use AURA as organization-owned memory, and preserve only the material meaning needed for future work.

## Operator attribution

Optional work receipts may record stable `operator_ref`, `team_ref`, and `role_ref` values when attribution or scoped preferences materially help continuity. These are context labels, not permissions or execution authority. `BUSINESSOS_OPERATOR_REF`, `BUSINESSOS_TEAM_REF`, and `BUSINESSOS_ROLE_REF` may provide workspace/session defaults; explicit arguments win where a helper accepts them.

## Multi-session behavior

Sequential shared-state use is supported: later sessions should inspect current canonical state and any relevant durable handoffs or work receipts rather than depending on another conversation's private memory.

AURA does **not** currently claim that arbitrary simultaneous independent writes to the same canonical object are conflict-safe. Without a concurrency-safe mutation primitive for the target state, serialize conflicting writes or allocate distinct work. Do not assume that last-writer-wins, a filesystem write, or a model's belief that it is the only worker provides safe coordination.

Potential concurrent-writer controls such as atomic claiming, leases, expected-version/compare-and-swap guards, idempotency keys, or file locking should be introduced only as shared AURA integrity primitives when validated need justifies them. Do not build harness-specific worker pools or schedulers into AURA merely to obtain parallel execution.
