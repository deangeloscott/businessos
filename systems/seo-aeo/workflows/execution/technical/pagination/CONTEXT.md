---
id: seo.execution.technical.pagination
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
---
# Pagination

## Purpose
Keep multi-page collections and sequence states discoverable when their deeper items/content matter, without collapsing distinct pages or multiplying unnecessary URL traps.

## Business Outcome
Ensure users and crawlers can reach valuable deeper items while maintaining coherent canonical, linking, and URL behavior across paginated or infinite-scroll experiences.

## Run When
Use when pagination, load-more, infinite scroll, or other multi-page collection behavior may materially affect discovery of deeper content/items or create duplicate crawl spaces.

## Process
1. Identify the relevant paginated series, collection behavior, infinite-scroll/load-more implementation, and which deeper items/content actually need independent discovery.
2. Ensure crawl-relevant sequence states have stable reachable URLs when that is necessary for discovering the underlying content; do not create indexable pages merely because a pagination state exists.
3. Verify crawlable links or another reliable discovery path to deeper pages and item URLs without requiring interaction-only behavior that relevant crawlers cannot traverse.
4. Check canonical behavior preserves genuinely unique paginated content and does not collapse all useful sequence pages to the first page by default.
5. Keep sorts, filters, pagination parameters, internal links, and generated URLs from multiplying uncontrolled duplicate spaces; use URL Hygiene or Faceted Navigation knowledge when those patterns become the real issue.
6. Test representative early, middle, deep, boundary, and no-JavaScript/error states where they materially affect discovery or user access.

## Proportionate Scope
Inspect enough sequence depth and representative collection types to establish whether discovery remains reliable. Expand when collections are very deep, dynamically generated, or differ substantially by template.

## Verification
- Valuable deeper items/content remain discoverable.
- Unique paginated content is not incorrectly canonicalized away.
- Pagination does not create unnecessary combinatorial crawl spaces.
- The user experience remains functional independently of the SEO treatment.
