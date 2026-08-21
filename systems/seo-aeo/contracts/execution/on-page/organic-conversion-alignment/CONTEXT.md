---
id: seo.execution.on-page.organic-conversion-alignment
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
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
  - cms.page.read
  optional:
  - search.serp.read
  - search.performance.read
  - cms.page.update
evidence_inputs:
- conversion CRM revenue best available proxy
---
# Conversion Alignment

## Purpose
Align organic intent and search promise with the landing experience; delegate general persuasion or journey mechanics when they are the true cause.

## Business Outcome
Improve valuable organic discovery through conversion alignment, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Conversion Alignment**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Define target conversion and prerequisite beliefs/actions for the page’s awareness stage.
2. [HYBRID] Inspect CTA relevance/visibility, proof, forms, friction, trust, pricing/contact expectations, and mobile usability.
3. [HYBRID] Match CTA to user readiness; avoid forcing bottom-funnel action on early informational intent.
4. [HYBRID] Add pathways to commercial/comparison/contact content when direct conversion is premature.
5. [HYBRID] Check offer-message consistency and post-click fulfillment.
6. [HYBRID] Verify conversion tracking before/after change and preserve search task satisfaction.


