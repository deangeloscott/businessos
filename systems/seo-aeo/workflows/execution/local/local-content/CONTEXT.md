---
id: seo.execution.local.local-content
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
- OrganicDemandUnit
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- location/profile data, local-result observations, and local competitors
- records topic intent evidence
---
# Local Content

## Purpose
Create market-specific information only where local differences, events, expertise, or customer needs justify it.

## Business Outcome
Improve valuable organic discovery through local content, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Local Content**, or when an authorized incident response requires it.

## Process
1. [AI] Identify location-specific questions, regulations, seasonal needs, events, case studies, datasets, services, comparisons, or community information.
2. [DETERMINISTIC] Validate that the topic serves real local users and maps to a business/customer journey need.
3. [HYBRID] Select the correct destination: location page enhancement, standalone resource, event/news item, or no new page.
4. [AI] Research local facts from authoritative/current sources and distinguish evergreen from time-sensitive facts.
5. [HYBRID] Create content with unique local evidence and appropriate internal/local-profile relationships.
6. [HYBRID] Expire/update time-sensitive content and measure qualified local discovery and conversion impact.


