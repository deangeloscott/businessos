---
id: seo.intelligence.organic-competition.discover-answer
type: playbook
version: 1.1.0
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
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# Answer Competitor / Source Discovery

## Purpose
Identify/search-analyze organic competitors and answer sources without maintaining a duplicate broad business competitor profile.

## Business Outcome
Improve valuable organic discovery through answer competitor / source discovery, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring competitor intelligence when **answer competitor / source discovery** is needed to explain competitive visibility or identify gaps.

## Process
1. [HYBRID] Sample weighted prompt clusters across configured answer surfaces.
2. [AI] Extract recommended/mentioned entities and cited domains/pages with observation context.
3. [AI] Aggregate business-value-weighted mention/recommendation/citation coverage.
4. [INTEGRATION] Classify competitor brands versus neutral authorities, communities, databases, publishers, and marketplaces.
5. [HYBRID] Link to OrganicCompetitorState and canonical Competitor refs when the same entity appears, but preserve answer-source role.
6. [AI] Create/update OrganicCompetitorState records and feed source-gap analysis.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


