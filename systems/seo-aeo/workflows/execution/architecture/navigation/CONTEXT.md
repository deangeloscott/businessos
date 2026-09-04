---
id: seo.execution.architecture.navigation
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
# Navigation Architecture

## Purpose
Make important user and crawler pathways discoverable without bloating navigation or flattening meaningful hierarchy.

## Business Outcome
Help people reach high-value destinations naturally while giving important assets reliable internal discovery paths and preserving a comprehensible site structure.

## Use When
Use when navigation is obscuring important destinations, creating orphaned or excessively deep paths, overexposing low-value pages, or changing in a way that could affect discovery or conversion.

## Process
1. Inventory the navigation surfaces that materially shape discovery: global, utility, contextual, footer, faceted, local, and other recurring pathways.
2. Map priority audiences, tasks, and high-value asset families to the routes people reasonably expect to use. Navigation should reflect real information needs rather than only SEO prominence.
3. Inspect orphaning, click/crawl depth, repetitive or low-value global links, misleading labels, inaccessible client-only paths, and other patterns that distort discovery or comprehension.
4. Design the smallest navigation changes that materially improve wayfinding and discovery while preserving meaningful hierarchy, accessibility, and conversion flow.
5. Reason about which pages gain or lose prominence and whether those shifts match business value, customer needs, and the intended information architecture.
6. If implementation is requested, use the site's real navigation mechanisms and verify rendering, accessibility, crawlability, analytics, and important downstream journeys after the change.

## Proportional Scope
Start with the navigation surfaces and asset families most relevant to the current business problem. Expand when shared templates or site-wide patterns make broader analysis necessary.
