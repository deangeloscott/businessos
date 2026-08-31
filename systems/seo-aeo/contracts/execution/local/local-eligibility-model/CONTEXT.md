---
id: seo.execution.local.local-eligibility-model
type: playbook
version: 1.1.0
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
# Local Eligibility and Market Model

## Purpose
Determine whether local discovery is relevant and represent locations/service areas/franchise relationships accurately.

## Business Outcome
Improve valuable organic discovery through local eligibility and market model, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Local Eligibility and Market Model**, or when an authorized incident response requires it.

## Process
1. [AI] Identify physical locations, staffed locations, service areas, delivery areas, franchises, virtual-only operations, and market boundaries.
2. [DETERMINISTIC] Validate what customers can actually do at/through each location and which addresses may legitimately be represented publicly.
3. [AI] Map services/products and conversion actions by location/market; identify differences in hours, availability, licensing, pricing, or language.
4. [HYBRID] Create canonical location/entity records and relationships to owned pages and local profiles.
5. [AI] Classify local strategy type: single-location, multi-location, service-area, franchise, hybrid, or not applicable.
6. [HYBRID] Flag ambiguous eligibility or platform-specific representation questions for evidence/review before profile changes.


