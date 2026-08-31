---
id: seo.execution.technical.pagination
type: playbook
version: 1.1.0
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
# Pagination

## Purpose
Maintain discoverable multi-page sequences without losing deep items or creating duplicate traps.

## Business Outcome
Improve valuable organic discovery through pagination, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Pagination**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory paginated series and infinite-scroll behavior.
2. [HYBRID] Ensure each crawl-relevant page/state has a stable URL where content requires discovery.
3. [HYBRID] Check crawlable links to next/deeper pages and item URLs.
4. [HYBRID] Check canonical behavior does not incorrectly collapse unique paginated content.
5. [HYBRID] Ensure filters/sorts/pagination do not multiply uncontrolled duplicate spaces.
6. [HYBRID] Verify users and crawlers can reach deep items without interaction-only mechanisms.


