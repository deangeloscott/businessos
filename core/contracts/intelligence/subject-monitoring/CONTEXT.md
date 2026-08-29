---
id: core.intelligence.subject-monitoring
type: playbook
version: 1.1.0
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
Let the organization build cumulative external intelligence over time instead of restarting research from zero, while remaining portable, evidence-bounded, signal-driven, and explicit about whether future refreshes are actually automated.

## Run When
Run when the user asks AURA to follow, track, deeply understand, refresh, or keep current a company, creator, public figure, publication, platform, product/brand, regulator, community, the active organization, or another decision-relevant subject.

## Process
1. [AI] Resolve the subject, its relationship to the active business, the user's actual question/decision, and the level of depth required. A relationship such as competitor, creator, benchmark, own organization, platform, or ecosystem actor does not by itself change domain ownership.
2. [HYBRID] Resolve authoritative/public profiles and sources. Use one SourceProfile per source/surface and a shared `subject_key` only after the identities are sufficiently matched. Preserve aliases and ambiguity rather than merging namesakes.
3. [AI] Define the smallest useful monitoring plan: questions, material-change signals, source classes/modalities, baseline window, and an appropriate cadence/next check. If the user specified a cadence, preserve it. Otherwise infer the slowest decision-useful cadence from expected rate of change and business consequence. Cadence may differ by subject/source/signal; do not impose one global monthly/weekly default and do not default to exhaustive or continuous crawling.
4. [HYBRID] Before concluding that a useful modality is unavailable, use host-capability discovery and capability preflight. If a trusted optional local capability pack can materially improve the work, inspect it with `scripts/manage_local_capabilities.py`; bind an already healthy tool without reinstalling it, and ask before any system install/update/repair. For media, acquisition/FFmpeg mechanics do not themselves establish semantic visual/audio understanding.
5. [INTEGRATION] For the current bounded check, acquire the best available evidence. Treat text, documents, images, audio, video, transcripts, captions, comments, structured records, and mixed-media pages as potential evidence. Prefer native multimodal inspection when available; otherwise use legitimate extraction/transcript/frame/document fallbacks and record the limitation.
6. [DETERMINISTIC] Preserve support-grade SourceRecords/evidence according to `core/policies/research-evidence.md` and `core/policies/intelligence-foundation.md`; update SourceProfile checkpoints instead of duplicating unchanged state. Persist semantic cadence in SourceProfile state through the supported helper; cadence/`next_check_at` is monitoring intent, not proof that a background task exists.
7. [AI] Publish direct factual Observations for material changes and compare them with prior state. Examples may include funding, hiring, layoffs, executive changes, M&A, partnerships, product/pricing/positioning changes, geographic expansion, content/message shifts, reviews/mentions, or other signals relevant to the stated watch.
8. [HYBRID] Route interpretation to the semantic owner: competitor strategy to Competitor Intelligence, broad market events to Industry Intelligence, creator/content mechanisms to Content Synthesis, customer/public-experience themes to Customer Intelligence, organic/local competition to SEO/AEO, and active-business truth changes through normal first-party/context governance.
9. [HYBRID] If the user actually requested recurring monitoring, follow `core/policies/monitoring-continuity.md`. Use an already-authorized harness scheduler first; otherwise an authorized OS/workflow scheduler when a compatible worker exists; otherwise reminder-only, due-on-next-start, or manual fallback. Record an external schedule as active only after it exists and is verified through `scripts/register_scheduler_binding.py`. Never call a saved `next_check_at` "scheduled" by itself.
10. [HYBRID] Surface an AttentionItem only when a material change needs human review/action, a user-requested automation is genuinely blocked, or no existing semantic item already represents the issue. Repeated unchanged checks should update checkpoint/binding state rather than create alert noise.
11. [DETERMINISTIC] Refresh the human knowledge layer when useful. Normal-user completion should point to the human concept first (for example `AtlasOps → Knowledge → Tracked Subjects → <subject>`) and include raw canonical/runtime paths only when they help an advanced operator/debugger.

## Verification
- Every material observation is traceable to inspected/preserved evidence.
- Identity resolution is explicit enough to avoid cross-subject contamination.
- Unchanged checks do not create duplicate Insights/alerts.
- Monitoring scope/cadence is proportionate to decision value and expected rate of change.
- User-specified cadence is not silently replaced by inferred cadence.
- A claimed automatic schedule has a verified environment scheduler binding; otherwise the state is described as reminder-only, planned/unbound/due-on-next-start, paused, or manual.
- No external signal silently becomes active-business truth or a domain-owned strategic conclusion.

## Completion Criteria
- The subject/source watch is durable and resumable, the current bounded check is evidence-backed, material changes are represented once, domain-specific next work is routed without creating a competing intelligence system, and the user can tell whether future monitoring is truly automated or merely planned.
