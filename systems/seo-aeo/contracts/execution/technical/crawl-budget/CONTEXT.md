---
id: seo.execution.technical.crawl-budget
type: playbook
owner_system: seo-aeo
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
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Crawl Budget

## Purpose
Improve discovery efficiency on very large or frequently changing sites when crawl capacity is a demonstrated constraint.

## Business Outcome
Improve valuable organic discovery through crawl budget, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Crawl Budget**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Confirm crawl-budget symptoms using logs, crawl, and index evidence; do not assume every site has a budget problem.
2. [AI] Identify low-value infinite/duplicate spaces, traps, unstable URLs, facets, calendars, and repetitive parameters.
3. [HYBRID] Measure important-page discovery/update latency.
4. [AI] Reduce waste through architecture, parameter/facet control, canonical consistency, response correctness, sitemap quality, and internal linking.
5. [HYBRID] Define SEO monitoring for crawler behavior, server load, and important-page freshness after changes.


