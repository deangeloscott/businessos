---
id: core.attention.manage
type: playbook
owner_system: core
reads:
- Business
- AttentionItem
- Opportunity
- WorkRequest
- Incident
- PlatformChange
writes:
- AttentionItem
capabilities:
  required:
  - none
  optional:
  - none
context:
- Business
---
# Manage Attention

## Purpose
Represent a material organizational condition that should remain visible across sessions without coupling AURA to any notification channel or generic governance gate.

## Business Outcome
Keep one small, deduplicated, resolvable queue of conditions worth future awareness or follow-up while letting the current model/harness decide how and when to surface them.

## Run When
When a material business condition, unresolved dependency, missing evidence, incident, important change, or unfinished outcome should survive the current session because later work will benefit from seeing it.

## Do Not Run When
Do not create attention merely because a generic risk label, approval framework, cached capability state, transient provider failure, or routine execution detail says something is blocked. Those are not automatically durable organizational facts.

## Process
1. [AI] Confirm the condition is materially useful to remember. Routine successful/unchanged monitoring and transient execution noise do not qualify.
2. [AI] Identify the stable business-scoped condition identity that should count as the same recurring AttentionItem across sessions. Express that as a compact `dedupe_key`; semantic sameness belongs to capable model/user judgment, not keyword hashing.
3. [DETERMINISTIC] Use `scripts/upsert_attention.py` with the chosen key to create/update one exact matching `AttentionItem`; repeated use of the same key updates `last_seen`/`occurrence_count` rather than creating duplicate files.
4. [AI] State why the condition matters, the smallest useful next action when one is known, material evidence/source refs, and originating organizational refs without inventing urgency, authority, or outcomes.
5. [DETERMINISTIC] When the condition is acknowledged or resolved, update its current status through `scripts/set_attention_status.py`; resolution should point to actual evidence, results, decisions, or changed state when available. If the same condition later returns, reopen the same stable item rather than creating a lifecycle graph.
6. [DETERMINISTIC] Expose active state through `scripts/list_attention.py`; notification and scheduling behavior stays outside AURA Core.
7. [DETERMINISTIC] Archive old resolved items with `scripts/maintain_lifecycle.py` when housekeeping is actually useful; AURA itself does not schedule periodic maintenance.

## Verification
There is at most one active item per explicitly chosen dedupe key, repeated unchanged detections do not multiply files, resolved items leave the active queue, and the stored condition remains organizationally meaningful rather than runtime bookkeeping.
