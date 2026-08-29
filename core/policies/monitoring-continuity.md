# Monitoring Continuity

AURA may decide that information should be refreshed on a cadence, but a semantic cadence is not the same thing as an active background schedule. Preserve that distinction everywhere.

## Core rule

AURA owns **what should be monitored, why, how often, what counts as material, and when a user should be surfaced something**. The host/harness/operating system/workflow provider owns the machinery that causes a future execution or notification to occur.

Never say a monitor is "scheduled", "active", or "will run" merely because a `SourceProfile` has `next_check_at` or a recurring cadence. Those fields express organization-owned monitoring intent. Automatic execution is true only when a current environment scheduler binding has been created and verified.

## Cadence

- Infer a reasonable starting cadence when durable monitoring is clearly requested and the user did not specify one. Base it on expected rate of change, business consequence, source volatility, and decision value.
- User-specified cadence wins over inferred cadence. Do not silently replace an explicit user cadence with a generic default.
- Cadence may differ by subject, source/surface, or signal. A competitor's pricing page may be monthly while hiring/news is weekly; a fast regulatory issue may justify daily checks while a creator baseline is monthly.
- Per-signal cadence should be machine-readable when the distinction matters rather than hidden only in prose.
- Prefer the slowest cadence that is still decision-useful. Do not create continuous polling merely because it is possible.
- A request to build a refreshable baseline is not automatically a request for background scheduling. A request such as "keep an eye on this", "monitor this", or an explicit recurring interval may authorize recurring monitoring within the user's stated scope, but installing software, connecting accounts, spending money, or creating privileged system persistence still follows the applicable authorization boundary.

## Notification/noise policy

Monitoring frequency and notification frequency are different. AURA may check often and surface rarely.

Default to **material changes only** unless the user asks for something noisier or quieter. A normal unchanged check should update checkpoints silently. Do not create or send a new notification merely to say that nothing changed.

Proactive surfacing should normally be limited to one or more of:

- a material evidence-backed change relevant to the monitoring purpose;
- a failure/blocker that prevents requested monitoring from continuing;
- a required user decision/authorization;
- genuinely overdue work when the lack of refresh now matters to a current decision;
- a cadence/status summary the user explicitly requested.

Use existing AttentionItem deduplication/state rather than generating repeated equivalent alerts. Repeated observations of the same unresolved condition should update the existing semantic item/occurrence state. When several low/medium items become relevant together, prefer one concise digest/summary over multiple interruptions when the host supports that presentation.

User-adjustable notification modes are:

- **material_changes_only** — default; unchanged checks stay quiet;
- **due_and_material_changes** — also surface when the monitoring work itself becomes meaningfully overdue;
- **all_checks** — explicitly noisy; surface every completed check when the user asks for this behavior;
- **silent** — keep monitoring/checkpoint state but do not proactively surface ordinary results; the user can still inspect status at any time.

A per-signal notification setting may override the source/default setting. Explicit user choices win over inferred defaults.

## Execution states

Treat monitoring continuity as one of these user-understandable states:

1. **Active automatic** — a verified scheduler binding exists in the current environment.
2. **Reminder-only** — a verified binding can surface that work is due but cannot autonomously run the required AI/business work.
3. **Due-on-next-start** — AURA has durable cadence/checkpoint state but no verified scheduler binding; the next AURA entry can notice overdue work and refresh it when relevant/authorized.
4. **Manual** — no automatic executor is available or desired; the user can ask AURA to refresh at any time.
5. **Paused/blocked** — the semantic watch remains durable but execution is intentionally paused or lacks a required dependency.

A scheduler binding belongs in the workspace environment overlay, not canonical business truth, because it is host-specific and regenerable. The monitoring intent/cadence remains durable organization state.

## Fallback ladder

When recurring monitoring is useful:

1. use an already-authorized harness-native scheduler when available;
2. otherwise use an appropriate authorized OS/workflow scheduler when the environment exposes one and a compatible worker can actually run the check;
3. otherwise use a reminder-only scheduler if available;
4. otherwise preserve `next_check_at` and surface overdue monitoring on the next AURA start when it materially matters;
5. manual refresh always remains valid.

Missing background automation changes the executor, not the monitoring plan. Do not fabricate completion or silently drop future work.

## Scheduler binding truth

- Store non-secret scheduler receipts/refs in `.businessos/environments/<environment>/scheduler-bindings.json` through the supported helper.
- An `active` binding must identify the target, actual executor, cadence, and a verification time/reference.
- Re-check a binding after a host change, migration, tool failure, or material schedule edit.
- A moved/copied workspace may preserve semantic monitoring state while its old scheduler binding becomes invalid; regenerate environment bindings rather than treating them as portable truth.
- If a schedule cannot be proven active, describe it as **planned/unbound**, not scheduled.

## Visibility and user control

A user should never need to remember raw JSON paths to know what AURA is watching. The model/harness should be able to answer ordinary requests such as:

- "What are you monitoring for us?"
- "What recurring checks are active?"
- "What is due?"
- "How often are you checking ServiceTitan?"
- "Make pricing monthly but hiring weekly."
- "Only tell me when something materially changes."
- "Pause the Hormozi watch."
- "Stop automatic monitoring but keep what we've learned."

Use `scripts/monitoring_status.py <business-id>` for a portable combined view of semantic cadence, per-signal cadence, notification mode, next-due state, and verified scheduler execution. The generated human knowledge view under `knowledge/<business-id>/_generated/Tracked-Subjects.md` is the file-based equivalent.

Changes to cadence/notification intent belong in SourceProfile state through supported helpers. Changes to actual host scheduling must also be applied to the host scheduler and reflected in `scheduler-bindings.json`; editing only the semantic cadence does not prove the external task changed.

Pausing/stopping monitoring should not delete accumulated organizational intelligence unless the user separately authorizes deletion. Prefer pausing the watch/executor while preserving the evidence/history already earned.

## On-start continuity

`scripts/list_due_monitoring.py` is the portable fallback used by AURA internals. The AURA front door may include due/unbound monitoring in its execution envelope so the agent can:

- refresh overdue intelligence when it is relevant to the current request;
- surface a concise due-work notice when it materially matters and the configured notification mode allows it;
- avoid repeated alerts for unchanged/irrelevant work.

Do not interrupt every ordinary task with a monitoring backlog. Continuity should reduce forgotten work, not create notification noise.
