---
id: seo.execution.on-page.freshness
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
# Freshness

## Purpose
Refresh content when changed facts, products, markets, user expectations, or quality standards make the current asset materially stale.

## Business Outcome
Keep important content accurate and useful without cosmetic date changes or unnecessary rewrites performed only to appear fresh.

## Use When
Use when material facts, examples, links, offers, screenshots, products, laws, staff, data, recommendations, or user expectations may have changed enough to affect usefulness or trust.

## Process
1. Identify the parts of the asset whose truth or usefulness is time-sensitive and gather evidence of what may have changed.
2. Compare the potential staleness with actual user demand, performance, business relevance, and maintenance cost. Do not update merely to change a publication date.
3. Research current authoritative information and current organization facts for the parts that genuinely need revision.
4. Update the substantive content, evidence, examples, media, links, offers, or recommendations that changed while preserving still-useful material.
5. Preserve what materially changed and why only when that history will improve future work; a ChangeEvent is not required for trivial edits.
6. Observe search, engagement, conversion, or other outcomes after an appropriate period when those effects matter to the objective. The host owns any future recheck schedule.

## Proportional Scope
Refresh the smallest portion needed to restore accuracy and usefulness. Broaden into a deeper rewrite when the page's intent, evidence base, competitive quality, or customer need has materially shifted.
