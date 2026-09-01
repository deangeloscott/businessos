---
id: seo.monitoring.ranking-visibility
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
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
  - local_profile.read
evidence_inputs:
- rank/visibility time series query-page mappings
updates:
  SEOAssetState:
  - organic_performance
---
# Ranking and Search Visibility Monitoring

## Purpose
Track material query/page/cluster visibility changes across relevant search surfaces.

## Business Outcome
Improve valuable organic discovery through ranking and search visibility monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **ranking and search visibility monitoring**.

## Process
1. [HUMAN] Refresh configured first-party search and rank observations at the approved cadence.
2. [HYBRID] Aggregate by value-weighted query cluster, asset, topic, market, device, branded/nonbrand, and result type.
3. [HYBRID] Compare configurable rolling/prior/YoY windows and detect sustained changes beyond noise.
4. [DETERMINISTIC] Join demand and SERP/result changes so position shifts are not interpreted without context.
5. [HYBRID] Route gains to learning and declines to ranking-decay/root-cause workflows.
6. [HYBRID] Maintain historical state rather than overwriting prior observations.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.

## Verification
- Separate demand, ranking, indexing, SERP-layout, seasonality and tracking effects before assigning a cause.


