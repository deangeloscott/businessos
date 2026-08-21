---
id: seo.execution.local.profile-completeness
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
# Local Profile Completeness

## Purpose
Ensure each authorized local profile accurately and comprehensively represents the business.

## Business Outcome
Improve valuable organic discovery through local profile completeness, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Local Profile Completeness**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] Retrieve current profile fields and compare with canonical brand/location state.
2. [DETERMINISTIC] Validate business name, address/service area, phone, website, hours, special hours, descriptions, categories, attributes, services/products, appointment/order links, and media where supported.
3. [AI] Identify missing, stale, conflicting, duplicated, or unverifiable fields.
4. [HUMAN] Prepare changes from approved canonical facts; do not add keywords or locations that are not legitimate business identity.
5. [HYBRID] Execute or route changes according to permissions and preserve before/after state.
6. [INTEGRATION] Verify published state and monitor for platform edits, suspensions, duplicates, or drift.


