---
id: seo.execution.authority.broken-link-acquisition
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
# Broken Link Acquisition

## Purpose
Find dead external resources where the brand has a genuinely relevant replacement or can create one.

## Business Outcome
Improve valuable organic discovery through broken link acquisition, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Broken Link Acquisition**, or when an authorized incident response requires it.

## Process
1. [AI] Identify relevant pages with broken outbound references or competitors' lost/dead linked assets.
2. [HYBRID] Recover the original referenced purpose/content using available evidence.
3. [HYBRID] Confirm an owned asset is a materially suitable replacement; if not, create a content/linkable-asset opportunity rather than forcing a fit.
4. [HYBRID] Qualify the source and contact path.
5. [AI] Outreach by explaining the broken reference and offering the replacement as one useful option.
6. [HYBRID] Track outcomes and update opportunity status; avoid scaled low-context outreach.


