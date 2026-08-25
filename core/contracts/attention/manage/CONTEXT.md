---
id: core.attention.manage
type: service
version: 1.8.4
owner_system: core
risk: low
autonomy_ceiling: 4
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
Represent a material condition that needs user/harness awareness without coupling BusinessOS to any notification channel.

## Business Outcome
Keep one small, deduplicated, resolvable queue of work/changes that need attention while allowing any compatible harness to decide how and when to surface it.

## Run When
When otherwise useful work is blocked on approval/input/credentials/capability, a material external/business change needs review, or a significant unresolved failure/incident cannot be safely completed autonomously.

## Process
1. [HYBRID] Confirm the condition is material enough to require attention; routine successful/unchanged monitoring does not qualify.
2. [DETERMINISTIC] Derive a stable business-scoped semantic `dedupe_key` from the underlying condition rather than the current timestamp/run/provider delivery.
3. [DETERMINISTIC] Use `scripts/upsert_attention.py` to create or update one `AttentionItem`; repeated detection updates `last_seen`/`occurrence_count` rather than creating duplicate files.
4. [HYBRID] State why attention is needed, the smallest recommended action, blocking condition, severity, evidence/source refs, and originating canonical refs without inventing urgency or outcomes.
5. [DETERMINISTIC] When acknowledged/resolved/superseded, update lifecycle through `scripts/set_attention_status.py`; resolution should point to verification/change/approval/evidence when available.
6. [DETERMINISTIC] Expose active state through `scripts/list_attention.py`; do not implement Slack/email/push/scheduler behavior inside BusinessOS.
7. [DETERMINISTIC] Periodically archive old resolved/superseded items with `scripts/maintain_lifecycle.py`; archived history is not normal agent context.

## Verification
There is at most one active item per dedupe key, repeated unchanged detections do not multiply files, terminal items leave the active queue, and delivery remains harness/provider agnostic.
