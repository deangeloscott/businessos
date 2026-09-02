---
id: seo.execution.architecture.hub-spoke
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
# Hub-and-Spoke Architecture

## Purpose
Create coherent topic, service, or solution clusters that help people navigate related needs and make relationships between useful assets clear.

## Business Outcome
Strengthen discovery and user journeys around important subjects without manufacturing thin hubs, duplicate-intent pages, or artificial content clusters.

## Use When
Use when several genuinely distinct assets serve related parts of the same customer problem, topic, service, or decision and a clearer shared structure could improve discovery or navigation.

## Process
1. Identify a cluster with a real shared subject or customer journey and multiple distinct intents or supporting assets. Do not force unrelated pages into a cluster because their keywords overlap.
2. Select or define the hub only when it can provide standalone value. Give each spoke a distinct purpose and avoid creating multiple pages for the same underlying intent.
3. Map useful hub-to-spoke, spoke-to-hub, and contextual spoke-to-spoke relationships based on what helps the user continue, not on a requirement to create a fully connected graph.
4. Identify genuine coverage or journey gaps. Create or recommend a new asset only when the missing destination would materially help users or the business; an AURA Opportunity is optional durable coordination, not a required output.
5. Add breadcrumbs, navigation, entity/structured-data relationships, or other architecture signals when they accurately represent the structure and improve usability or interpretation.
6. Verify that the hub and spokes remain independently useful, discoverable, and non-duplicative and that the architecture has not created a thin doorway layer.

## Proportional Scope
Use the smallest coherent cluster that serves the business problem. Broaden when additional related assets materially improve the journey or reveal a larger architecture problem.
