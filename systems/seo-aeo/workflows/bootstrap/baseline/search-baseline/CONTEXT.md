---
id: seo.bootstrap.baseline.search-baseline
type: workflow
owner_system: seo-aeo
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- Effective Capability Profile
- Available search analytics local authority AI
updates:
  SEOAssetState:
  - organic_performance
  - technical fields crawl indexability index structured data as applicable
  - internal_authority external_authority
---
# Search Performance Baseline

## Purpose
Establish current organic query/page/surface performance and business-value linkage.

## Business Outcome
Improve valuable organic discovery through search performance baseline, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial baseline, scheduled re-baseline, or after a material site/business change when **search performance baseline** must be re-observed.

## Process
1. [HYBRID] Ingest the longest reliable recent history plus comparison windows available from search-performance/rank providers.
2. [DETERMINISTIC] Normalize query/page/date/country/device/search-appearance/surface data and join target assets.
3. [DETERMINISTIC] Compute impressions, clicks, CTR, average position/visibility observations and trends without over-interpreting averages.
4. [DETERMINISTIC] Join analytics/conversion/value data where possible; label proxy-only segments.
5. [AI] Segment branded/nonbranded, intent, topic, audience, awareness stage, market, and asset type where classification is confident.
6. [HYBRID] Write baseline distributions and initial threshold models for later anomaly/opportunity detection.

## Decisions / Routing
- Route → SEO Organic Demand Intelligence when baseline evidence needs demand interpretation.
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.


