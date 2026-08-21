---
id: seo.execution.architecture.navigation
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
  - cms.page.read
  - cms.page.update
---
# Navigation Architecture

## Purpose
Make important user and crawler pathways discoverable without bloating global navigation or flattening meaningful hierarchy.

## Business Outcome
Improve valuable organic discovery through navigation architecture, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Navigation Architecture**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Inventory global, utility, contextual, footer, faceted, and local navigation elements.
2. [AI] Map priority audiences/tasks and high-value asset families to expected navigation paths.
3. [INTEGRATION] Measure orphaning, click/crawl depth, repetitive links, inaccessible JS-only paths, and misleading labels.
4. [HYBRID] Design candidate navigation changes that improve discovery while preserving user comprehension and conversion flow.
5. [AI] Model affected internal-link relationships and identify pages that would gain/lose prominence.
6. [AI] Stage and test the navigation; verify rendering, accessibility, crawlability, analytics, and downstream page behavior.


