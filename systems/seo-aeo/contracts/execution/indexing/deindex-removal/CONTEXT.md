---
id: seo.execution.indexing.deindex-removal
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
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Deindexing and Removal

## Purpose
Remove or consolidate URLs from discovery/indexes intentionally while protecting users, links, legal requirements, and replacements.

## Business Outcome
Improve valuable organic discovery through deindexing and removal, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Deindexing and Removal**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Confirm business/legal reason and desired final state: redirect, gone, noindex, access restriction, temporary removal, or content update.
2. [AI] Inventory traffic, conversions, backlinks, internal links, canonicals, hreflang, sitemap references, and dependent assets.
3. [HYBRID] Select the correct method based on whether a replacement exists and whether users should still access the content.
4. [HYBRID] Route destructive or high-impact changes through required approval and preserve previous content/URL map.
5. [INTEGRATION] Execute changes, update internal references/sitemaps, and use supported removal tools only for their intended temporary/specific purposes.
6. [HYBRID] Define SEO monitoring for old/new URL behavior, traffic/link effects, and unexpected index persistence; rollback/escalate if requirements were wrong.


