---
id: core.intelligence.subject-monitoring
type: playbook
version: 1.2.0
owner_system: core
risk: low
autonomy_ceiling: 4
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
  - automation.schedule.manage
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
Create or refresh a bounded, organization-owned watch for a decision-relevant public/authorized subject across one or more evidence surfaces while keeping domain interpretation with the existing semantic owner.

## Business Outcome
Let the organization build cumulative external intelligence over time instead of restarting research from zero, while remaining portable, evidence-bounded, signal-driven, quiet by default, user-adjustable, and explicit about whether future refreshes are actually automated.

## Run When
Run when the user asks AURA to follow, track, deeply understand, refresh, or keep current a company, creator, public figure, publication, platform, product/brand, regulator, community, the active organization, or another decision-relevant subject.

## Process
1. [AI] Resolve the subject, its relationship to the active business, the user's actual question/decision, and the level of depth required. A relationship such as competitor, creator, benchmark, own organization, platform, or ecosystem actor does not by itself change domain ownership.
2. [HYBRID] Resolve authoritative/public profiles and sources. Use one SourceProfile per source/surface and a shared `subject_key` only after the identities are sufficiently matched. Preserve aliases and ambiguity rather than merging namesakes.
3. [AI] Define the smallest useful monitoring plan: questions, material-change signals, source classes/modalities, baseline window, and an appropriate cadence/next check. If the user specified a cadence, preserve it. Otherwise infer the slowest decision-useful cadence from expected rate of change and business consequence. Cadence may differ by subject, source, or signal; persist meaningful per-signal differences as machine-readable `monitoring_signal_cadences` rather than hiding them in prose. Do not impose one global monthly/weekly default and do not default to exhaustive or continuous crawling.
4. [AI] Resolve notification intent separately from check cadence. Default to `material_changes_only`: unchanged checks update checkpoints silently. Honor user requests for `due_and_material_changes`, `all_checks`, or `silent`, including per-signal overrides when useful. Do not silently replace an explicit user notification choice with an inferred default.
5. [HYBRID] Before concluding that a useful modality is unavailable, use host-capability discovery and capability preflight. If a trusted optional local capability pack can materially improve the work, inspect it with `scripts/manage_local_capabilities.py`; bind an already healthy tool without reinstalling it, and ask before any system install/update/repair. For media, acquisition/FFmpeg mechanics do not themselves establish semantic visual/audio understanding.
6. [INTEGRATION] For the current bounded check, acquire the best available evidence. Treat text, documents, images, audio, video, transcripts, captions, comments, structured records, and mixed-media pages as potential evidence. Prefer native multimodal inspection when available; otherwise use legitimate extraction/transcript/frame/document fallbacks and record the limitation.
7. [DETERMINISTIC] Preserve support-grade SourceRecords/evidence according to `core/policies/research-evidence.md` and `core/policies/intelligence-foundation.md`; update SourceProfile checkpoints instead of duplicating unchanged state. Persist semantic cadence/notification intent in SourceProfile state through the supported helper; cadence/`next_check_at` is monitoring intent, not proof that a background task exists.
8. [AI] Publish direct factual Observations for material changes and compare them with prior state. Examples may include funding, hiring, layoffs, executive changes, M&A, partnerships, product/pricing/positioning changes, geographic expansion, content/message shifts, reviews/mentions, or other signals relevant to the stated watch.
9. [HYBRID] Route interpretation to the semantic owner: competitor strategy to Competitor Intelligence, broad market events to Industry Intelligence, creator/content mechanisms to Content Synthesis, customer/public-experience themes to Customer Intelligence, organic/local competition to SEO/AEO, and active-business truth changes through normal first-party/context governance.
10. [HYBRID] If the user actually requested recurring monitoring, follow `core/policies/monitoring-continuity.md`. Use an already-authorized harness scheduler first; otherwise an authorized OS/workflow scheduler when a compatible worker exists; otherwise reminder-only, due-on-next-start, or manual fallback. Record an external schedule as active only after it exists and is verified through `scripts/register_scheduler_binding.py`. Never call a saved `next_check_at` "scheduled" by itself.
11. [HYBRID] Surface an AttentionItem only when a material change needs human review/action, a user-requested automation is genuinely blocked, a required decision/authorization is needed, or no existing semantic item already represents the issue. Repeated unchanged checks should update checkpoint/binding state rather than create alert noise. Prefer one concise digest over many low-value interruptions when several related low/medium items can be reviewed together.
12. [HYBRID] Support ordinary user control. Inspect current monitoring with `scripts/monitoring_status.py <business-id>`. Persist cadence/notification edits through SourceProfile helpers. For "pause/stop this watch but keep what we learned", use `scripts/set_monitoring_watch_status.py` rather than deleting evidence/history, and separately pause/disable any real host scheduler before updating its scheduler-binding receipt. If semantic watch state and actual scheduler state disagree, surface the mismatch rather than claiming the watch stopped.
13. [DETERMINISTIC] Refresh the human knowledge layer when useful. Normal-user completion should point to the human concept first (for example `AtlasOps → Knowledge → Tracked Subjects → <subject>`) and include raw canonical/runtime paths only when they help an advanced operator/debugger. The user/model/harness should be able to review and change monitoring through normal AURA requests without knowing internal paths.

## Verification
- Every material observation is traceable to inspected/preserved evidence.
- Identity resolution is explicit enough to avoid cross-subject contamination.
- Unchanged checks do not create duplicate Insights/alerts or routine "nothing changed" notifications under the default policy.
- Monitoring scope/cadence is proportionate to decision value and expected rate of change.
- User-specified cadence and notification preferences are not silently replaced by inferred defaults.
- Meaningful per-signal cadence differences are machine-readable and visible to the user.
- A claimed automatic schedule has a verified environment scheduler binding; otherwise the state is described as reminder-only, planned/unbound/due-on-next-start, paused, or manual.
- Pausing a watch preserves accumulated intelligence and an active host scheduler cannot be hidden behind a semantic paused flag.
- Current monitoring can be listed in one combined human/AI-readable view and changed without deleting accumulated intelligence.
- No external signal silently becomes active-business truth or a domain-owned strategic conclusion.

## Completion Criteria
- The subject/source watch is durable and resumable, the current bounded check is evidence-backed, material changes are represented once, domain-specific next work is routed without creating a competing intelligence system, and the user can tell what is monitored, how often, how noisy it is, and whether future monitoring is truly automated or merely planned.
