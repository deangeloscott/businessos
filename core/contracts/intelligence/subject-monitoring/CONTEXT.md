---
id: core.intelligence.subject-monitoring
type: playbook
version: 1.0.0
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
Let the organization build cumulative external intelligence over time instead of restarting research from zero, while remaining portable, evidence-bounded, and signal-driven.

## Run When
Run when the user asks AURA to follow, track, deeply understand, refresh, or keep current a company, creator, public figure, publication, platform, product/brand, regulator, community, the active organization, or another decision-relevant subject.

## Process
1. [AI] Resolve the subject, its relationship to the active business, the user's actual question/decision, and the level of depth required. A relationship such as competitor, creator, benchmark, own organization, platform, or ecosystem actor does not by itself change domain ownership.
2. [HYBRID] Resolve authoritative/public profiles and sources. Use one SourceProfile per source/surface and a shared `subject_key` only after the identities are sufficiently matched. Preserve aliases and ambiguity rather than merging namesakes.
3. [AI] Define the smallest useful monitoring plan: questions, material-change signals, source classes/modalities, baseline window, and an appropriate next-check cadence. Do not default to exhaustive or continuous crawling.
4. [INTEGRATION] For the current bounded check, acquire the best available evidence. Treat text, documents, images, audio, video, transcripts, captions, comments, structured records, and mixed-media pages as potential evidence. Prefer native multimodal inspection when available; otherwise use legitimate extraction/transcript/frame/document fallbacks and record the limitation.
5. [DETERMINISTIC] Preserve support-grade SourceRecords/evidence according to `core/policies/research-evidence.md` and `core/policies/intelligence-foundation.md`; update SourceProfile checkpoints instead of duplicating unchanged state.
6. [AI] Publish direct factual Observations for material changes and compare them with prior state. Examples may include funding, hiring, layoffs, executive changes, M&A, partnerships, product/pricing/positioning changes, geographic expansion, content/message shifts, reviews/mentions, or other signals relevant to the stated watch.
7. [HYBRID] Route interpretation to the semantic owner: competitor strategy to Competitor Intelligence, broad market events to Industry Intelligence, creator/content mechanisms to Content Synthesis, customer/public-experience themes to Customer Intelligence, organic/local competition to SEO/AEO, and active-business truth changes through normal first-party/context governance.
8. [HYBRID] Surface an AttentionItem only when a material change needs human review/action and no existing semantic item already represents it. AURA stores the watch/checkpoint; the host/harness chooses scheduling/notification machinery.

## Verification
- Every material observation is traceable to inspected/preserved evidence.
- Identity resolution is explicit enough to avoid cross-subject contamination.
- Unchanged checks do not create duplicate Insights/alerts.
- Monitoring scope/cadence is proportionate to decision value and expected rate of change.
- No external signal silently becomes active-business truth or a domain-owned strategic conclusion.

## Completion Criteria
- The subject/source watch is durable and resumable, the current bounded check is evidence-backed, material changes are represented once, and domain-specific next work is routed without creating a competing intelligence system.
