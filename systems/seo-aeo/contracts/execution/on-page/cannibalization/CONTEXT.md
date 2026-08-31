---
id: seo.execution.on-page.cannibalization
type: playbook
version: 1.1.0
owner_system: seo-aeo
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
# Cannibalization

## Purpose
Resolve harmful overlap among owned pages without assuming every multi-URL ranking is a problem.

## Business Outcome
Improve valuable organic discovery through cannibalization, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Cannibalization**, or when an authorized incident response requires it.

## Process
1. [AI] Identify query/topic clusters with multiple owned URLs, swapping results, diluted CTR, or conflicting intent.
2. [HYBRID] Compare page intent, conversion role, backlinks, internal links, content overlap, canonical state, and historical performance.
3. [HYBRID] Decide whether URLs serve distinct useful intents.
4. [HYBRID] If harmful overlap exists, choose consolidate/redirect, differentiate/retarget, canonicalize, or change internal architecture.
5. [HYBRID] Preserve valuable backlinks/content/conversion paths during changes.
6. [HYBRID] Measure combined topic/cluster performance rather than one URL only.


