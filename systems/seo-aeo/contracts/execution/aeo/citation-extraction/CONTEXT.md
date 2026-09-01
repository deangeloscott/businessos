---
id: seo.execution.aeo.citation-extraction
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
  - ai_answer.observe
  optional:
  - research.web.read
  - cms.page.read
  - cms.page.update
  - analytics.read
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- backlink/referring-domain/mention evidence and prospect records
---
# AI Citation and Link Extraction

## Purpose
Determine which sources and owned assets are cited/linked in answers and for which question contexts.

## Business Outcome
Improve valuable organic discovery through ai citation and link extraction, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **AI Citation and Link Extraction**, or when an authorized incident response requires it.

## Process
1. [DETERMINISTIC] Parse each Answer Observation for explicit links/citations/source cards and normalize destination URL/domain.
2. [AI] Resolve redirects/canonicals and classify owned, competitor, neutral authority, community, marketplace, or unknown source.
3. [AI] Map citation to the claim/answer section it appears to support when observable.
4. [HYBRID] Aggregate citation frequency/coverage by prompt cluster, surface, topic, asset, competitor, and time period.
5. [AI] Distinguish citation presence from recommendation/mention; do not assume a citation means endorsement or traffic.
6. [HYBRID] Create source/citation gap Opportunities where business relevance and a plausible information improvement exist.


