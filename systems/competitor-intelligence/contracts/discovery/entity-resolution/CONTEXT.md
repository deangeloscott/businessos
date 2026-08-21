---
id: competitor.discovery.entity-resolution
type: playbook
version: 1.7.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 3
reads:
- Competitor
- SourceRecord
- Observation
writes:
- Competitor
- Observation
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.fetch
  - social.observe
  - review.read
  - advertising.observe
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Entity Resolution

## Purpose
Resolve domains, aliases, social/review/advertising profiles, and other public identities to the correct canonical competitor before evidence is merged.

## Business Outcome
Prevent competitive intelligence from mixing similarly named businesses, brands, subsidiaries, resellers, or unrelated public profiles.

## Run When
Run when creating a competitor, onboarding new evidence surfaces, or when a source/profile identity is ambiguous or changed.

## Process
1. [AI] Start from the candidate competitor, market/audience context, known domain/name/aliases, and the evidence surface that needs resolution.
2. [INTEGRATION] Gather identity candidates from first-party links, returned links to the official domain, public profile metadata, advertiser/payer identity, location, legal/product identity, known handles, marketplace/app records, and other relevant corroboration.
3. [HYBRID] Treat similar names, logos, keywords, or handles as candidates only. Prefer bidirectional or multi-signal corroboration such as official site → profile plus profile → official domain.
4. [AI] Distinguish parent/subsidiary, regional entity, reseller/partner, former identity, and unrelated namesakes when material to the research question.
5. [HYBRID] Assign each profile/identity a status of verified, probable, ambiguous, or rejected with confidence and evidence references. Do not merge ambiguous evidence into canonical competitor state.
6. [DETERMINISTIC] Update the Competitor identity block with deduplicated official domains, aliases, and resolved profiles; preserve rejected/ambiguous candidates in evidence rather than silently discarding why they were excluded.
7. [AI] Route unresolved identity questions for confirmation only when they materially affect downstream research; otherwise continue with verified surfaces and mark coverage partial.

## Verification
Downstream competitor evidence can be traced to an identity surface whose relationship to the canonical Competitor is explicit and confidence-scored.
