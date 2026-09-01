---
id: seo.execution.architecture.hub-spoke
type: playbook
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
---
# Hub-and-Spoke Architecture

## Purpose
Create coherent topic/service hubs that help users traverse a subject and concentrate internal discovery signals.

## Business Outcome
Improve valuable organic discovery through hub-and-spoke architecture, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Hub-and-Spoke Architecture**, or when an authorized incident response requires it.

## Process
1. [AI] Identify a topic/service cluster with multiple distinct intents or supporting assets.
2. [HYBRID] Select or define the hub asset and each spoke's unique purpose; prevent duplicate-intent pages.
3. [AI] Map required hub-to-spoke, spoke-to-hub, and contextually useful spoke-to-spoke links.
4. [AI] Identify missing assets needed to complete the journey or topic coverage and create Opportunities for them.
5. [HYBRID] Define breadcrumbs/navigation/schema relationships where relevant.
6. [HYBRID] Verify that each linked asset remains useful independently and that the hub is not a thin doorway page.


