---
id: seo.execution.technical.faceted-navigation
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
---
# Faceted Navigation

## Purpose
Control combinatorial filter URLs while preserving valuable filtered landing pages.

## Business Outcome
Improve valuable organic discovery through faceted navigation, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Faceted Navigation**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] Inventory facets, parameter combinations, crawl paths, and corresponding demand.
2. [AI] Classify combinations as valuable unique landing pages, useful-but-nonindexable user states, or crawl/index waste.
3. [HYBRID] Define deterministic allow/index/canonical/noindex/block rules that preserve user navigation.
4. [HYBRID] Create dedicated optimized landing pages for high-value combinations when warranted.
5. [HYBRID] Ensure internal links and sitemaps do not explode low-value variants.
6. [INTEGRATION] Crawl-test combinatorial boundaries and index behavior after deployment.


