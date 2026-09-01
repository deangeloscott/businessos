---
id: seo.execution.on-page.topical-coverage
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- OrganicDemandUnit
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
evidence_inputs:
- records topic intent evidence
---
# Topical Coverage

## Purpose
Close meaningful content gaps without padding or duplicating other pages.

## Business Outcome
Improve valuable organic discovery through topical coverage, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Topical Coverage**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Define the page’s primary intent boundary.
2. [HYBRID] Compare demand questions, owned expertise, competitor coverage, sales/support questions, entities, and current page.
3. [AI] Classify missing subtopics as required, helpful, irrelevant, or better served on another asset.
4. [HYBRID] Gather evidence/original inputs for required additions.
5. [HYBRID] Add sections that improve task completion, trust, differentiation, or conversion.
6. [HYBRID] Link to deeper dedicated assets rather than bloating the page when appropriate.
7. [INTEGRATION] Check cannibalization/duplication before publishing.


