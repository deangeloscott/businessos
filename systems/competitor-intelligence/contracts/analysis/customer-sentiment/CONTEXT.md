---
id: competitor.analysis.customer-sentiment
type: playbook
version: 1.1.0
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
# Competitor Customer Sentiment

## Purpose
Understand what customers praise, dislike, expect, and compare about competitors.

## Business Outcome
Improve competitive decisions through evidence-backed competitor customer sentiment, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor customer sentiment and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Gather current reviews, public support/community discussions, and customer-alternative evidence with source/date/product context.
2. [DETERMINISTIC] Deduplicate syndicated reviews and identify source/sample limitations.
3. [AI] Extract aspect-level strengths, weaknesses, complaints, desired outcomes, switching reasons, and exact comparison language.
4. [HYBRID] Separate high-frequency minor issues from lower-frequency severe decision drivers.
5. [AI] Compare across competitors and relevant customer segments where evidence permits.
6. [HYBRID] Publish competitor-specific Insights; contribute broader customer-market observations to Customer Intelligence without claiming our customers share them.
