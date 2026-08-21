---
id: seo.execution.indexing.index-troubleshooting
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
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Indexing Troubleshooting

## Purpose
Diagnose why a material asset is not being indexed/served rather than repeatedly resubmitting it.

## Business Outcome
Improve valuable organic discovery through indexing troubleshooting, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Indexing Troubleshooting**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Verify URL response, robots access, meta/X-Robots directives, canonical, redirects, rendering, authentication, and availability.
2. [HYBRID] Inspect sitemap/internal-link discovery and whether the asset is orphaned or inconsistently referenced.
3. [HYBRID] Check duplicate/near-duplicate clusters, canonical alternatives, thin/low-value patterns, soft errors, and sitewide quality/index patterns.
4. [INTEGRATION] Review available platform diagnostics/log/crawl evidence and timing relative to changes.
5. [HYBRID] Select the smallest root-cause intervention: technical fix, canonical/link alignment, content differentiation, consolidation, wait/monitor, or escalation.
6. [HYBRID] Verify changes and return to index-status monitoring; do not promise indexing.


