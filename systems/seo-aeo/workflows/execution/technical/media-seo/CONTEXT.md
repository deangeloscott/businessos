---
id: seo.execution.technical.media-seo
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
# Media Seo

## Purpose
Make important image/video assets discoverable, descriptive, performant, and connected to relevant pages.

## Business Outcome
Improve valuable organic discovery through media seo, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Media Seo**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory high-value media, host/delivery method, surrounding pages, and business purpose.
2. [INTEGRATION] Check crawl access, surrounding context, alt/caption text where appropriate, dimensions, file delivery, lazy loading, and page relevance.
3. [HYBRID] For video, verify primary playable content, thumbnail availability, metadata/structured data where supported, and transcript/context when useful.
4. [HYBRID] Optimize media weight without degrading quality needed for conversion/trust.
5. [HYBRID] Track image/video discovery surfaces when material.


