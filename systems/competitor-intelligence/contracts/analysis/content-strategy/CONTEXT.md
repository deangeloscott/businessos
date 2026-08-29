---
id: competitor.analysis.content-strategy
type: playbook
version: 1.8.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 4
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - webpage.screenshot
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
  - creator_content.observe
  - public_comment.read
  - community.read
  - news.read
events:
  consumes:
  - none
  emits:
  - competitor.insight.updated
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Competitor Content Strategy

## Purpose
Understand the narratives, topics, formats, cadence, distribution, multimodal execution, and apparent audience role of competitor content.

## Business Outcome
Improve competitive decisions through evidence-backed competitor content strategy without mistaking observed activity or visible engagement for proven effectiveness.

## Run When
Run when a decision requires current competitor content strategy and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Inventory recent representative content across owned channels and major distribution surfaces, reusing resolved SourceProfiles/subject identity where available.
2. [HYBRID] Inspect the modalities that actually carry each representative item's mechanism. This may include article/page text, image/carousel composition, video visuals and spoken transcript, audio/podcast segments, thumbnails, demonstrations, captions/descriptions, comments, or linked pages. Record transcript-only, sampled-frame, inaccessible-comment, or other material acquisition limits.
3. [DETERMINISTIC] Classify format, topic, audience/awareness/funnel role, publish date, platform, CTA, and observable engagement/discovery data; preserve source/time/frame/page evidence for material examples.
4. [AI] Identify recurring narratives, teachings, series, content pillars, hooks, structures, proof/story devices, visual/audio mechanisms, unique evidence/assets, and distribution patterns.
5. [HYBRID] Separate SEO-driven, social/community, thought-leadership, product, and commercial content roles where evidence supports it; do not infer a funnel role solely from format/platform.
6. [AI] Compare coverage against customer questions/criteria, category narratives, the relevant competitive cohort, and this competitor's own recent baseline when enough evidence exists.
7. [HYBRID] Treat visible engagement/search performance as surface-specific proxies, not total content ROI. Normalize obvious account-size/age/repost effects where data allows and consider paid amplification, audience scale, celebrity, novelty, and controversy as alternative explanations.
8. [AI] Abstract transferable topic/format/creative mechanisms from competitor-specific expression; do not direct downstream systems to copy protected content/style.
9. [DETERMINISTIC] Publish content-strategy Observations/Insights for Content/SEO consumption with source coverage, confidence, and modality limitations explicit.
