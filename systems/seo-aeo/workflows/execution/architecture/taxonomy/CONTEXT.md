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
Design durable classifications for content, products, services, and other business entities around how people understand and navigate them.

## Business Outcome
Create a taxonomy that improves organization, discovery, and maintainability without forcing unrelated intents together or exposing internal labels as user-facing structure when they do not belong there.

## Use When
Use when categories, tags, product/service families, topic structures, or other classifications are missing, overlapping, confusing, or creating discovery and maintenance problems.

## Process
1. Inventory the relevant content and business entities and distinguish user-facing concepts from purely internal labels or metadata.
2. Map audience tasks, offers, topic or product/service families, market/location dimensions, and meaningful discovery demand to the classifications that could help organize them.
3. Define understandable parent/child or peer relationships where hierarchy is useful. Keep navigation labels, URLs, and internal metadata separate when they serve different purposes.
4. Test whether important intents can map to clear primary destinations without forcing unrelated needs together or multiplying near-duplicate categories.
5. Identify consequences for URLs, breadcrumbs, internal links, facets, structured data, filters, and existing destination ownership before changing a live taxonomy.
6. Define naming and extension principles only where they help the taxonomy remain coherent over time. If implementation changes URLs or other consequential site state, handle those real migration effects directly rather than routing through an AURA change-control lifecycle.

## Proportional Scope
Design to the complexity the business actually has. Avoid elaborate classification systems for small inventories, but broaden when scale, multiple dimensions, or future extension materially affect the architecture decision.
