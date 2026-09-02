---
id: core.monitoring.status
type: workflow
owner_system: core
reads:
- SourceProfile
- AttentionItem
writes: []
context:
- Business
---
# Review Monitoring Intent

## Purpose
Give the user one understandable view of what the organization has asked AURA to keep watching, why it matters, intended cadence/materiality, what appears due for another useful check, and what meaningful findings remain unresolved.

## Business Outcome
Make durable monitoring intent inspectable and reusable across sessions/harnesses without pretending AURA itself owns a scheduler, daemon, polling loop, notification channel, or active background job.

## Run When
Run when the user asks what AURA is watching, what monitoring plans exist, what appears due for another check, how often a subject/signal is intended to be revisited, or wants to review/change monitoring intent.

## Process
1. [DETERMINISTIC] Resolve the active business.
2. [DETERMINISTIC] Run `scripts/monitoring_status.py <business-id> --json` to summarize durable SourceProfile cadence/materiality/notification intent and semantic due state.
3. [AI] Present a concise human summary grouped by subject. Clearly distinguish cadence intent from actual runtime scheduling and notification intent from an active delivery channel.
4. [HYBRID] When the user asks to change what should be watched, cadence intent, materiality criteria, notification intent, or pause/resume the semantic watch, update the applicable organization-owned monitoring state through the subject-monitoring path.
5. [AI] If the user asks whether an actual recurring/background task is running, answer only from the active harness/runtime's real scheduler/task state when available. AURA monitoring state alone is never proof that automation is active.
6. [HYBRID] If the user asks to stop monitoring, preserve accumulated organizational intelligence unless deletion was separately requested; retire/pause the semantic watch and let the active runtime manage any real scheduled task through its own facilities.

## Verification
- No cadence intent is represented as an active schedule merely because AURA stores it.
- Notification intent does not imply a notification channel exists.
- Related sources for one subject are summarized together while meaningful source/signal differences remain visible.
- Unknown runtime automation state remains unknown rather than being inferred from AURA files.

## Completion Criteria
- The user receives an accurate view of durable monitoring intent/due state, and any runtime scheduling claim is grounded in the current harness rather than AURA-owned scheduler metadata.
