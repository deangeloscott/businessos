---
id: seo.execution.local.local-eligibility-model
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
# Local Eligibility and Market Model

## Purpose
Determine whether local discovery applies to the business and represent locations, service areas, franchise relationships, and market boundaries accurately.

## Business Outcome
Give local work a truthful foundation so profiles, pages, services, and measurement reflect where and how customers can actually engage with the business.

## Use When
Use when local eligibility, physical presence, service areas, franchise relationships, delivery coverage, or market boundaries are unclear or materially affect local discovery work.

## Process
1. Establish the business's physical locations, staffed locations, service areas, delivery areas, franchises, virtual-only operations, and meaningful market boundaries from reliable organization evidence.
2. Verify what customers can actually do at or through each location and which addresses or service-area representations may legitimately be public. Unknown eligibility should remain unresolved rather than being inferred from convenience.
3. Map services/products and conversion actions by location or market, including real differences in hours, availability, licensing, pricing, language, or operational model when relevant.
4. Preserve canonical location/entity relationships to owned pages and local profiles when future work benefits from that durable truth. Do not create state merely to satisfy the Workflow.
5. Describe the practical local model—single-location, multi-location, service-area, franchise, hybrid, virtual/non-local, or another accurate form—only to the extent it helps downstream decisions.
6. When platform-specific representation rules or eligibility remain uncertain, gather current evidence before changing public profiles rather than inventing a generic approval gate.

## Proportional Scope
Model only the locations, markets, and relationships needed for the current business and foreseeable work. Do not create an elaborate location ontology for a simple operation.
