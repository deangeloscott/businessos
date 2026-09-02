---
id: seo.execution.internal-linking.anchor-text
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
- backlink/referring-domain/mention evidence and prospect records
---
# Internal Anchor Text

## Purpose
Use descriptive, varied, context-appropriate internal anchor text that clarifies destination purpose.

## Business Outcome
Improve valuable organic discovery through internal anchor text, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Internal Anchor Text**, or when an authorized incident response requires it.

## Process
1. [HYBRID] Extract internal anchors by source-target pair and target page.
2. [AI] Identify empty/generic/misleading/over-optimized anchors, image links without useful alt context, and inconsistent naming.
3. [AI] Map target intent/entities and source sentence context.
4. [AI] Draft concise descriptive anchors that help users predict the destination; avoid forced exact-match repetition.
5. [HYBRID] Apply only where the surrounding copy naturally supports the link.
6. [INTEGRATION] Re-crawl and verify link destination, accessibility, and anchor distribution.


