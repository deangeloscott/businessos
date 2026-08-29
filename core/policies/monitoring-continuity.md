# Monitoring Continuity

AURA may decide that information should be refreshed on a cadence, but a semantic cadence is not the same thing as an active background schedule. Preserve that distinction everywhere.

## Core rule

AURA owns **what should be monitored, why, how often, and what counts as material**. The host/harness/operating system/workflow provider owns the machinery that causes a future execution to occur.

Never say a monitor is "scheduled", "active", or "will run" merely because a `SourceProfile` has `next_check_at` or a recurring cadence. Those fields express organization-owned monitoring intent. Automatic execution is true only when a current environment scheduler binding has been created and verified.

## Cadence

- Infer a reasonable starting cadence when durable monitoring is clearly requested and the user did not specify one. Base it on expected rate of change, business consequence, source volatility, and decision value.
- User-specified cadence wins over inferred cadence. Do not silently replace an explicit user cadence with a generic default.
- Cadence may differ by subject, source/surface, or signal. A competitor's pricing page may be monthly while hiring/news is weekly; a fast regulatory issue may justify daily checks while a creator baseline is monthly.
- Prefer the slowest cadence that is still decision-useful. Do not create continuous polling merely because it is possible.
- A request to build a refreshable baseline is not automatically a request for background scheduling. A request such as "keep an eye on this", "monitor this", or an explicit recurring interval may authorize recurring monitoring within the user's stated scope, but installing software, connecting accounts, spending money, or creating privileged system persistence still follows the applicable authorization boundary.

## Execution states

Treat monitoring continuity as one of these user-understandable states:

1. **Active automatic** — a verified scheduler binding exists in the current environment.
2. **Reminder-only** — a verified binding can surface that work is due but cannot autonomously run the required AI/business work.
3. **Due-on-next-start** — AURA has durable cadence/checkpoint state but no verified scheduler binding; the next AURA entry should surface overdue work and refresh it when relevant/authorized.
4. **Manual** — no automatic executor is available or desired; the user can ask AURA to refresh at any time.
5. **Paused/blocked** — the semantic watch remains durable but execution is intentionally paused or lacks a required dependency.

A scheduler binding belongs in the workspace environment overlay, not canonical business truth, because it is host-specific and regenerable. The monitoring intent/cadence remains durable organization state.

## Fallback ladder

When recurring monitoring is useful:

1. use an already-authorized harness-native scheduler when available;
2. otherwise use an appropriate authorized OS/workflow scheduler when the environment exposes one and a compatible worker can actually run the check;
3. otherwise use a reminder-only scheduler if available;
4. otherwise preserve `next_check_at` and surface overdue monitoring on the next AURA start;
5. manual refresh always remains valid.

Missing background automation changes the executor, not the monitoring plan. Do not fabricate completion or silently drop future work.

## Scheduler binding truth

- Store non-secret scheduler receipts/refs in `.businessos/environments/<environment>/scheduler-bindings.json` through the supported helper.
- An `active` binding must identify the target, actual executor, cadence, and a verification time/reference.
- Re-check a binding after a host change, migration, tool failure, or material schedule edit.
- A moved/copied workspace may preserve semantic monitoring state while its old scheduler binding becomes invalid; regenerate environment bindings rather than treating them as portable truth.
- If a schedule cannot be proven active, describe it as **planned/unbound**, not scheduled.

## On-start continuity

`scripts/list_due_monitoring.py` is the portable fallback. The AURA front door may include due/unbound monitoring in its execution envelope so the agent can:

- refresh overdue intelligence when it is relevant to the current request;
- surface a concise due-work notice when it materially matters but would derail the current request;
- avoid repeated alerts for unchanged/irrelevant work.

Do not interrupt every ordinary task with a monitoring backlog. Continuity should reduce forgotten work, not create notification noise.
