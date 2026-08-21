---
id: seo.execution.architecture.crawl-depth
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
  - cms.page.read
  - cms.page.update
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Crawl Depth Optimization

## Purpose
Reduce unnecessary path depth for high-value assets while preserving meaningful information architecture.

## Business Outcome
Improve valuable organic discovery through crawl depth optimization, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Crawl Depth Optimization**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Measure shortest internal-link path from discoverable entry points to each indexable asset.
2. [INTEGRATION] Join depth with business value, demand, traffic, index state, and crawl observations.
3. [HYBRID] Flag valuable assets that are unusually deep or reachable only through weak/conditional navigation.
4. [AI] Diagnose whether depth is caused by architecture, orphaning, pagination, filters, JS rendering, or intentional rarity.
5. [HYBRID] Choose internal-link/navigation/hub changes rather than indiscriminately flattening the whole site.
6. [HYBRID] Verify new paths and define SEO monitoring for crawl/index/performance effects.


