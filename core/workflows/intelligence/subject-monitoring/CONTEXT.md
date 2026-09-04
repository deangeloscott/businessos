---
id: core.intelligence.subject-monitoring
type: workflow
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
- AttentionItem
context:
- Business
- Market
- Objective
---
# Durable Subject Monitoring

## Purpose
Create or refresh a bounded, organization-owned watch for a decision-relevant public/authorized subject while keeping runtime scheduling and domain interpretation outside the monitoring record itself.

## Business Outcome
Let the organization accumulate useful external intelligence over time instead of restarting from zero, without turning AURA into a crawler, scheduler, notification service, semantic router, or competing intelligence system.

## Run When
Use when the user wants to follow, track, understand, refresh, or keep current a company, creator, public figure, publication, platform, product/brand, regulator, community, the active organization, or another decision-relevant subject.

## Process
1. [AI] Resolve the subject, its relationship to the active business, the user's real question/decision, and the depth required. Preserve identity ambiguity rather than merging namesakes.
2. [HYBRID] Resolve useful authoritative/public sources. Use one SourceProfile per source/surface when durable source memory is useful, and a shared `subject_key` only after the capable model/user has enough evidence to treat identities as the same real-world subject. Draw on `core.intelligence.ecosystem.maintain-source-profile` when its source-memory method adds value; it is not a mandatory stage.
3. [AI] Define the smallest useful monitoring intent: questions, material-change signals, source classes/modalities, and cadence/next useful check. Preserve user-specified cadence. Otherwise the model may suggest the slowest decision-useful cadence. Persist meaningful per-signal differences in `monitoring_signal_cadences` only when useful.
4. [AI] Keep notification intent separate from check cadence. Honor explicit user choices; otherwise use a quiet material-change-oriented default rather than creating alert noise.
5. [HYBRID] For the current bounded check, use the best evidence capabilities actually available to the active model/harness/user. AURA may describe useful evidence modalities or preserve acquisition limitations, but it does not inventory, bind, install, rank, or select tools/providers.
6. [HYBRID] Acquire and inspect the best available evidence. Treat text, documents, images, audio, video, transcripts, captions, comments, structured records, and mixed-media pages as potential evidence. Preserve material acquisition limitations.
7. [DETERMINISTIC] Preserve support-grade SourceRecords/evidence and update SourceProfile checkpoints when useful instead of duplicating unchanged exact state. Cadence and `next_check_at` are organizational monitoring intent, never proof that a background task exists.
8. [AI] Preserve direct factual Observations for material changes and compare them with prior state when useful.
9. [AI] Use relevant domain operating knowledge when deeper interpretation is needed—for example Competitor, Industry, Content, Customer, SEO/AEO, or active-business context. AURA does not deterministically route semantic meaning between domains.
10. [HYBRID] If recurring background execution is actually wanted, preserve the monitoring intent and let the current harness/runtime create the real schedule separately. Only the runtime that actually creates/observes that schedule may claim automation is active.
11. [HYBRID] Surface an AttentionItem only when a material condition genuinely needs future organizational awareness/action or a real unresolved dependency matters. Repeated unchanged checks should update checkpoints rather than create alert noise.
12. [HYBRID] Support ordinary user control. `scripts/monitoring_status.py <business-id>` shows the saved watch/cadence/due state. For "pause this watch but keep what we learned", use `scripts/set_monitoring_watch_status.py`; do not delete accumulated evidence/history.
13. [HYBRID] Refresh the human knowledge layer when it would genuinely improve reviewability; this is an optional view, not required monitoring state.

## Verification
- Material observations are traceable to inspected/preserved evidence.
- Identity resolution avoids cross-subject contamination.
- Unchanged checks do not create duplicate findings/alerts.
- Monitoring scope/cadence is proportionate to decision value and expected rate of change.
- Explicit cadence/notification preferences are preserved.
- AURA never claims `next_check_at` or cadence proves future automatic execution.
- Pausing a watch preserves accumulated intelligence.
- Domain-specific conclusions come from capable semantic work rather than deterministic monitoring state.

## Completion Criteria
The monitoring intent is durable and understandable, the current bounded check is evidence-backed, material changes are represented without duplication, and future runtime automation—if any—remains owned and truthfully represented by the active harness rather than AURA.
