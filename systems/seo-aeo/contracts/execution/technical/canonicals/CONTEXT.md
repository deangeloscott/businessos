---
id: seo.execution.technical.canonicals
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
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Canonicals

## Purpose
Consolidate duplicate/near-duplicate URL signals without suppressing legitimately distinct pages.

## Business Outcome
Improve valuable organic discovery through canonicals, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Canonicals**, or when an authorized incident response requires it.

## Process
1. [AI] Cluster duplicate and near-duplicate URLs; identify intended primary version based on business/user purpose.
2. [AI] Compare rel=canonical, redirects, sitemap URLs, internal links, hreflang, host/protocol, and content signals.
3. [AI] Identify contradictions, canonical loops/chains, and improper cross-market/page-type canonicals.
4. [HYBRID] Choose consolidation method: redirect, canonical hint, removal, noindex, parameter handling, or content differentiation.
5. [HYBRID] Align internal links, sitemaps, and other signals with intended primary URL.
6. [HYBRID] Verify source/destination and monitor selected canonical/index behavior.

## Verification
- Test affected URL sets and rollback path before broad deployment; verify crawl/index behavior afterward.


