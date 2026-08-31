---
id: seo.execution.internal-linking.orphan-recovery
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
  - cms.page.read
  - cms.page.update
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Orphan Page Recovery

## Purpose
Find valuable assets with no meaningful internal discovery path and either reconnect, consolidate, or retire them.

## Business Outcome
Improve valuable organic discovery through orphan page recovery, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Orphan Page Recovery**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Build the set difference between known indexable/valuable assets and assets reached through navigable internal links.
2. [DETERMINISTIC] Join orphan candidates with traffic, backlinks, conversions, demand, index state, freshness, and business purpose.
3. [AI] Determine whether each candidate should remain independent, merge, redirect, noindex/remove, or receive links.
4. [HYBRID] Select contextually relevant source pages and link placements for retained pages; avoid sitewide filler links.
5. [HYBRID] Execute or prepare changes and update asset relationships.
6. [HYBRID] Re-crawl/re-render and verify that the orphan condition is resolved without creating duplicate intent.


