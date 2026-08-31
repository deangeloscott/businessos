---
id: seo.execution.indexing.publish-discovery
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
  - search.index.inspect
  optional:
  - search.index.request
  - cms.page.read
  - crawler.run
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Publish and Discovery Signaling

## Purpose
Ensure newly published or materially changed assets are accessible, linked, represented in discovery files, and handed to monitoring.

## Business Outcome
Improve valuable organic discovery through publish and discovery signaling, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Publish and Discovery Signaling**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Confirm final production URL, status, canonical, index directive, rendering, and required content exist.
2. [HYBRID] Update internal links/navigation/hubs when the asset should be discoverable from the site.
3. [HYBRID] Update XML sitemap or other supported discovery feeds when applicable and remove obsolete URL variants.
4. [HYBRID] Use supported URL-notification/submission capabilities when appropriate; do not assume submission guarantees indexing.
5. [INTEGRATION] Record publish/change time and expected search/answer/local surfaces.
6. [HYBRID] Create index-status monitoring checkpoints and route verification.


