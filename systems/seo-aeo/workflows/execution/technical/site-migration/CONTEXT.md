---
id: seo.execution.technical.site-migration
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
- Incident
---
# Site Migration

## Purpose
Plan, execute, and verify a domain, CMS, architecture, platform, or URL migration while protecting organic discovery, attribution, and recoverability.

## Business Outcome
Move the site to its intended new state with the least avoidable loss of search/answer visibility, user access, measurement continuity, and accumulated URL/link signals.

## Run When
Use for a planned migration or when a recent migration is plausibly causing material discovery problems. Migration scope and verification depth should reflect the affected surface, business stakes, uncertainty, and reversibility.

## Process
1. [HYBRID] Establish the pre-migration truth needed for comparison and rollback: material URL/asset inventory, search and analytics/business baseline, observed index state, important backlinks/referring URLs, canonicals, hreflang where relevant, sitemaps, crawl/index directives, key templates, forms, feeds, ownership/verification, and conversion/tracking behavior.
2. [AI] Define the intended destination state. Create intent-correct old→new mappings to the closest true equivalents, including redirects, canonicals, hreflang relationships where relevant, intentional removals/consolidations, and URLs that should remain unchanged. Do not redirect every removed URL to an unrelated homepage merely to avoid a 404.
3. [HYBRID] Validate staging or the best available pre-launch representation for accidental blocking/indexability, duplicate exposure, content/metadata/structured-data parity where required, rendering, internal links/navigation, status behavior, performance, forms, analytics/conversion tracking, and server/platform behavior.
4. [AI] Limit unrelated simultaneous changes where practical when doing so materially improves post-launch diagnosability. Do not preserve obsolete structure merely for purity when the migration’s actual objective requires a coordinated change.
5. [HYBRID] Verify a representative sample plus the highest-value/risk URL classes before broad launch, including redirect chains/loops, canonical/robots conflicts, rendered content, tracking, and a credible rollback or correction path for material failures.
6. [HYBRID] Launch using the real host/platform controls available, updating redirects, canonicals, internal links, sitemaps, hreflang/feeds where applicable, verification/ownership, analytics, conversion tracking, and other dependent discovery surfaces to the intended state.
7. [HYBRID] Soon enough to catch consequential defects, crawl/test representative and high-value old/new URLs and inspect index/search/traffic/conversion/link/log evidence appropriate to the migration. Observation frequency should be higher while uncertainty and potential harm are high, then taper as evidence stabilizes; AURA does not own the schedule.
8. [AI] Diagnose residual mapping, template, access, rendering, canonical, internal-link, sitemap, index, tracking, or content-parity failures by common cause before generating repetitive per-URL fixes. Use the relevant diagnostic Workflow directly when a specialized problem emerges.
9. [HYBRID] Keep redirects and other continuity mechanisms as long as they continue to serve users, crawlers, or accumulated signals; do not remove them on an arbitrary short schedule. Preserve an Incident only when a severe migration problem benefits from durable cross-session coordination.
10. [AI] Close the migration as an operating concern when the intended state is sufficiently verified and material residual risks are resolved or consciously accepted. Preserve the mapping decisions, consequential changes, unresolved exceptions, outcomes, and reusable Learning that future work should know.

## Verification
- Affected URL classes and the highest-value/risk paths are tested before and after launch at depth proportionate to the migration.
- Redirect, canonical, crawl/index, rendering, internal-link, tracking, and sitemap/feed behavior agree with the intended state.
- Search/index/traffic/conversion changes are treated as observed evidence with appropriate uncertainty, not automatically attributed to the migration.
- Rollback/correction capability exists for material reversible failures where practical.
- Stabilization is evidence-based rather than a fixed calendar checkpoint.
