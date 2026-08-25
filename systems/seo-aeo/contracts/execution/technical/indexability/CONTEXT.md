---
id: seo.execution.technical.indexability
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
  - crawler.run
  optional:
  - webpage.fetch
  - cms.page.read
  - cms.page.update
  - search.index.inspect
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Indexability

## Purpose
Diagnose whether valuable pages are eligible for indexing and why eligible pages may still be absent.

## Business Outcome
Improve valuable organic discovery through indexability, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Indexability**, or when an authorized incident response requires it.

## Process
1. [INTEGRATION] For target URLs capture status, crawl access, meta/X-Robots directives, canonical, rendered main content, sitemap presence, internal links, and observed index state.
2. [HYBRID] Separate “not eligible” from “eligible but not selected/indexed.”
3. [HYBRID] Check duplicate/near-duplicate clusters, soft-error signals, thin/non-unique utility, canonical conflicts, and content accessibility.
4. [HYBRID] Confirm the page actually serves independent user/search demand and should be indexed.
5. [HYBRID] Fix blocking directives/technical defects only where indexing is desired.
6. [INTEGRATION] If eligible but unindexed, improve discovery, distinct value, internal references, or canonical consistency as diagnosis warrants rather than repeatedly resubmitting.
7. [HYBRID] Verify eligibility and schedule index-state recheck.



## Customer-Facing Mutation Guardrail
If an indexability fix changes visible/customer-facing text (including broken-link remediation, CTA text, navigation, headings, or page creation), follow `core/policies/customer-facing-mutations.md`. Prefer removal/narrowing when a broken target refers to a service/capability not established in canonical business truth.
