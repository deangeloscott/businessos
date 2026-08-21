---
id: seo.execution.technical.duplicate-content
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: medium
autonomy_ceiling: 3
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
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
evidence_inputs:
- records topic intent evidence
---
# Duplicate Content

## Purpose
Reduce waste/confusion from duplicate and near-duplicate assets while preserving useful variants.

## Business Outcome
Improve valuable organic discovery through duplicate content, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Duplicate Content**, or when an authorized incident response requires it.

## Process
1. [AI] Generate duplicate clusters from URL patterns, hashes/similarity, titles, canonicals, and parameters.
2. [AI] Classify legitimate variants versus accidental duplicates.
3. [HYBRID] Measure traffic, links, conversions, market/language, and intent uniqueness of cluster members.
4. [HYBRID] Choose improve/differentiate, consolidate/redirect, canonicalize, noindex, parameter control, or leave unchanged.
5. [HYBRID] Align internal links/sitemaps and ensure valuable intent is not lost.
6. [HYBRID] Define SEO monitoring for selected canonical and combined performance after consolidation.


