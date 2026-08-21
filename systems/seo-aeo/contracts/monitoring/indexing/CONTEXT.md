---
id: seo.monitoring.indexing
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
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
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
schedule:
  class: recurring
  default: daily
  configurable: true
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
updates:
  SEOAssetState:
  - organic_performance
---
# Indexing Monitoring

## Purpose
Track priority assets for unexpected changes in accessibility, canonical, indexed, and serving states.

## Business Outcome
Improve valuable organic discovery through indexing monitoring, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run on the configured cadence or event trigger for **indexing monitoring**.

## Process
1. [INTEGRATION] Refresh provider/index/crawl observations for priority and recently changed assets.
2. [HYBRID] Compare intended Asset / SEOAssetState state with response, directives, canonical, sitemap/internal-link, and observable index/serving state.
3. [HYBRID] Detect individual issues versus broad site/template patterns.
4. [INTEGRATION] Allow expected propagation windows after publish/migration/removal before escalating.
5. [HYBRID] Route material mismatches to indexing detector; broad losses to mass-deindexing Incident.
6. [HYBRID] Preserve last-known-good state and change-event correlation.

## Decisions / Routing
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.
- Route → Core verification using SEO-specific assertions.
- Route → SEO measurement / Core OutcomeEvaluation.


