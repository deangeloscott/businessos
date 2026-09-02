---
id: seo.execution.local.profile-completeness
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
# Local Profile Completeness

## Purpose
Ensure each legitimate local profile accurately represents the business with the fields that materially help customers and discovery.

## Business Outcome
Make local profiles useful, current, and trustworthy without keyword stuffing, invented offerings, or filling every optional field merely to achieve a completeness score.

## Use When
Use when an important local profile is missing material information, contains stale or conflicting facts, or no longer reflects the way customers can engage with the business.

## Process
1. Retrieve or inspect the current profile and compare its material fields with canonical location/business truth.
2. Verify the fields that matter on that surface, such as business identity, address/service area, phone, website, hours/special hours, categories, attributes, services/products, descriptions, appointment/order links, and media where supported.
3. Identify missing, stale, conflicting, duplicated, unsupported, or unverifiable fields. Distinguish a real gap from an optional field that adds no customer value.
4. Prepare only changes supported by established business facts. Do not add keywords, locations, categories, services, amenities, credentials, or other claims that are not legitimately true.
5. If the user requested execution and the host has the necessary profile access, make the changes through the real platform and preserve before/after context only when useful later. Otherwise provide the exact corrections without claiming publication.
6. Verify the published state. If platform edits, suspensions, duplicates, or drift materially matter, preserve monitoring intent; the host/runtime owns actual recurrence and notifications.

## Proportional Scope
Prioritize fields that affect customer decisions, eligibility, relevance, conversion, or factual trust. Do not optimize for a generic profile-completion percentage.
