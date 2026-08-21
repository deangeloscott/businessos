---
id: seo.execution.local.nap-consistency
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
# Business Identity / NAP Consistency

## Purpose
Maintain a canonical business identity across owned and important third-party sources.

## Business Outcome
Improve valuable organic discovery through business identity / nap consistency, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Business Identity / NAP Consistency**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Define canonical legal/public business name, address or service-area representation, phone(s), URLs, hours, and identifiers per location.
2. [DETERMINISTIC] Discover important listings/citations and normalize variations.
3. [AI] Classify differences as acceptable formatting, outdated data, duplicate entity, wrong entity, or material inconsistency.
4. [HYBRID] Prioritize corrections on high-impact data sources and user-facing profiles.
5. [INTEGRATION] Submit/claim/correct through authorized channels and record verification.
6. [HYBRID] Continuously recheck material sources after moves, rebrands, phone/URL changes, mergers, or closures.


