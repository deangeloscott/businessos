---
id: seo.execution.authority.resource-page-acquisition
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 2
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - backlink.read
  optional:
  - research.web.read
  - crm.contact.read
  - email.send
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Resource Page Acquisition

## Purpose
Earn inclusion on curated resources/directories when the owned resource genuinely belongs.

## Business Outcome
Improve valuable organic discovery through resource page acquisition, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Resource Page Acquisition**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Find curated pages/directories serving the target audience/topic/market.
2. [HYBRID] Inspect inclusion criteria, existing resources, maintenance recency, and editorial legitimacy.
3. [HYBRID] Match a specific owned resource/business/location to the page's purpose.
4. [HYBRID] Prepare the exact facts, descriptions, evidence, and destination needed for inclusion.
5. [INTEGRATION] Submit or outreach through the preferred channel and comply with editorial rules.
6. [HYBRID] Verify listing accuracy/link destination and define SEO monitoring for continued presence/value.


