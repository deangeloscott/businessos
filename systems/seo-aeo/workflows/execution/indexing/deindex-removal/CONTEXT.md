---
id: seo.execution.indexing.deindex-removal
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
- crawl/index state HTTP behavior and URL relationships
---
# Deindexing and Removal

## Purpose
Remove, consolidate, restrict, or retire URLs intentionally while protecting users, valid replacements, accumulated signals, legal obligations, and business continuity.

## Business Outcome
Make unwanted or obsolete URLs leave discovery in the correct way without sacrificing useful traffic, links, customer access, or factual/legal requirements unnecessarily.

## Use When
Use when a URL should no longer remain available or indexable in its current form, including retirement, consolidation, privacy/access changes, legal removal, temporary suppression, or replacement by a better destination.

## Process
1. Establish why the URL should change and the intended final state: updated content, redirect, gone/not found, noindex, access restriction, temporary search removal, or another justified outcome.
2. Inspect the material dependencies before changing it: user demand, traffic/conversions, backlinks/referrals, internal links, canonicals, hreflang, sitemap/feed references, embeds, campaigns, or other assets that could be affected.
3. Choose the method from the real user/business need. Redirect only when a genuinely relevant replacement exists; use noindex when users should still access the page but search inclusion is not wanted; use access controls for actual privacy/security needs; use removal tools only for the temporary/specific purposes they support.
4. For destructive or high-impact changes, respect the user's requested scope and any real organizational, legal, platform, or account constraints. Preserve a practical rollback or prior URL/content map when reversibility matters. AURA does not add a separate approval lifecycle.
5. If implementation is requested and the host has the necessary access, make the change and update dependent internal links, sitemaps, feeds, canonicals, or other discovery references that should follow the new state. Otherwise produce a precise implementation-ready plan without claiming execution.
6. Verify old/new URL behavior and observe material search, referral, link, or business effects when they matter. Record monitoring intent when future checks are useful; the host/runtime owns actual scheduling and alerts.

## Proportional Scope
For a small set of URLs, verify each consequential relationship directly. For large removals or consolidations, reason by URL class and root cause, then sample high-value and boundary cases deeply enough to protect the intended outcome.

## Verification
- The chosen final state matches the real reason for removal or consolidation.
- Redirects point to true replacements rather than unrelated destinations.
- A search-removal request or successful submission is not treated as proof of durable deindexing.
- Claims about traffic, ranking, or business impact match subsequent evidence rather than being assumed from the technical change.
