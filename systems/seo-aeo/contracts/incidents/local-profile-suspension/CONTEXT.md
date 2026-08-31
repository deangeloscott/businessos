---
id: seo.incidents.local-profile-suspension
type: incident
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
- Incident
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.index.inspect
  - crawler.run
  - cms.page.read
events:
  consumes:
  - none
  emits:
  - seo.incident.updated
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Local Profile Suspension Incident

## Purpose
Handle loss/restriction of an important local business profile without making risky repeated edits.

## Business Outcome
Improve valuable organic discovery through local profile suspension incident, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run immediately when monitoring or an operator identifies a plausible **local profile suspension incident**. Incident routing overrides normal optimization until containment is complete.

## Process
1. [HYBRID] Confirm affected profile/location, notice/reason if provided, recent profile/site/entity changes, and business eligibility facts.
2. [HYBRID] Freeze nonessential profile automation and preserve canonical location/business evidence.
3. [HYBRID] Audit name/address/service-area/category/ownership/duplicate/website data against actual business facts and current platform requirements.
4. [HYBRID] Correct factual issues through authorized channels and assemble verifiable evidence; avoid repeated speculative changes.
5. [HYBRID] Use the platform's official reinstatement/appeal process when applicable and track correspondence/status.
6. [HYBRID] After restoration, verify profile/site/citation consistency and document root cause/prevention.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


