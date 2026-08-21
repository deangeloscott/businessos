---
id: seo.execution.local.map-visibility
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
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
# Map Visibility Monitoring and Optimization

## Purpose
Measure local result presence and diagnose why visibility/conversion differs by query and geography.

## Business Outcome
Improve valuable organic discovery through map visibility monitoring and optimization, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Map Visibility Monitoring and Optimization**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Define a representative local query/task set by service, intent, market, and language.
2. [DETERMINISTIC] Observe result presence across representative geographic points where data collection is legitimate/available; record timestamp and surface.
3. [DETERMINISTIC] Join visibility with profile completeness, relevance, proximity context, reviews, website relevance, citations/authority, and competitor state.
4. [HYBRID] Separate controllable relevance/prominence/asset issues from geographic distance or measurement noise.
5. [HYBRID] Create specific Opportunities for profile, website, reputation, authority, or content interventions rather than a generic 'rank maps' task.
6. [HYBRID] Measure outcome by qualified calls, direction/booking/site actions, leads, and visibility share where observable.


