---
id: seo.execution.local.categories-services
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
# Local Categories and Services

## Purpose
Represent each location with accurate categories, services, and product descriptors that match what customers can actually obtain there.

## Business Outcome
Improve relevant local discovery and conversion without category stuffing, unsupported services, or copying competitor representations that do not fit the business.

## Use When
Use when local categories, attributes, services, or product representations are missing, stale, inaccurate, or plausibly limiting discovery for legitimate offerings.

## Process
1. Establish the real offerings and availability for each relevant location or service area from current business truth.
2. Observe how customers describe those needs and how relevant local surfaces represent comparable businesses, treating competitor choices as evidence rather than truth for the organization.
3. Choose the most specific truthful primary and supporting categories available on the relevant surface; platform availability does not make a category accurate.
4. Map supported services/products to canonical offerings and actual location availability, preserving market-specific differences where real.
5. Reject keyword stuffing, duplicate category inflation, or any representation the organization cannot substantiate.
6. If significant changes are implemented, verify the published fields and observe relevant visibility and conversion evidence over an appropriate period. AURA may remember the material change and measurement intent; the host owns any recurring recheck.

## Proportional Scope
Prioritize categories and services tied to meaningful customer demand and business value. Do not optimize every optional field merely because a platform exposes it.
