---
id: seo.execution.local.multi-location-franchise
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
# Multi-Location and Franchise Governance

## Purpose
Scale local operations while preserving per-location truth, ownership, quality, and meaningful exceptions.

## Business Outcome
Keep multi-location or franchise discovery coherent at brand scale without overwriting real local differences or turning governance into an internal approval bureaucracy.

## Use When
Use when many locations, franchisees, regions, or local operators share brand systems but differ in facts, ownership, offerings, permissions, or performance.

## Process
1. Maintain the minimum useful location registry: stable identity, ownership/franchise relationships, canonical facts, services, important permissions/constraints, and lifecycle state where those meanings matter later.
2. Distinguish facts and fields that are genuinely brand-wide from those that are location-specific or locally controlled. Resolve conflicts from real ownership, legal, platform, or organizational authority rather than an AURA autonomy tier.
3. Standardize repeatable data structures, quality checks, and reusable components where useful, but do not template duplicate customer-facing copy as a substitute for local relevance.
4. Detect material location-specific exceptions such as closures, moves, duplicates, hours changes, suspensions, inconsistent pages/profiles, review anomalies, or offering changes.
5. Apply changes through the person/system that actually owns the relevant external surface when the user's request and real permissions allow it. Preserve durable handoff state only when another actor genuinely must continue the work later.
6. Compare performance at the location, region, franchisee, and brand level when those rollups help decisions, while keeping poor individual-location outcomes visible rather than hiding them in averages.

## Proportional Scope
Use governance only to the degree scale and ownership complexity require. A handful of locations should not inherit enterprise bureaucracy merely because the same Workflow can describe it.
