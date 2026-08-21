---
id: seo.execution.technical.site-migration
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
# Site Migration

## Purpose
Plan and execute domain/CMS/architecture/URL migrations without avoidable discovery or attribution loss.

## Business Outcome
Improve valuable organic discovery through site migration, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Site Migration**, or when an authorized incident response requires it.

## Process
1. [AI] Freeze pre-migration URL inventory, search/analytics/revenue baseline, backlinks, canonicals, sitemaps, directives, key templates, and tracking.
2. [AI] Create one-to-one redirect map to closest equivalents and identify intentional removals.
3. [DETERMINISTIC] Validate staging for accidental block/noindex, content parity, links, metadata, structured data, tracking, performance, forms, and server behavior.
4. [AI] Limit unrelated changes where practical so post-launch diagnosis remains possible.
5. [HYBRID] Launch with redirects, canonicals, internal links, sitemaps, ownership/verification, analytics, and feeds updated.
6. [INTEGRATION] Crawl immediately and define SEO monitoring for old/new URLs, index state, errors, traffic, conversion, backlinks, and logs.
7. [HYBRID] Maintain redirects long enough for users/crawlers/signals; do not remove on an arbitrary short schedule.
8. [HYBRID] Run migration postmortem and resolve residual orphan/redirect/index issues.

## Verification
- Test affected URL sets and rollback path before broad deployment; verify crawl/index behavior afterward.


