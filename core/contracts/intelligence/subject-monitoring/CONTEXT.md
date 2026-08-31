---
id: core.intelligence.subject-monitoring
type: playbook
version: 1.3.0
owner_system: core
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Business
- Market
- Objective
writes:
- SourceProfile
- SourceRecord
- Observation
- WorkRequest
- AttentionItem
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - news.read
  - social.observe
  - social.listen
  - creator_content.observe
  - public_comment.read
  - rss.read
  - document.read
  - webpage.fetch
  - webpage.snapshot
  - webpage.compare
  - webpage.screenshot
  - crawler.run
  - media.video.acquire
  - media.transcript.acquire
  - media.metadata.inspect
  - media.video.process
  - media.audio.extract
  - media.frame.extract
context:
- Business
- Market
- Objective
subcontracts:
  required:
  - core.intelligence.ecosystem.maintain-source-profile
---
# Durable Subject Monitoring

## Purpose
Create or refresh a bounded, organization-owned watch for a decision-relevant public/authorized subject while keeping runtime scheduling and domain interpretation outside the monitoring record itself.

## Business Outcome
Let the organization accumulate useful external intelligence over time instead of restarting from zero, without turning AURA into a crawler, scheduler, notification service, or competing intelligence system.

## Run When
Run when the user asks AURA to follow, track, understand, refresh, or keep current a company, creator, public figure, publication, platform, product/brand, regulator, community, the active organization, or another decision-relevant subject.

## Process
1. [AI] Resolve the subject, its relationship to the active business, the user's real question/decision, and the depth required. Preserve identity ambiguity rather than merging namesakes.
2. [HYBRID] Resolve useful authoritative/public sources. Use one SourceProfile per source/surface and a shared `subject_key` only after identities are sufficiently matched.
3. [AI] Define the smallest useful monitoring intent: questions, material-change signals, source classes/modalities, and cadence/next useful check. Preserve user-specified cadence. Otherwise infer the slowest decision-useful cadence. Persist meaningful per-signal differences in `monitoring_signal_cadences`.
4. [AI] Resolve notification intent separately from check cadence. Default to `material_changes_only`; honor explicit `due_and_material_changes`, `all_checks`, or `silent` choices.
5. [HYBRID] For the current bounded check, use the best evidence capabilities actually available to the active model/harness/user. AURA's capability declarations describe useful modalities only; they do not inventory, bind, install, rank, or select the tools/providers that satisfy them.
6. [HYBRID] Acquire and inspect the best available evidence. Treat text, documents, images, audio, video, transcripts, captions, comments, structured records, and mixed-media pages as potential evidence. Use native multimodal inspection or legitimate fallbacks and record material limitations.
7. [DETERMINISTIC] Preserve support-grade SourceRecords/evidence and update SourceProfile checkpoints instead of duplicating unchanged state. Cadence and `next_check_at` are organizational monitoring intent, never proof that a background task exists.
8. [AI] Publish direct factual Observations for material changes and compare them with prior state.
9. [HYBRID] Route interpretation to the semantic owner when useful: competitor strategy to Competitor Intelligence, broad market events to Industry Intelligence, content mechanisms to Content Synthesis, customer themes to Customer Intelligence, organic/local competition to SEO/AEO, and active-business truth changes through normal evidence/context semantics.
10. [HYBRID] If the user also wants recurring background execution, preserve the AURA monitoring intent and let the current harness/runtime handle scheduling separately. AURA does not create, mirror, or certify scheduler bindings. Only the runtime that actually created a schedule may claim it is active.
11. [HYBRID] Surface an AttentionItem only when a material condition genuinely needs future awareness/action or a real unresolved dependency matters. Repeated unchanged checks should update checkpoints rather than create alert noise.
12. [HYBRID] Support ordinary user control. `scripts/monitoring_status.py <business-id>` shows semantic watch/cadence/due state. For "pause this watch but keep what we learned", use `scripts/set_monitoring_watch_status.py`; do not delete accumulated evidence/history.
13. [DETERMINISTIC] Refresh the human knowledge layer when useful so the user can review the watch without knowing raw object paths.

## Verification
- Material observations are traceable to inspected/preserved evidence.
- Identity resolution avoids cross-subject contamination.
- Unchanged checks do not create duplicate findings/alerts.
- Monitoring scope/cadence is proportionate to decision value and expected rate of change.
- Explicit cadence/notification preferences are preserved.
- AURA never claims `next_check_at` or cadence proves future automatic execution.
- Pausing a watch preserves accumulated intelligence.
- Domain-specific conclusions remain with the appropriate semantic work rather than being invented by the monitoring record.

## Completion Criteria
The monitoring intent is durable and understandable, the current bounded check is evidence-backed, material changes are represented without duplication, and future runtime automation—if any—remains owned and truthfully represented by the active harness rather than AURA.
