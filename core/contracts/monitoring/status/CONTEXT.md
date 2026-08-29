---
id: core.monitoring.status
type: service
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- SourceProfile
- AttentionItem
writes: []
capabilities:
  required:
  - none
  optional:
  - none
context:
- Business
---
# Review Monitoring Status

## Purpose
Give the user one understandable view of what AURA is monitoring, how often, what is due, how noisy each watch is intended to be, and whether recurring execution is actually active.

## Business Outcome
Make durable monitoring inspectable and controllable without requiring users to remember SourceProfile files, scheduler IDs, or host-specific paths.

## Run When
Run when the user asks what AURA is monitoring, what recurring checks/schedules exist, what is due, how often a subject/signal is checked, whether monitoring is actually automatic, or wants a status review before changing monitoring.

## Process
1. [DETERMINISTIC] Resolve the active business and environment.
2. [DETERMINISTIC] Run `scripts/monitoring_status.py <business-id> --json` to combine SourceProfile cadence/notification intent with verified scheduler bindings.
3. [AI] Present a concise human summary grouped by subject. Distinguish default/source cadence from signal-specific cadence, notification mode from check frequency, due state from material-change state, and planned/unbound from active automatic execution.
4. [AI] When the user asks to change cadence, notification mode, pause/resume a watch, or stop automatic execution, route the mutation through `core.intelligence.subject-monitoring` and the applicable host scheduler path rather than editing only the displayed view.
5. [HYBRID] If the user asks to stop monitoring, preserve accumulated organizational intelligence unless deletion was separately requested; pause/disable the semantic watch and actual executor as appropriate.

## Verification
- No planned cadence is represented as an active schedule without a verified scheduler binding.
- Quiet/default notification behavior is visible and does not imply a notification channel exists.
- Related sources for one subject are summarized together while source-specific/per-signal differences remain visible.
- The user can understand how to change the watch without seeing internal contract/schema mechanics.

## Completion Criteria
- The user receives one current, accurate monitoring/scheduling view and any requested changes are handed to the governed monitoring path rather than hidden filesystem edits.
