---
id: seo.diagnosis.detectors.local-gap
type: detector
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
writes:
- Opportunity
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.serp.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- location/profile data, local-result observations, and local competitors
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Local Visibility Gap Detector

## Purpose
Find material local discovery/conversion gaps by location, service, query, profile, or reputation state.

## Business Outcome
Explain controllable local-discovery gaps in the context of actual customer/business value rather than treating every visibility difference as an SEO problem.

## Run When
Use when fresh relevant local observations exist and the user/model needs to diagnose a **local visibility gap**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Relate local query/map observations, profiles, location pages, reviews, citations/links, conversions, and established location/service context.
2. [AI] Identify absent/weak high-value query coverage, incomplete/incorrect profiles, location-page gaps, review deficits, inconsistent identity, or competitor prominence.
3. [HYBRID] Separate uncontrollable distance/proximity effects from controllable relevance/prominence/Asset factors.
4. [AI] Define a specific intervention hypothesis only where the gap appears controllable; avoid generic “improve local SEO” recommendations.
5. [AI] Create/update an Opportunity only when expected local customer/business value and location capacity justify attention, without fabricating uplift.
6. [HYBRID] Define later evaluation using calls/bookings/directions/site conversions where trustworthy, with visibility as supporting evidence.

## Verification
- Verify location eligibility and established business facts before any public profile/location change.
- Local visibility difference alone does not prove a controllable opportunity.
