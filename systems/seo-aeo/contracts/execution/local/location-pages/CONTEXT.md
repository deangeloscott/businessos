---
id: seo.execution.local.location-pages
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - local_profile.read
  optional:
  - local_profile.update
  - review.read
  - research.web.read
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Location Page Optimization

## Purpose
Create or improve location pages that provide unique local utility and connect local discovery to conversion.

## Business Outcome
Improve valuable organic discovery through location page optimization, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Location Page Optimization**, or when an authorized incident response requires it.

## Process
1. [AI] Map each legitimate location/service area to local intents, services, offers, proof, and conversion paths.
2. [HYBRID] Audit existing pages for unique facts, address/service area, hours, staff/team, amenities, directions, parking/access, local testimonials/reviews, images, FAQs, policies, and service availability where applicable.
3. [AI] Identify duplicated boilerplate and missing local evidence; determine whether a separate page is justified.
4. [HYBRID] Create/update content, metadata, internal links, structured data, and local-profile website links while preserving factual accuracy.
5. [HYBRID] Ensure pages are useful to humans even without search traffic and avoid doorway-style permutations.
6. [HYBRID] Verify indexability, local entity consistency, conversions, and local visibility.


