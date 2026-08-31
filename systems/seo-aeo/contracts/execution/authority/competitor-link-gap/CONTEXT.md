---
id: seo.execution.authority.competitor-link-gap
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
- OrganicCompetitorState
- Competitor
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
# Competitor Link Gap

## Purpose
Find external sources that credibly reference competitors or the topic but not the owned brand.

## Business Outcome
Improve valuable organic discovery through competitor link gap, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Competitor Link Gap**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Select true search/business/answer competitors relevant to the opportunity.
2. [DETERMINISTIC] Collect linking/mentioning domains and pages for competitor assets and normalize them.
3. [DETERMINISTIC] Filter sources by topical/business relevance, editorial legitimacy, audience fit, accessibility, and whether the brand could plausibly add value.
4. [AI] Identify the reason each competitor earned the reference: data, tool, quote, product, relationship, directory, newsworthiness, etc.
5. [AI] Classify the appropriate acquisition strategy rather than sending one generic pitch.
6. [HYBRID] Create qualified Authority Opportunities with evidence, target source, required asset/value proposition, and expected business pathway.


