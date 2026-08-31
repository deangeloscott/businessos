---
id: seo.execution.internal-linking.authority-routing
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
  - crawler.run
  optional:
  - cms.page.read
  - cms.page.update
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Internal Authority Routing

## Purpose
Route internal prominence toward strategically important pages without harming navigation or creating manipulative link patterns.

## Business Outcome
Improve valuable organic discovery through internal authority routing, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Internal Authority Routing**, or when an authorized incident response requires it.

## Process
1. [AI] Identify high-value target pages and internal source pages with relevant contextual/topical relationships and strong existing visibility/links.
2. [AI] Map current inlinks, source importance, anchors, click context, depth, and competing target pages.
3. [HYBRID] Prioritize links that improve user next-step usefulness as well as discovery; reject irrelevant authority-only placements.
4. [HYBRID] Select source, target, anchor/context, and placement; preserve natural language and accessibility.
5. [DETERMINISTIC] Execute in controlled batches where impact is uncertain and record Change Events.
6. [HYBRID] Define SEO measurement / Core OutcomeEvaluation for target/source ranking, traffic, click, crawl, and conversion effects and recalibrate rules.


