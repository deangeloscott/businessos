---
id: seo.execution.local.local-citations-links
type: playbook
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
  - local_profile.read
  optional:
  - local_profile.update
  - review.read
  - research.web.read
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- location/profile data, local-result observations, and local competitors
- backlink/referring-domain/mention evidence and prospect records
---
# Local Citations and Links

## Purpose
Earn/correct locally meaningful references that reinforce discoverability and trust.

## Business Outcome
Improve valuable organic discovery through local citations and links, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Local Citations and Links**, or when an authorized incident response requires it.

## Process
1. [AI] Identify local chambers, associations, government/community resources, suppliers, partners, sponsorships, news outlets, directories, and neighborhood resources relevant to the business.
2. [HYBRID] Qualify each source for legitimacy, audience usefulness, geographic relevance, and actual relationship/opportunity.
3. [AI] Determine whether the needed action is data correction, listing, partnership, contribution, event/resource, or earned editorial coverage.
4. [HYBRID] Route outreach/claiming through the appropriate authority playbook.
5. [HYBRID] Verify canonical identity and destination URL on publication.
6. [HYBRID] Track local referral, lead, visibility, and authority effects rather than counting citations alone.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


