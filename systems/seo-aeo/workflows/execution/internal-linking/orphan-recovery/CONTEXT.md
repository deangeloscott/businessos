---
id: seo.execution.internal-linking.orphan-recovery
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
# Orphan Page Recovery

## Purpose
Find valuable assets with no meaningful internal discovery path and decide whether to reconnect, consolidate, redirect, retire, or leave them intentionally isolated.

## Business Outcome
Restore useful internal discovery for assets that deserve it while avoiding filler links to pages whose value or intended state does not justify reconnection.

## Use When
Use when known valuable or indexable assets are absent from navigable internal-link paths, or when architecture changes may have created orphaned destinations.

## Process
1. Compare the set of known relevant assets with what can actually be reached through meaningful navigable internal links. Distinguish true orphans from intentionally isolated utility, campaign, private, or transitional pages.
2. Evaluate orphan candidates using business purpose, demand, traffic, conversions, backlinks/referrals, index state, freshness, content quality, and relationship to other assets.
3. Decide the intended outcome for each material candidate: remain independent and receive links, merge with another destination, redirect to a true replacement, update, noindex/remove, or remain intentionally isolated.
4. For retained pages, choose source pages and placements that are contextually useful rather than adding sitewide filler links simply to eliminate an orphan count.
5. If implementation is requested and the host can perform it, make the smallest useful changes and update dependent relationships when necessary.
6. Re-crawl or otherwise inspect the affected paths to verify the orphan condition is resolved as intended without creating duplicate intent, misleading navigation, or unnecessary hierarchy changes.

## Proportional Scope
Prioritize high-value or systematically orphaned asset classes. On large sites, diagnose template, publishing, migration, or architecture causes before treating thousands of URLs as independent tasks.
