---
id: seo.monitoring.local
type: playbook
version: 1.1.0
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
schedule:
  class: recurring
  default: daily
  configurable: true
evidence_inputs:
- location/profile data, local-result observations, and local competitors
updates:
  SEOAssetState:
  - organic_performance
---
# Local Discovery Monitoring

## Purpose
Track profile state, local visibility, local actions, location pages, citations, and location-specific issues.

## Business Outcome
Improve valuable organic discovery through local discovery monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **local discovery monitoring**.

## Process
1. [HYBRID] Refresh local profiles, visibility observations, local-site assets, reviews, citations, and business actions by location.
2. [HYBRID] Detect edits/drift, duplicates, suspensions, hours/location changes, category/service changes, and visibility shifts.
3. [HYBRID] Segment query/service/location/geographic observation points and separate proximity effects where possible.
4. [DETERMINISTIC] Join calls/bookings/directions/site actions and qualified local conversions.
5. [HYBRID] Route normal gaps to Local Opportunities and profile suspensions/major identity failures to Incidents.
6. [HYBRID] Roll up multi-location results while preserving individual underperformance.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


