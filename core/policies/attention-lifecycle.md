# Attention

**Attention is organizational memory, not execution authority.** An `AttentionItem` records a material condition worth remembering because future work may benefit from awareness, follow-up, resolution, or review. Its existence is not an execution gate, task queue, notification obligation, or proof that a background task exists.

A model, harness, provider, or external system may poll, watch, schedule, or deliver attention through Slack, email, push, terminal, tickets, or another channel. Those delivery mechanics remain runtime capabilities rather than AURA dependencies.

## When to create attention
Create or update an `AttentionItem` only when the condition should survive the current session and future organizational work materially benefits from knowing it.

Good examples include:
- a material competitor, customer, market, or platform change that should be revisited;
- missing evidence that materially limits an important decision;
- an experiment or initiative whose outcome remains unresolved;
- a real operational constraint another person/system must resolve;
- a significant contradiction, stale state, or unresolved business condition.

Do not persist transient tool/runtime trouble, routine execution steps, or ordinary reminders merely because they happened. If a runtime problem becomes a durable organizational condition, preserve the organizational meaning rather than the tool chatter.

Use `python3 scripts/upsert_attention.py ...` when useful. One semantic condition gets one stable business-scoped `dedupe_key`.

**Repetition updates the same condition.** While an item remains open or acknowledged, repeated observation updates `last_seen`, increments `occurrence_count`, and merges useful refs rather than creating another item. A resolved/archived item may reopen when that same semantic condition genuinely recurs. If the meaning changes enough to be a different condition, use a different dedupe key rather than building a supersession graph.

## Current state
- `open` — currently worth awareness or follow-up.
- `acknowledged` — seen, but the underlying condition still matters.
- `resolved` — the condition no longer needs active attention; preserve useful resolution references.
- `archived` — explicitly retained historical state outside the normal active view.

These statuses describe organizational memory. They do not authorize, block, assign, schedule, or prove execution.

Canonical active items live under `instances/<business-id>/operations/attention/`. Harnesses may query them with `python3 scripts/list_attention.py <business-id> --json` or read/watch the canonical files. AURA makes no assumption about delivery channel, cadence, scheduler, daemon, webhook, or UI.

## Historical retention

Keeping the active view small is useful, but **elapsed time is not semantic authority**. AURA must not decide that a resolved condition is no longer useful merely because 90 days, 180 days, or another arbitrary interval has passed.

When the active model/user determines that an already-resolved AttentionItem should remain available only as history, use:

`python3 scripts/archive_history.py <business-id> <attention-id> --reason "<why this should leave the active view>"`

The helper performs only mechanical work: it verifies that the item is already `resolved`, changes it to `archived`, preserves the explicit reason/time, and moves it under `instances/<business-id>/history/AttentionItem/`. It does not choose candidates, infer retention value, or schedule housekeeping.

The same explicit-history helper may move an already-`superseded` `PlatformChange` out of the active platform-state view. Current platform state can never be archived by this helper.

Repeated unchanged checks should not produce new canonical files. Raw/high-volume monitoring and execution data belongs in runtime systems, bounded evidence, or temporary work state. AURA retains only the organizational meaning needed for future understanding and useful action.
