---
id: seo.execution.technical.faceted-navigation
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
# Faceted Navigation

## Purpose
Control combinatorial filter and sort URL spaces while preserving filtered experiences or landing pages that serve real customer demand.

## Business Outcome
Prevent low-value facet combinations from overwhelming crawl/index space without sacrificing useful navigation or valuable filtered discovery.

## Run When
Use when faceted filters, sorts, parameters, or generated combinations create materially different crawl/index states or a large URL space that needs intentional treatment.

## Process
1. Inventory the relevant facets, parameter patterns, generated combinations, crawl paths, and observable demand at enough depth to understand how the system behaves.
2. Classify combinations as valuable unique landing pages, useful customer states that do not need independent indexing, redundant variants, or low-value crawl/index waste.
3. Define the smallest coherent crawl/index/canonical/URL-generation rules that preserve useful navigation while preventing unnecessary combinatorial expansion. Use platform-appropriate mechanisms rather than assuming one universal implementation.
4. Create or preserve dedicated filtered landing pages only when the combination serves meaningful distinct demand and can provide a genuinely useful experience.
5. Keep internal links, navigation, sitemaps, canonicals, and generated URLs aligned so low-value combinations are not continually reintroduced as discovery targets.
6. Test representative valuable, boundary, and waste combinations after changes to verify both user navigation and crawler/index behavior.

## Proportionate Scope
Sample enough facet dimensions and combination depth to identify the generation pattern and important exceptions. Expand toward broader combinatorial testing when the interaction rules are complex or a small sample cannot establish safe boundaries.

## Verification
- Useful filtered customer experiences remain functional.
- Indexability is justified by distinct user/demand value, not merely by the existence of a URL.
- Controls do not create contradictory canonical, crawl, or internal-link behavior.
- Boundary testing covers the patterns most likely to create runaway combinations.
