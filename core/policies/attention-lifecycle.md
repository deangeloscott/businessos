# Attention and Lifecycle

**Attention is organizational memory, not execution authority.** An `AttentionItem` records a material condition worth remembering because future work may need awareness, follow-up, resolution, or review. Its existence is not an execution gate and is not proof that a background task exists.

A model, harness, provider, or external system may poll, watch, schedule, render, or deliver attention through Slack, email, push, terminal, tickets, or another channel. Those delivery mechanics remain runtime capabilities rather than AURA dependencies.

## When to create attention
Create or update an `AttentionItem` only when the condition should survive the current session and future organizational work materially benefits from knowing it.

Good examples include:
- a material competitor, customer, market, or platform change that should be revisited;
- missing evidence that materially limits an important decision;
- an experiment or initiative whose outcome remains unresolved;
- a real operational constraint another person/system must resolve;
- a significant incident, contradiction, stale state, or unresolved business condition.

Do not persist transient tool/runtime trouble, routine execution steps, or ordinary reminders merely because they happened. If a runtime problem becomes a durable organizational condition that future work genuinely needs to know, preserve the organizational meaning rather than the tool chatter.

Use `python3 scripts/upsert_attention.py ...` when possible. One semantic condition gets one stable `dedupe_key` within a business.

**Repetition updates state; meaningful change creates history.** While an item remains open/acknowledged, repeated observation updates `last_seen`, increments `occurrence_count`, and merges refs instead of creating another item or notification obligation. A previously resolved item may reopen when the same condition genuinely recurs.

## Active view and delivery
Canonical items live under `instances/<business-id>/operations/attention/`. Harnesses may query the current view with `python3 scripts/list_attention.py <business-id> --json` or read/watch the canonical files. AURA makes no assumption about delivery channel, cadence, scheduler, daemon, webhook, or UI.

## Lifecycle
- `open` — currently worth awareness or follow-up.
- `acknowledged` — seen/owned but not yet resolved.
- `resolved` — the underlying condition no longer needs active attention; preserve useful resolution references.
- `superseded` — replaced by a more current semantic item.
- `archived` — historical compact state, excluded from the normal active view.

Resolve an item when the underlying condition is no longer materially relevant or actionable. Do not keep resolved conditions open merely to preserve history.

## Retention and clutter control
Current state should stay small. `scripts/maintain_lifecycle.py` can move sufficiently old resolved/superseded AttentionItems and superseded PlatformChanges into `instances/<business-id>/history/...` while preserving canonical IDs and references. Repeated unchanged checks should not produce new canonical files.

Raw/high-volume monitoring and execution data belongs in runtime systems, bounded evidence, or temporary work state. AURA retains only the organizational meaning needed for future understanding and useful action.
