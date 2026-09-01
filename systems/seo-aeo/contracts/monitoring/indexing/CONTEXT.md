---
id: seo.monitoring.indexing
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
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
updates:
  SEOAssetState:
  - organic_performance
---
# Indexing Monitoring

## Purpose
Review priority assets for unexpected changes in accessibility, canonical, indexed, and serving states without turning AURA into an index polling runtime.

## Business Outcome
Keep indexability evidence current enough to detect material asset/site problems while distinguishing expected propagation and observable uncertainty from real defects.

## Run When
Use for a bounded indexing check when the user requests it, saved monitoring intent indicates another check would be useful, or a publication/migration/removal/visibility change warrants reinspection. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve current crawl/index/serving evidence for decision-relevant priority or recently changed assets using the available search/crawl/CMS capabilities.
2. [HYBRID] Compare intended Asset/SEOAssetState with response behavior, directives, canonical, sitemap/internal-link, and observable index/serving state.
3. [AI] Distinguish isolated URL issues from shared template/site patterns and preserve uncertainty where the external surface is not directly observable.
4. [AI] Account for reasonable propagation windows after publication, migration, or removal before treating a mismatch as a persistent problem.
5. [AI] Decide whether a material mismatch warrants deeper indexing diagnosis, a sitewide Incident, an Opportunity, or simply a state update. These are optional next meanings/methods, not automatic routes.
6. [HYBRID] Preserve the useful last-known-good/current state and evidence relationships when future diagnosis or comparison benefits from them.

## Verification
- Claimed index/crawl problems are supported by observable evidence appropriate to the surface.
- Semantic severity/materiality remains model judgment.
- Saved cadence/checkpoint intent never proves an automatic polling job exists.
