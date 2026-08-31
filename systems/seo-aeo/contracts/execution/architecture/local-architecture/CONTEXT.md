---
id: seo.execution.architecture.local-architecture
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
  - crawler.run
  optional:
  - cms.page.read
  - cms.page.update
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Local Site Architecture

## Purpose
Represent locations and service areas without producing thin, duplicative doorway pages.

## Business Outcome
Improve valuable organic discovery through local site architecture, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Local Site Architecture**, or when an authorized incident response requires it.

## Process
1. [AI] Identify actual locations, service areas, franchises, services, and market-specific differences.
2. [AI] Determine which combinations have distinct user value and sufficient business justification for dedicated pages.
3. [HYBRID] Design location hierarchy, find-a-location paths, service-to-location relationships, breadcrumbs, and local entity markup needs.
4. [HYBRID] Specify unique factual content requirements: address/service area, hours, services, staff, reviews, proof, directions, local policies, etc.
5. [HYBRID] Prevent bulk creation of location-service permutations without unique value.
6. [HYBRID] Verify canonical/internal-link/local-profile consistency and define SEO monitoring for local discovery/conversion outcomes.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


