---
id: seo.execution.internal-linking.contextual-linking
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
# Contextual Linking

## Purpose
Add internal links where another owned asset naturally answers the next question, deepens understanding, or advances a useful journey.

## Business Outcome
Improve user navigation and organic discovery by connecting genuinely related assets without adding filler links or forcing ambiguous intent ownership.

## Use When
Use when a target page would benefit from relevant internal discovery paths or when source content naturally creates a useful next-step relationship.

## Process
1. Find plausible source pages through semantic relevance, shared entities, journey adjacency, audience overlap, and the actual role of the target page.
2. Inspect the specific passages where a link could appear and keep only placements that improve the local context for the reader.
3. If multiple targets appear to serve the same intent, resolve or diagnose that ownership question before distributing links mechanically. Continue into the Cannibalization Workflow when the overlap itself is the real problem; an Opportunity object is not required.
4. Add or edit only the amount of surrounding copy needed to make the relationship clear, useful, and natural.
5. Preserve source-target relationship metadata only when it materially helps future architecture, diagnosis, or maintenance; do not log every link merely because a schema can represent it.
6. If implementation is requested and the host can perform it, verify the rendered link, destination, context, and important user/discovery behavior afterward.

## Proportional Scope
Start with the most valuable target pages and strongest source relationships. Expand when the site's architecture or content network indicates a wider linking gap.
