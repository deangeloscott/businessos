# Monitoring Continuity

AURA owns durable **monitoring intent**, not the machinery that makes future executions happen.

## Core rule

AURA may remember what should be monitored, why it matters, a useful cadence, material-change signals, notification intent, prior checks, meaningful findings, and when another check would become useful. The active harness/runtime owns scheduling, reminders, background workers, webhooks, polling, retries, and notification delivery.

A `SourceProfile` cadence or `next_check_at` is therefore organizational intent. It is never proof that a task has been scheduled or will run automatically.

## Cadence and scope

- User-specified cadence beats inferred cadence.
- Cadence may differ by subject, source, or signal.
- Infer a starting cadence only when durable monitoring is clearly requested and it helps future work.
- Prefer the slowest cadence that remains decision-useful.
- A refreshable baseline is not automatically a request for background scheduling.
- Pausing or stopping a watch should not erase evidence or Learning already earned.

## Notification intent

Monitoring frequency and notification frequency are different. Default to **material changes only** unless the user asks for a different behavior.

Supported semantic preferences are:
- `material_changes_only` — default;
- `due_and_material_changes`;
- `all_checks`;
- `silent`.

These values describe what the organization/user wants surfaced. Actual delivery remains a runtime responsibility.

## Due state

`next_check_at` may be used as a durable cue that another check is useful by/after a point in time. `scripts/list_due_monitoring.py` and `scripts/monitoring_status.py` summarize this semantic state. They do not inspect or certify external scheduler state.

When a current task makes overdue monitoring relevant, the active model may refresh it. Do not interrupt unrelated work merely to clear a backlog.

## Scheduling requests

If a user asks the current harness to schedule recurring work, the harness may use its own scheduler or another external runtime. AURA may preserve the monitoring intent and meaningful results, but it should not duplicate the scheduler receipt/state as canonical organizational truth.

Only the current runtime can truthfully say whether a schedule is active. AURA itself should say only what it knows: the monitoring intent and last/next useful check state.

## User experience

A capable model should be able to answer ordinary questions such as:
- "What are we monitoring?"
- "What changed since the last check?"
- "What is due for another look?"
- "Make pricing monthly but hiring weekly."
- "Only tell me when something materially changes."
- "Pause this watch but keep what we learned."

Continuity should reduce forgotten organizational work without turning AURA into a scheduler or notification service.
