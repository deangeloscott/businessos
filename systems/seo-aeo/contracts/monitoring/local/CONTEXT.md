---
id: seo.monitoring.local
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
capabilities:
  required:
  - local_profile.read
  optional:
  - local_profile.update
  - review.read
  - research.web.read
evidence_inputs:
- location/profile data, local-result observations, and local competitors
updates:
  SEOAssetState:
  - organic_performance
---
# Local Discovery Monitoring

## Purpose
Review profile state, local visibility, local actions, location pages, citations, and location-specific issues without making AURA the local-platform monitoring runtime.

## Business Outcome
Keep local-discovery evidence current enough to identify meaningful visibility/identity problems or opportunities while preserving location-specific differences.

## Run When
Use for a bounded local-discovery check when the user requests it, saved monitoring intent indicates another review would be useful, or a material business/location/platform change warrants reinspection. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve current local profiles, visibility observations, location Assets, reviews, citations, and observable business actions for the relevant locations.
2. [AI] Identify edits/drift, duplicates, suspensions, hours/location changes, category/service changes, and visibility shifts while distinguishing direct observations from interpretation.
3. [HYBRID] Segment query/service/location/geographic observations and account for proximity effects where the evidence allows.
4. [HYBRID] Correlate calls, bookings, directions, site actions, and qualified local conversions only to the degree supported by available attribution/identity evidence.
5. [AI] Decide whether a material gap warrants a local Opportunity, profile/location correction, Incident, or deeper diagnosis. Monitoring does not route these automatically.
6. [HYBRID] Preserve useful location-level and rolled-up measurement/state while keeping underperforming locations inspectable.

## Verification
- Verify location eligibility and established business facts before changing public profile/location data.
- Local visibility, customer action, and business outcome remain separate evidence classes.
- AURA does not claim recurring execution unless the external runtime actually provides it.
