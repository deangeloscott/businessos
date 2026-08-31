---
id: seo.monitoring.ctr
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
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
  - local_profile.read
schedule:
  class: recurring
  default: daily
  configurable: true
evidence_inputs:
- query-page impressions clicks CTR position SERP
updates:
  SEOAssetState:
  - organic_performance
---
# CTR Monitoring

## Purpose
Track click-through behavior relative to query/page position and result context.

## Business Outcome
Improve valuable organic discovery through ctr monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **CTR monitoring**.

## Process
1. [DETERMINISTIC] Ingest impressions/clicks/CTR/position by query-page-market-device and validate data health.
2. [HYBRID] Update expected CTR distributions from sufficient brand data while retaining configurable cold-start defaults.
3. [HYBRID] Flag material under/overperformance adjusted for brand/nonbrand, intent, position, and result-feature context where observable.
4. [HYBRID] Detect sudden CTR changes without position movement as possible snippet/SERP/brand/reputation changes.
5. [HYBRID] Route controllable underperformance to low-CTR detector and useful gains to SEO Domain Learning or Core Business Learning, as scope warrants.
6. [HYBRID] Do not optimize CTR if the resulting clicks are low-quality or harm downstream business outcomes.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Compare CTR only against a relevant position/query/device/market expectation; do not mistake rank movement for presentation lift.
- Create an Opportunity only when the gap is material and plausibly controllable.


