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
Detect and explain material local visibility gap early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **local visibility gap**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [DETERMINISTIC] Join local query/map observations, profiles, location pages, reviews, citations/links, conversions, and canonical location/service data.
2. [AI] Identify absent/weak high-value query coverage, incomplete/incorrect profiles, location-page gaps, review deficits, inconsistent identity, or competitor prominence.
3. [HYBRID] Separate uncontrollable distance/proximity effects from controllable relevance/prominence/asset factors.
4. [HYBRID] Create specific routed Opportunities rather than 'improve local SEO'.
5. [HYBRID] Prioritize by expected local business action/value and location capacity.
6. [HYBRID] Define downstream measurement using calls/bookings/directions/site conversions, with visibility as a supporting metric.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


