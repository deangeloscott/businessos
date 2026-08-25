# Attention, Escalation, and Lifecycle

BusinessOS owns **attention semantics**, not notification delivery. A model/harness/provider may poll, watch, schedule, render, or deliver BusinessOS attention through Slack, email, push, terminal, tickets, or another channel, but those channel integrations are optional execution capabilities rather than BusinessOS dependencies.

## When to create attention
Create or update an `AttentionItem` only when a material business condition needs human/harness awareness because work is blocked, approval/input/credential/capability is required, a material external change needs review, or a significant unresolved validation/incident state cannot be safely completed autonomously. Do **not** create attention for routine successful checks, unchanged monitoring results, low-value informational noise, or every raw event.

Use `python3 scripts/upsert_attention.py ...` when possible. One semantic condition gets one stable `dedupe_key` within a business.

**Repetition updates state; meaningful change creates history.** While an item remains open/acknowledged, repeated detection updates `last_seen`, increments `occurrence_count`, and merges refs instead of creating another item or another notification obligation. A previously resolved item may reopen when the same condition genuinely recurs; the compact transition history records the episode rather than spawning duplicate active files.

## Portable queue
Canonical items live under `instances/<business-id>/operations/attention/`. Harnesses may query the current queue with `python3 scripts/list_attention.py <business-id> --json` or read/watch the canonical files. BusinessOS makes no assumption about delivery channel, cadence, scheduler, daemon, webhook, or UI. A harness should normally surface only open/acknowledged material items according to user preferences and should not re-alert merely because `occurrence_count` increased.

## Lifecycle
- `open` — currently requires awareness/action.
- `acknowledged` — seen/owned but not yet resolved; still active.
- `resolved` — underlying condition is no longer actionable; preserve resolution evidence.
- `superseded` — replaced by a more current semantic item.
- `archived` — historical compact state, excluded from the normal active queue.

Resolve an item when the underlying blocker/condition is verified resolved or the originating work is no longer relevant. Do not leave resolved conditions open simply to preserve history. Use `scripts/set_attention_status.py` for acknowledgement/resolution/supersession when possible.

## Retention and clutter control
Current state should stay small. `scripts/maintain_lifecycle.py` can move sufficiently old resolved/superseded AttentionItems and superseded PlatformChanges into `instances/<business-id>/history/...` while preserving their canonical IDs and references. It does not delete durable referenced history. Repeated unchanged checks should never produce new canonical files in the first place.

Raw/high-volume monitoring data belongs in provider systems, bounded evidence, or temporary run state; BusinessOS should retain only the evidence necessary to audit material conclusions. Do not turn polling frequency into filesystem growth.
