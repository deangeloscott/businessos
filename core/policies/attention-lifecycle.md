# Attention and Lifecycle

AURA owns **attention semantics**, not notification delivery. A model, harness, provider, or external system may poll, watch, schedule, render, or deliver AURA attention through Slack, email, push, terminal, tickets, or another channel, but those delivery mechanisms are runtime capabilities rather than AURA dependencies.

## When to create attention
Create or update an `AttentionItem` only when a material organizational condition should survive the current session because future work benefits from knowing that something needs awareness, follow-up, resolution, or review.

Good examples include:
- a material competitor or market change that should be revisited;
- missing evidence that materially limits an important decision;
- an experiment or initiative whose outcome is still unresolved;
- a real operational blocker that another person/system must resolve;
- a significant incident, contradiction, stale state, or unresolved business condition.

Do **not** create attention merely because AURA assigns a generic risk level, because an approval framework says a gate is required, because a cached capability appears unavailable, or because a routine tool/runtime step failed transiently. Runtime capability/tool failures belong to the harness unless they become a durable organizational blocker worth remembering.

Use `python3 scripts/upsert_attention.py ...` when possible. One semantic condition gets one stable `dedupe_key` within a business.

**Repetition updates state; meaningful change creates history.** While an item remains open/acknowledged, repeated detection updates `last_seen`, increments `occurrence_count`, and merges refs instead of creating another item or another notification obligation. A previously resolved item may reopen when the same condition genuinely recurs.

## Portable queue
Canonical items live under `instances/<business-id>/operations/attention/`. Harnesses may query the current queue with `python3 scripts/list_attention.py <business-id> --json` or read/watch the canonical files. AURA makes no assumption about delivery channel, cadence, scheduler, daemon, webhook, or UI.

## Lifecycle
- `open` — currently worth awareness or follow-up.
- `acknowledged` — seen/owned but not yet resolved.
- `resolved` — underlying condition no longer needs active attention; preserve useful resolution references.
- `superseded` — replaced by a more current semantic item.
- `archived` — historical compact state, excluded from the normal active queue.

Resolve an item when the underlying condition is no longer materially actionable or the originating work is no longer relevant. Do not keep resolved conditions open merely to preserve history.

## Retention and clutter control
Current state should stay small. `scripts/maintain_lifecycle.py` can move sufficiently old resolved/superseded AttentionItems and superseded PlatformChanges into `instances/<business-id>/history/...` while preserving canonical IDs and references. Repeated unchanged checks should never produce new canonical files in the first place.

Raw/high-volume monitoring and execution data belongs in provider/runtime systems, bounded evidence, or temporary work state. AURA should retain only the organizational meaning needed for future understanding and action.
