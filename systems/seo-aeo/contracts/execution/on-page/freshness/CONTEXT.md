---
id: seo.execution.on-page.freshness
type: playbook
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - cms.page.read
  optional:
  - search.serp.read
  - search.performance.read
  - cms.page.update
---
# Freshness

## Purpose
Refresh content when changed facts, market conditions, user expectations, or competitive quality make it stale.

## Business Outcome
Improve valuable organic discovery through freshness, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Freshness**, or when an authorized incident response requires it.

## Process
1. [AI] Identify facts, data, examples, links, offers, screenshots, product details, laws, staff, and dates that may be stale.
2. [HYBRID] Compare update need with actual demand/performance/user relevance; do not cosmetically change publication dates.
3. [AI] Research current authoritative information and current brand facts.
4. [HYBRID] Update substantive content, evidence, examples, media, and internal/external links.
5. [DETERMINISTIC] Record what materially changed and why.
6. [HYBRID] Define SEO measurement / Core OutcomeEvaluation for after an appropriate observation window.


