---
id: seo.execution.on-page.prune-consolidate
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
# Prune Consolidate

## Purpose
Remove or consolidate low-value content only when evidence shows it should not remain independently available.

## Business Outcome
Improve valuable organic discovery through prune consolidate, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Prune Consolidate**, or when an authorized incident response requires it.

## Process
1. [AI] Identify candidates using duplication, outdatedness, no demand, low utility, quality, maintenance burden, or strategic mismatch.
2. [HYBRID] Check historical traffic, links, assisted conversions, support/brand value, seasonal demand, and legal/archive needs.
3. [HYBRID] Choose improve, merge, archive, redirect, noindex, or remove.
4. [AI] Map retained content/value and destination before deletion.
5. [HYBRID] Update redirects, links, sitemaps, canonicals, navigation, and feeds where needed.
6. [HYBRID] Verify and define SEO monitoring for destination/sitewide effects.


