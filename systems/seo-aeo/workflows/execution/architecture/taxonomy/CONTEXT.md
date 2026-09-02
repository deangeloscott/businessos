---
id: seo.execution.architecture.taxonomy
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
---
# Taxonomy Design

## Purpose
Design durable content/product/service classifications that reflect user tasks, business offerings, and discovery demand.

## Business Outcome
Improve valuable organic discovery through taxonomy design, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Taxonomy Design**, or when an authorized incident response requires it.

## Process
1. [AI] Inventory current content and business entities; identify overlapping, missing, and purely internal labels.
2. [AI] Map audience tasks, offers, topic clusters, product/service families, and market/location dimensions.
3. [HYBRID] Propose a taxonomy with mutually understandable parent/child relationships; separate navigation labels from internal metadata where useful.
4. [AI] Test whether important demand can map to one primary canonical destination without forcing unrelated intents together.
5. [AI] Identify migration implications for existing URLs, breadcrumbs, internal links, faceted paths, and structured data.
6. [HYBRID] Document naming rules, ownership, allowed values, and future extension rules; route URL-changing work through change-control.


