---
id: seo.execution.authority.guest-expert-contribution
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
# Guest / Expert Contribution

## Purpose
Contribute genuine expertise to third-party audiences when the contribution itself has business/editorial value.

## Business Outcome
Improve valuable organic discovery through guest / expert contribution, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Guest / Expert Contribution**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Find publications, communities, podcasts, events, or resources with relevant audiences and legitimate contribution models.
2. [HYBRID] Review editorial standards, topical gaps, author requirements, disclosure, and link policies.
3. [HYBRID] Select a contribution angle based on demonstrable expertise or original evidence.
4. [HYBRID] Prepare a pitch and, if accepted, produce original useful content rather than recycled SEO filler.
5. [HYBRID] Ensure bios/links/claims are accurate and proportionate to editorial norms.
6. [HYBRID] Track publication, referral/business impact, mentions, and relationship value.


