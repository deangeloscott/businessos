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
# Prune & Consolidate

## Purpose
Improve, merge, archive, redirect, noindex, or remove content only when evidence shows it should not remain independently available in its current form.

## Business Outcome
Reduce genuinely low-value or duplicative content while preserving useful demand, links, conversions, customer utility, historical value, and legitimate archival needs.

## Use When
Use when content appears materially outdated, duplicative, low-utility, strategically misaligned, costly to maintain, or better served by another destination.

## Process
1. Identify candidates using meaningful evidence such as duplication, outdatedness, lack of demand or utility, weak quality, maintenance burden, or strategic mismatch. Low traffic alone is not sufficient proof that a page has no value.
2. Check historical traffic, backlinks/referrals, assisted conversions, support/customer value, branded demand, seasonality, legal/archive requirements, and relationships to other assets.
3. Choose the outcome that best preserves useful value: improve, merge, archive, redirect to a true replacement, noindex, or remove.
4. Before destructive changes, map the content, links, proof, conversion paths, and other legitimate value that should survive elsewhere.
5. If implementation is requested, update redirects, internal links, navigation, sitemaps/feeds, canonicals, and dependent relationships as needed to match the intended state.
6. Verify the resulting old/new behavior and observe material discovery or business effects when they matter. AURA may preserve useful monitoring intent; the host owns recurrence.

## Proportional Scope
Prioritize content classes with the clearest evidence and highest maintenance or discovery impact. On large sites, reason by pattern and representative examples before executing mass removal.
