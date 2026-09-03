---
id: competitor.analysis.profiling
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceProfile
- type: Insight
  domain: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Competitor Profile

## Purpose
Build a current evidence-backed competitor state across the source modalities relevant to the decision without turning the summary object into a copy of raw evidence.

## Business Outcome
Improve competitive decisions through an evidence-backed competitor profile that can evolve over time, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor profile and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Retrieve current authoritative competitor-owned product/service, pricing, offer, positioning, company information, relevant public profiles, and useful third-party evidence. Reuse resolved SourceProfiles for this subject rather than recreating the source map. Draw on adaptive source coverage, source mapping, or baseline-snapshot operating knowledge when those methods materially improve coverage or comparison.
2. [HYBRID] Inspect the evidence modalities that materially carry the competitor signal. This may include webpages/documents, ads/images, video/audio/transcripts, social posts/comments, jobs/hiring pages, reviews, news, or structured records. Use native multimodal inspection when available; record limitations when a fallback representation was used.
3. [DETERMINISTIC] Snapshot/version important source pages or bounded evidence and compare with prior state where available.
4. [AI] Extract factual state separately from strategic interpretation; retain exact source references, timestamps/pages/frames where material, and acquisition limitations. When the source is about a resolved competitor, preserve the competitor ref in `SourceRecord.subject_refs` and carry compatible subject scope into supporting Observations/Insights. Do not attach another competitor's evidence to this profile merely because it appeared in the same research session.
5. [HYBRID] Reconcile conflicting sources by fact type, authority, freshness, directness, and subject relevance rather than defaulting to one source hierarchy.
6. [AI] Summarize current products, audiences, positioning, offers, public operating signals, strengths/weaknesses hypotheses, and notable recent changes. Use strength/weakness operating knowledge when its comparative method materially helps. Treat hiring, funding, partnerships, M&A, expansion, content/message shifts, or similar signals as evidence to interpret, not automatic proof of strategy. Where a material profile field is unsupported or stale, keep it limited/unknown instead of filling the field from memory or unrelated evidence.
7. [HYBRID] Attach confidence and unanswered questions to the Competitor record; confidence must reflect evidence directness, freshness, coverage, contradictions, and important gaps rather than the fluency of the summary. Keep detailed evidence in Observations/Insights and broad market events with Industry Intelligence when appropriate.
8. [DETERMINISTIC] Validate subject-scoped research evidence, persist the selected current profile state, and update `last_reviewed`. Do not emit an AURA runtime event merely because the profile changed.
