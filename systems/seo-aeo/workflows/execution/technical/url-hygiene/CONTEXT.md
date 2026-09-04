---
id: seo.execution.technical.url-hygiene
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
# URL Hygiene

## Purpose
Keep URL generation stable and intentional so operational parameters and generated variants do not create unnecessary crawl/index complexity or needless migrations.

## Business Outcome
Prevent uncontrolled URL-variant growth while preserving distinct URLs that serve real customer, market, product, or content needs.

## Run When
Use when URL patterns, parameters, generated routes, alternate views, or proposed URL changes may be creating unnecessary variants or unstable discovery behavior.

## Process
1. Inspect the relevant URL patterns and parameter combinations at a scope sufficient to reveal the generation rules rather than treating each observed URL as an independent problem.
2. Identify session, tracking, sort/filter, search, calendar, printer, duplicate-path, case/protocol/host, generated, or other variants that may create operational noise.
3. Determine which variants represent distinct useful demand or functionality and which are merely alternate technical representations of the same resource.
4. Define stable URL-generation, crawl, index, and canonical behavior appropriate to each pattern, using the actual platform/site capabilities rather than prescribing one implementation.
5. Avoid changing stable functional URLs for cosmetic keyword or style reasons when the migration cost/risk exceeds the likely value.
6. When URL changes are genuinely necessary, use the relevant redirect, canonical, internal-link, sitemap, hreflang, and migration safeguards directly and verify representative/high-value paths.

## Proportionate Scope
Analyze representative patterns first. Expand toward full parameter/pattern enumeration when the site generates URLs combinatorially, crawl/index impact is material, or sampling cannot establish the rules safely.

## Verification
- Useful functional or demand-serving variants are not removed merely to reduce URL count.
- Stable URLs are preferred over cosmetic churn.
- URL-generation rules and discovery/index treatment are coherent enough that the same unwanted variant class does not immediately reappear.
