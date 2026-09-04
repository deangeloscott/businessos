---
id: seo.execution.internal-linking.broken-internal-links
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
# Broken Internal Links

## Purpose
Find and repair internal links that lead to errors, unnecessary redirects, incorrect destinations, noncanonical variants, or retired assets.

## Business Outcome
Keep important internal pathways reliable for users and discovery systems while exposing recurring template or CMS causes instead of repeatedly patching symptoms.

## Use When
Use when internal links produce errors, redirect chains, irrelevant redirects, soft-error destinations, stale references, or inconsistent canonical targets.

## Process
1. Inspect the internal-link relationships that matter and classify the actual failure: hard error, soft error, redirect chain, irrelevant redirect, noncanonical target, retired destination, or another mismatch.
2. Recover the intended destination from surrounding context, historical content, redirects, sitemaps, asset records, or other reliable evidence rather than guessing from the URL alone.
3. Choose the best correction: update the source link, restore the needed destination, remove the link, fix the redirect, or point to the true replacement.
4. Prefer correcting links at the source where practical rather than relying indefinitely on avoidable redirect chains.
5. If implementation is requested and the host can perform it, make the change and verify each material source-target relationship affected by the correction.
6. When repeated breakage indicates a shared template, CMS, migration, or publishing cause, diagnose and fix that root pattern. Preserve monitoring intent only when recurrence materially matters; the host owns any later schedule.

## Proportional Scope
Fix high-value and systemic relationships first. For large sites, analyze recurring patterns and representative URL classes before attempting exhaustive per-link cleanup.
