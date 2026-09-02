---
id: seo.incidents.mass-deindexing
type: incident
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
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Mass Deindexing Incident

## Purpose
Respond to unexpected loss of indexed/served pages across a material site segment.

## Business Outcome
Improve valuable organic discovery through mass deindexing incident, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run immediately when monitoring or an operator identifies a plausible **mass deindexing incident**. Incident routing overrides normal optimization until containment is complete.

## Process
1. [DETERMINISTIC] Validate index observations and define affected templates/directories/markets plus first-known time.
2. [INTEGRATION] Check status/access, robots/noindex, canonicals, redirects, sitemaps, rendering, authentication, deployment/config changes, and security.
3. [AI] Compare intended versus observed state and identify common root cause before per-URL actions.
4. [HYBRID] Immediately reverse accidental blocking/noindex/redirect/canonical changes when authorized and safe.
5. [DETERMINISTIC] Restore discovery/internal-link/sitemap signals and use supported notification/diagnostic tools appropriately.
6. [HYBRID] Monitor re-crawl/reindex recovery and close only after stable intended state or explicit accepted outcome.


