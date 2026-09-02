---
id: seo.execution.architecture.ecommerce-architecture
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
# Ecommerce Architecture

## Purpose
Organize categories, collections, products, variants, filters, and merchandising paths around real shopping behavior and durable organic discovery.

## Business Outcome
Help customers and discovery systems reach the right commercial destinations without creating crawl traps, duplicate inventory surfaces, or confusing category overlap.

## Use When
Use when an ecommerce site's category tree, product relationships, variants, filters, discontinued inventory, or merchandising structure is limiting discovery, shopping usability, or maintainability.

## Process
1. Inventory the current category/collection tree, product relationships, variants, facets, internal search behavior, inventory states, and important merchandising paths.
2. Map meaningful customer shopping tasks and commercial demand to destinations that deserve to exist. Distinguish navigational convenience from a reason to create another indexable landing page.
3. Separate useful category or filtered landing experiences from crawl traps, near-duplicate combinations, thin inventory states, and parameter patterns that add no distinct value.
4. Define coherent behavior for canonicals, internal links, navigation, sitemaps, variants, out-of-stock products, discontinued items, pagination, and filtered states. Use the specialist Workflow when one of those becomes the real problem.
5. Identify missing commercial destinations and category/product intent collisions. Do not create a new category merely because a keyword can be found; it should serve a real shopping or business need.
6. For material architecture changes, map affected URLs and relationships, protect revenue and measurement continuity, and verify representative high-value paths before and after implementation.

## Proportional Scope
Start with the categories, product families, and parameter patterns that carry the most business value or risk. Expand when evidence indicates the architecture problem is systemic or broader analysis could materially alter the design.
