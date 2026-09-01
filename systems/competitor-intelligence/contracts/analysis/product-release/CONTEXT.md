---
id: competitor.analysis.product-release
type: playbook
owner_system: competitor-intelligence
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
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Product & Release Intelligence

## Purpose
Track material competitor product/service launches, feature movement, deprecations, and delivery changes.

## Business Outcome
Improve competitive decisions through evidence-backed product & release intelligence, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current product & release intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Monitor product pages, changelogs, release notes, documentation, announcements, and credible demonstrations.
2. [DETERMINISTIC] Compare with prior state and identify net-new, changed, deprecated, or repackaged capability.
3. [AI] Distinguish announced capability from generally available capability and marketing claim from observed behavior.
4. [HYBRID] Assess affected audience/use case and potential strategic significance.
5. [AI] Connect change to pricing, positioning, hiring, partnerships, and customer sentiment when evidence exists.
6. [HYBRID] Create/update competitor strategic Insights and downstream relevance tags.
