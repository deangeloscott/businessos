---
id: seo.execution.authority.unlinked-mentions
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Unlinked Brand Mention Recovery

## Purpose
Turn legitimate existing brand references into accurate links where a link would improve the source for its audience.

## Business Outcome
Improve valuable organic discovery through unlinked brand mention recovery, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Unlinked Brand Mention Recovery**, or when an authorized incident response requires it.

## Process
1. [DETERMINISTIC] Discover brand/product/person/entity mentions across accessible sources and deduplicate.
2. [HYBRID] Confirm the mention refers to the owned entity and whether a correct owned destination would add reader value.
3. [HYBRID] Exclude negative/sensitive contexts where outreach could worsen the situation; route reputation issues separately.
4. [DETERMINISTIC] Find an appropriate contact channel and record provenance/confidence.
5. [HYBRID] Prepare a concise correction/value request referencing the exact page and suggested destination without entitlement or manipulation.
6. [INTEGRATION] Track response, resulting link/mention correction, and performance; do not repeatedly pressure nonresponsive publishers.


