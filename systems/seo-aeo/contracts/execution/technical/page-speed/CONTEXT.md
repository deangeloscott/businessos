---
id: seo.execution.technical.page-speed
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
---
# Page Speed

## Purpose
Reduce unnecessary latency and page weight beyond named CWV thresholds.

## Business Outcome
Improve valuable organic discovery through page speed, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Page Speed**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Capture network waterfall, server timing, asset weight, caching/compression, render-blocking resources, third-party scripts, media, fonts, and API latency.
2. [HYBRID] Rank bottlenecks by actual user path and template leverage.
3. [HYBRID] Remove, replace, defer, preload, compress, cache, resize, or optimize only where technically appropriate.
4. [AI] Test functionality, analytics, ads/consent, and visual regressions.
5. [INTEGRATION] Deploy and compare before/after representative journeys.


