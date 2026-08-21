---
id: competitor.discovery.emerging-competitors
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 2
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
# Emerging Competitor Discovery

## Purpose
Detect new or previously peripheral alternatives becoming strategically relevant.

## Business Outcome
Prevent the competitive set from becoming stale as customers, technology, and category structure change.

## Run When
Run periodically or when customer alternatives, search behavior, industry events, or lost deals reveal new entities.

## Process
1. [AI] Gather candidate entities from customer alternatives, industry events, search/AEO overlap, reviews, communities, partnerships, funding/product launches, and sales evidence.
2. [DETERMINISTIC] Deduplicate entities and match to existing Competitor records.
3. [AI] Classify candidate relationship: direct, substitute, emerging, adjacent, platform, or non-competitor reference.
4. [AI] Evaluate overlap in audience, job/outcome, offer, budget, distribution, and customer consideration.
5. [HYBRID] Require stronger evidence before labeling a company a material competitor than before placing it on a watchlist.
6. [AI] Create/update Competitor records only for materially relevant entities; keep watch candidates scoped.
7. [DETERMINISTIC] Emit discovery evidence and review cadence.
