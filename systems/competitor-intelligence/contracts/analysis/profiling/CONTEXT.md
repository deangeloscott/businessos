---
id: competitor.analysis.profiling
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
  - crawler.run
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
subcontracts:
  required:
  - competitor.research.adaptive-source-coverage
  - competitor.research.source-map
  - competitor.research.baseline-snapshot
  - competitor.analysis.strength-weakness
---
# Competitor Profile

## Purpose
Build a current evidence-backed competitor state without turning the summary object into a copy of raw evidence.

## Business Outcome
Improve competitive decisions through evidence-backed competitor profile, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor profile and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Retrieve current authoritative competitor-owned product/service, pricing, offer, positioning, and company information plus relevant third-party evidence.
2. [DETERMINISTIC] Snapshot/version important source pages and compare with prior state where available.
3. [AI] Extract factual state separately from strategic interpretation; retain exact source references.
4. [HYBRID] Reconcile conflicting sources by fact type, authority, freshness, and directness rather than defaulting to one source hierarchy.
5. [AI] Summarize current products, audiences, positioning, offers, strengths/weaknesses hypotheses, and notable recent changes.
6. [HYBRID] Attach confidence and unanswered questions to the Competitor record; keep detailed evidence in Observations/Insights.
7. [DETERMINISTIC] Update last_reviewed and emit competitor.updated when material.
