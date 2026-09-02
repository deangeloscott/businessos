---
id: seo.execution.local.local-media
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Local Media Optimization

## Purpose
Maintain useful, accurate visual assets for local profiles and location pages.

## Business Outcome
Improve valuable organic discovery through local media optimization, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Local Media Optimization**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory profile/site photos and videos by location, subject, freshness, rights, and quality.
2. [AI] Identify missing customer-useful views such as exterior/entrance, interior, team, products/services, accessibility, parking, work examples, or amenities.
3. [HYBRID] Collect or request authorized assets; do not fabricate documentary imagery of a real location.
4. [HYBRID] Prepare accurate filenames/alt/context/captions where relevant and platform-supported metadata.
5. [INTEGRATION] Publish through authorized profile/site channels and verify correct location association.
6. [AI] Define SEO monitoring for stale/incorrect user-generated or owner media and route reputation/content issues appropriately.


