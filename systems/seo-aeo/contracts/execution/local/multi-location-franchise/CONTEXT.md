---
id: seo.execution.local.multi-location-franchise
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
# Multi-Location and Franchise Governance

## Purpose
Scale local optimization while preserving per-location truth, ownership, quality, and exception handling.

## Business Outcome
Improve valuable organic discovery through multi-location and franchise governance, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Multi-Location and Franchise Governance**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Create a location registry with IDs, ownership/franchise relationships, canonical facts, services, permissions, and lifecycle status.
2. [HYBRID] Define which fields are centrally governed versus locally editable and establish conflict-resolution rules.
3. [HYBRID] Template repeatable data structures and QA, not duplicated customer-facing copy.
4. [HYBRID] Detect location-specific anomalies: closures, moves, duplicates, hours changes, review spikes, profile suspensions, and inconsistent pages.
5. [HYBRID] Route local changes through per-location autonomy/approval when ownership or legal responsibility differs.
6. [HYBRID] Roll up metrics at location, region, franchisee, and brand levels without hiding poor individual-location performance.


