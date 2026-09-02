---
id: seo.execution.technical.crawl-budget
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Crawl Budget

## Purpose
Improve discovery efficiency on very large, complex, or frequently changing sites when crawl capacity or crawl allocation is a demonstrated constraint.

## Business Outcome
Reduce crawler effort spent on low-value spaces when doing so can materially improve discovery or refresh of important Assets.

## Run When
Use only when log, crawl, index, freshness, or other evidence indicates crawl capacity/allocation may actually be limiting important discovery. Do not assume every site has a crawl-budget problem.

## Process
1. Verify the suspected constraint using the strongest available evidence, such as crawler logs, crawl frequency, discovery/update latency, index behavior, server constraints, or large low-value crawl spaces.
2. Identify the main sources of wasted crawl effort: infinite/duplicate spaces, unstable URLs, faceted combinations, calendars, repetitive parameters, soft errors, redirect chains, or other patterns actually present.
3. Measure or estimate important-page discovery/update latency and distinguish crawl allocation from unrelated indexing, content, rendering, or demand problems.
4. Reduce waste using the smallest appropriate mechanisms—architecture, URL/facet control, canonical consistency, response correctness, sitemap quality, internal linking, rendering changes, or another sound method—without blocking useful customer states or valuable demand.
5. Re-check crawler behavior, important-page freshness/discovery, server impact, and unintended exclusions after material changes.

## Proportionate Scope
Use representative logs/patterns and high-value Assets first. Expand toward broader log/crawl analysis when site scale, heterogeneity, or uncertainty prevents a reliable conclusion. Do not optimize crawl volume for its own sake when important content is already discovered and refreshed adequately.

## Verification
- A real crawl-capacity/allocation constraint is supported before optimization begins.
- Important discovery/indexing problems are not misdiagnosed as crawl budget merely because the site is large.
- Waste reduction does not remove useful user navigation or valuable unique URLs.
