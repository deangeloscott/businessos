---
id: seo.execution.technical.mobile
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
# Mobile

## Purpose
Ensure mobile users/crawlers receive complete, usable core content and metadata.

## Business Outcome
Improve valuable organic discovery through mobile, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Mobile**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Compare mobile and desktop content, links, metadata, structured data, media, and directives.
2. [HYBRID] Check responsive layout, viewport, intrusive overlays, touch targets, form usability, and interaction blockers.
3. [HYBRID] Confirm mobile implementation does not omit important text, links, images, video, structured data, or alternate/canonical relationships.
4. [HYBRID] Fix parity/usability defects and re-test representative templates.
5. [HYBRID] Monitor mobile-specific performance and conversions.


