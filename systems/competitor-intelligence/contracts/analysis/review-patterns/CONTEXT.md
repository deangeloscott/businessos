---
id: competitor.analysis.review-patterns
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - review.read
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Review Pattern Analysis

## Purpose
Analyze recurring competitor praise, complaints, expectations, and switching evidence from public/customer sources.

## Business Outcome
Reveal competitor strengths and vulnerabilities customers actually experience while respecting sampling limits.

## Run When
Run when competitor customer sentiment is relevant to positioning, product, sales, or customer strategy.

## Process
1. [INTEGRATION] Collect current reviews/comments from legitimate sources with dates, ratings, product/location context, and source refs.
2. [DETERMINISTIC] Deduplicate syndicated/identical reviews and identify obvious source/platform selection effects.
3. [AI] Code praise, complaints, outcomes, use cases, expectations, support/service, switching reasons, and comparison mentions.
4. [DETERMINISTIC] Compare theme frequency by source, date, segment/context where known, and rating/outcome without treating review populations as representative of all customers.
5. [AI] Identify persistent patterns, changes, and negative cases.
6. [HYBRID] Separate customer statements from conclusions about the competitor and mark possible manipulation/unreliable evidence.
7. [AI] Publish competitor sentiment Observations/Insights and relevant signals to Customer Intelligence.
