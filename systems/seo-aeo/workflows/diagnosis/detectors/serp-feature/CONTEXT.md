---
id: seo.diagnosis.detectors.serp-feature
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
context:
- AudienceSegment
- Market
- Objective
- Offer
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# SERP / Discovery Feature Opportunity Detector

## Purpose
Find valuable result formats or surface features the brand could legitimately qualify for or better serve.

## Business Outcome
Identify useful discovery-feature opportunities without assuming feature eligibility, visibility, or ownership can be guaranteed.

## Run When
Use when fresh relevant result-surface observations exist and the user/model needs to diagnose a **SERP / discovery feature opportunity**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [AI] Inspect high-value result ecosystems and identify recurring local, image, video, product, rich-result, discussion, news, or other feature types.
2. [AI] Judge whether the feature aligns with actual user intent and whether the business has or could legitimately create useful eligible content/data.
3. [HYBRID] Inspect current owned eligibility, structured information, media, product/local data, and relevant competitor/source examples.
4. [AI] Identify the most relevant content/media/structured-data/local/product/technical method when useful; do not route execution automatically.
5. [AI] Create/update an Opportunity only when feature-specific evidence and business value justify it; do not imply guaranteed feature ownership.
6. [HYBRID] Define later observation/evaluation evidence if a future intervention is performed. Runtime scheduling and execution remain external to AURA.

## Verification
- Feature presence, eligibility, user value, and likely business effect remain distinct.
- A detected feature does not itself authorize or require an intervention.
