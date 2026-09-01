---
id: seo.intelligence.organic-competition.movement-monitoring
type: playbook
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
writes:
- OrganicCompetitorState
- MetricObservation
- Observation
- Competitor
capabilities:
  required:
  - search.serp.read
  optional:
  - ai_answer.observe
  - backlink.read
  - research.web.read
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Competitor Movement Monitoring

## Purpose
Detect material changes in competitor visibility, assets, authority, answers, reputation, and offers.

## Business Outcome
Improve valuable organic discovery through competitor movement monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring competitor intelligence when **competitor movement monitoring** is needed to explain competitive visibility or identify gaps.

## Process
1. [HYBRID] Refresh weighted search/answer visibility and high-priority competitor asset observations.
2. [HYBRID] Detect new pages, major revisions, site migrations, acquired/lost references, review/local changes, new offers, and repeated rank/citation gains.
3. [HYBRID] Distinguish provider noise/normal volatility from sustained material movement.
4. [AI] Compare changes with owned performance to identify competitive displacement versus market-wide shifts.
5. [HYBRID] Create Opportunities or strategic alerts only when the change affects business-relevant demand or reveals a useful tactic/hypothesis.
6. [HYBRID] Feed novel tactics to SEO ecosystem evidence assessment rather than automatically copying them.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


