---
id: competitor.analysis.content-strategy
type: playbook
version: 1.7.0
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
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
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
Understand the narratives, topics, formats, cadence, distribution, and apparent audience role of competitor content.

## Business Outcome
Improve competitive decisions through evidence-backed competitor content strategy, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor content strategy and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Inventory recent representative content across owned channels and major distribution surfaces.
2. [DETERMINISTIC] Classify format, topic, audience/stage, publish date, platform, CTA, and observable engagement/discovery data.
3. [AI] Identify recurring narratives, series, content pillars, unique evidence/assets, and distribution patterns.
4. [HYBRID] Separate SEO-driven, social/community, thought-leadership, product, and commercial content roles where evidence supports it.
5. [AI] Compare coverage against customer questions/criteria and category narratives.
6. [HYBRID] Treat visible engagement/search performance as surface-specific evidence, not total content ROI.
7. [DETERMINISTIC] Publish content-strategy Insights for Content/SEO consumption.
