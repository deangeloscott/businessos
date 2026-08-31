---
id: seo.execution.on-page.intent-alignment
type: playbook
version: 1.1.0
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
# Intent Alignment

## Purpose
Align an existing page with the actual high-value user intent it should satisfy.

## Business Outcome
Improve valuable organic discovery through intent alignment, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Intent Alignment**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Define target audience, awareness/buyer stage, demand cluster, and conversion objective.
2. [AI] Inspect current SERP/answer composition and winning assets to infer the user task and expected asset type.
3. [HYBRID] Compare page purpose, information, proof, and CTA with observed intent.
4. [AI] Identify mismatches: wrong page type, missing decision information, over-broad focus, irrelevant sections, or audience mismatch.
5. [HYBRID] Decide whether to rewrite, split, consolidate, retarget, or leave unchanged.
6. [HYBRID] Implement while preserving valuable existing coverage, links, and brand differentiation.
7. [AI] Re-evaluate the revised page against representative user tasks before publication.


