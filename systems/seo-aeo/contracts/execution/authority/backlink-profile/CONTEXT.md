---
id: seo.execution.authority.backlink-profile
type: playbook
version: 1.1.0
owner_system: seo-aeo
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
  - backlink.read
  optional:
  - research.web.read
  - crm.contact.read
  - email.send
evidence_inputs:
- location/profile data, local-result observations, and local competitors
- backlink/referring-domain/mention evidence and prospect records
---
# Backlink Profile Analysis

## Purpose
Build an evidence-based view of external links, referring domains, anchors, destinations, quality, risk, and business relevance.

## Business Outcome
Improve valuable organic discovery through backlink profile analysis, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Backlink Profile Analysis**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Ingest all available backlink/referring-domain observations with source and timestamp.
2. [DETERMINISTIC] Normalize domains/URLs, deduplicate links, identify redirects/canonicals, and preserve first/last seen.
3. [HYBRID] Enrich each relationship with topical relevance, traffic/visibility proxies, editorial context, placement, destination, anchor, followability, and known risk signals.
4. [HYBRID] Separate earned/editorial value from self-created, low-value, spammy, or unknown links; do not treat raw link count as authority.
5. [AI] Map links to assets/topics/business priorities and identify concentrated dependency or lost-link patterns.
6. [HYBRID] Write a baseline and create opportunities only where an actionable gap or risk exists.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


