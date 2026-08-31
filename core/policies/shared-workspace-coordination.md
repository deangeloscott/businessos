# Shared Workspace Coordination

BusinessOS is shared durable operating state, not an agent runtime. One model, sequential models, harness-managed subagents, or different compatible harnesses may operate against the same business instance when they preserve canonical state and Run provenance.

## Runtime boundary

The harness/runtime owns model selection, worker spawning, scheduling, retries, parallelism, process supervision, delivery channels, and its own private/session memory mechanisms. BusinessOS owns durable organizational context, operational knowledge, evidence, ownership, authorization state, material work history, durable handoffs, validation, and state transitions.

A WorkRequest is a durable delegation/coordination object; it does not require BusinessOS itself to spawn another agent. A harness may execute the WorkRequest in the same model/session, a later session, or another authorized worker.

## Model and harness memory boundary

A model context window, conversation history, harness memory, Skill state, scratchpad, or provider-specific memory can be useful execution context. Use it when available; AURA should not force the model to reload or duplicate information it already has merely to prove that AURA was consulted.

Those memories are not the organization's portable source of continuity. Material business facts, evidence, preferences, decisions, outputs, outcomes, unresolved work, and Learning that another authorized worker may need should be preserved in AURA at the appropriate durable level. Do not persist transcripts, hidden chain-of-thought, every temporary hypothesis, or every tool interaction merely because they existed in the current model context.

When current model/harness memory conflicts with current grounded AURA organizational state, do not silently let stale private memory overwrite the durable record. Resolve the conflict from current explicit user/organization information and evidence, then update durable organizational state when appropriate. Likewise, new explicit information in the current interaction may supersede stale AURA state; AURA is durable memory, not immutable memory.

The practical rule is: use host memory as working memory, use AURA as organization-owned memory, and preserve only the material meaning needed for future work.

## Operator attribution

Runs may record stable `operator_ref`, `team_ref`, and `role_ref` values. These are attribution/context labels and do not by themselves grant authority. `BUSINESSOS_OPERATOR_REF`, `BUSINESSOS_TEAM_REF`, and `BUSINESSOS_ROLE_REF` may provide workspace/session defaults; explicit Run arguments win.

## Multi-session behavior

Sequential shared-state use is supported: later sessions should inspect and resume valid canonical/Run state rather than depending on another conversation's private memory.

BusinessOS does **not** currently claim that arbitrary simultaneous independent writes to the same canonical object are conflict-safe. Without a concurrency-safe mutation primitive for the target state, serialize conflicting writes or allocate distinct work. Do not assume that last-writer-wins, a filesystem write, or a model's belief that it is the only worker provides safe coordination.

Potential concurrent-writer controls such as atomic claiming, leases, expected-version/compare-and-swap guards, idempotency keys, or file locking should be introduced only as shared BusinessOS primitives when validated need justifies them. Do not build harness-specific worker pools or schedulers into BusinessOS merely to obtain parallel execution.
