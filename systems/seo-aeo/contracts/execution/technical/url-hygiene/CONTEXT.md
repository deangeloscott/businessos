---
id: seo.execution.technical.url-hygiene
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
# Url Hygiene

## Purpose
Keep URLs stable, canonical, and free from uncontrolled variant explosion.

## Business Outcome
Improve valuable organic discovery through url hygiene, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Url Hygiene**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory URL patterns and parameter combinations.
2. [AI] Identify session, tracking, sort/filter, search, calendar, printer, duplicate path, and generated variants.
3. [AI] Determine which variants represent distinct useful demand versus operational noise.
4. [INTEGRATION] Define canonical/index/crawl rules and stable URL-generation behavior.
5. [HYBRID] Avoid URL changes solely for cosmetic keyword reasons when current URLs are stable and functional.
6. [HYBRID] For necessary URL changes, invoke redirects plus link/sitemap/canonical migration controls.


