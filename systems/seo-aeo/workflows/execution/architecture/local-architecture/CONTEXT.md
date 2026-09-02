---
id: seo.execution.architecture.local-architecture
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
# Local Site Architecture

## Purpose
Represent real locations, service areas, and market-specific offerings in a way that helps customers and organic discovery without producing thin doorway pages.

## Business Outcome
Create a local site structure that reflects where and how the business actually serves customers, making relevant local destinations easy to discover while preserving factual accuracy.

## Use When
Use when locations, service areas, franchises, or market-specific offerings need a clearer web architecture or when existing local pages are duplicative, thin, inconsistent, or poorly connected.

## Process
1. Establish the actual locations, service areas, franchises, services, and meaningful market-specific differences from reliable business evidence. Unknown coverage is not proof that the business does not serve an area.
2. Determine which location, service-area, or service/location combinations provide enough distinct customer value and business reality to deserve dedicated destinations. Do not generate permutations merely because they can target a query.
3. Design the location hierarchy, find-a-location or market-navigation paths, service-to-location relationships, breadcrumbs, and useful entity relationships around real customer behavior.
4. Define the factual content each local destination needs to be genuinely useful, such as verified address or service-area information, hours, available services, staff, directions, local policies, proof, or other real differentiators. Do not invent local uniqueness.
5. Keep public site facts, relevant local profiles, canonicals, internal links, and structured entity relationships consistent where they describe the same business reality.
6. If implementation is requested, make the smallest coherent architecture change the host can actually perform and verify representative local journeys afterward. Observe local discovery and conversion effects when they matter; the host owns any recurring monitoring schedule.

## Proportional Scope
Prioritize the markets, locations, and services that materially affect customers or business value. Broaden only when the architecture decision genuinely depends on wider market coverage.

## Verification
- Verify location eligibility and business facts before changing public location/profile information.
- Dedicated local pages have distinct customer value rather than only substituted place names.
- Claims about service areas, availability, proof, or performance remain supported by actual business evidence.
