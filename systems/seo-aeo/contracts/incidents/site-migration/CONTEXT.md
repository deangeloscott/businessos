---
id: seo.incidents.site-migration
type: incident
version: 1.1.0
owner_system: seo-aeo
risk: high
autonomy_ceiling: 2
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- ActionPacket
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
---
# Site Migration Incident / Command

## Purpose
Coordinate planned or emergency domain/URL/platform migrations as a controlled high-risk program.

## Business Outcome
Improve valuable organic discovery through site migration incident / command, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run immediately when monitoring or an operator identifies a plausible **site migration incident / command**. Incident routing overrides normal optimization until containment is complete.

## Process
1. [HYBRID] Freeze a complete pre-migration asset/URL/performance/backlink/index baseline and define mapping ownership.
2. [AI] Create one-to-one/intent-correct redirect and canonical/hreflang/sitemap/internal-link plans; identify intentional removals/consolidations.
3. [DETERMINISTIC] Validate staging without exposing accidental indexable duplicates and preserve analytics/conversion tracking.
4. [HYBRID] Launch in controlled sequence, verify status/redirect/canonical/robots/render/tracking across representative and high-value URLs.
5. [HYBRID] Monitor old/new index/search/traffic/conversion/link behavior daily initially and repair mapping/template errors.
6. [HYBRID] Keep migration Change Events/Incident open until stabilization criteria are met.

## Verification
- Test affected URL sets and rollback path before broad deployment; verify crawl/index behavior afterward.


