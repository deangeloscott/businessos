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
---
# Internal Anchor Text

## Purpose
Use descriptive, natural internal anchor text that helps people understand the destination and reinforces the site's real information structure.

## Business Outcome
Improve navigation and internal discovery without forcing repetitive exact-match wording or treating anchor text as an isolated ranking lever.

## Use When
Use when internal anchors are empty, generic, misleading, inconsistent, over-optimized, or otherwise obscuring the destination's purpose.

## Process
1. Inspect the relevant source-target relationships and the anchor/context people actually encounter, including image links whose surrounding or alternative text carries the link meaning.
2. Identify anchors that are vague, misleading, inaccessible, excessively repetitive, stuffed, or inconsistent with the destination's real purpose.
3. Understand the target page's intent/entities and the source passage's local context before changing wording.
4. Write the shortest natural anchor that helps users predict the destination. Variation should emerge from context rather than from a quota for anchor diversity.
5. Change the link only where the surrounding copy naturally supports the destination; do not add awkward links solely to manufacture anchor text.
6. Verify the rendered link, destination, accessibility, and surrounding meaning after implementation when the host can make the change.

## Proportional Scope
Prioritize important destinations and recurring anchor patterns. Expand when template-level or site-wide wording problems materially affect navigation or discovery.
