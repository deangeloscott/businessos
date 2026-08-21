---
id: seo.execution.on-page.entities-evidence
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - cms.page.read
  optional:
  - search.serp.read
  - search.performance.read
  - cms.page.update
---
# Entities Evidence

## Purpose
Clarify important entities, relationships, facts, and proof.

## Business Outcome
Improve valuable organic discovery through entities evidence, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Entities Evidence**, or when an authorized incident response requires it.

## Process
1. [AI] Identify people, products, organizations, places, concepts, specifications, claims, and comparisons important to the page.
2. [HYBRID] Check ambiguity and inconsistent naming across site/structured data/profiles.
3. [HYBRID] Add clear definitions/relationships where users need them.
4. [HYBRID] Attach evidence, citations, author/expert context, original data, methodology, case examples, or proof to material claims.
5. [HYBRID] Ensure visible content, structured data, and persistent brand facts do not contradict each other.
6. [HYBRID] Escalate regulated or high-impact claims to fact/compliance review.


