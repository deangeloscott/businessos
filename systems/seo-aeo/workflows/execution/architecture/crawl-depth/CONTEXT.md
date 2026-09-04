---
id: seo.execution.architecture.crawl-depth
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- crawl/index state HTTP behavior and URL relationships
---
# Crawl Depth Optimization

## Purpose
Make high-value assets meaningfully discoverable through the site's internal-link architecture without flattening useful hierarchy.

## Business Outcome
Reduce avoidable discovery friction for important pages while preserving an information architecture that still makes sense to users and the business.

## Use When
Use when important assets are unusually deep, orphaned, dependent on weak or conditional paths, or when architecture changes may alter their discoverability.

## Process
1. Measure or infer the shortest meaningful internal-link paths from discoverable entry points to the assets that matter to the current objective.
2. Interpret depth alongside business value, demand, traffic, index state, crawl observations, and the site's actual architecture. Depth alone is not a defect.
3. Identify high-value assets whose discoverability is weak relative to their importance, including pages reachable only through fragile pagination, filters, client rendering, or infrequently traversed paths.
4. Diagnose whether the real cause is hierarchy, orphaning, navigation, pagination, faceting, rendering, internal-link design, or intentional rarity before changing structure.
5. Improve the smallest useful set of navigation, hub, contextual-link, or architecture relationships. Do not indiscriminately flatten the entire site or add repetitive links solely to reduce a numeric depth score.
6. Verify the new paths in the actual rendered/link graph and observe crawl, index, experience, or business effects when those outcomes matter. AURA may preserve useful monitoring intent; the host owns any later schedule.

## Proportional Scope
Prioritize the highest-value templates and assets plus representative boundary cases. Expand when the problem appears systemic or additional coverage could materially change the architecture decision.
