---
id: seo.execution.authority.directories-citations
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
- prompt/question observations, answer text, citations, mentions, and competing sources
- backlink/referring-domain/mention evidence and prospect records
---
# Directories and Citations

## Purpose
Create or correct authoritative business listings where presence helps users, local verification, or industry discovery.

## Business Outcome
Improve valuable organic discovery through directories and citations, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Directories and Citations**, or when an authorized incident response requires it.

## Process
1. [AI] Identify general/local/industry directories and citation sources relevant to business type/location.
2. [HYBRID] Prioritize sources by legitimacy, audience utility, data ecosystem importance, and business relevance—not raw domain metrics.
3. [DETERMINISTIC] Normalize canonical business identity fields and resolve conflicting NAP/entity data.
4. [INTEGRATION] Claim/submit/update profiles through authorized channels, including required categories/services/URLs.
5. [DETERMINISTIC] Verify publication and consistency; record login/ownership metadata securely outside the public workspace.
6. [HYBRID] Monitor for drift, duplicates, closures, relocations, and inaccurate third-party changes.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


