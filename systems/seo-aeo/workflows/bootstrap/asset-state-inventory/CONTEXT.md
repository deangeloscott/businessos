---
id: seo.bootstrap.asset-state-inventory
type: workflow
owner_system: seo-aeo
reads:
- Asset
writes:
- SEOAssetState
- Observation
- Asset
context:
- Brand
- Business
- Market
- Offer
- ProductService
---
# SEO Asset State Inventory

## Purpose
Understand the current search-relevant state of owned pages/assets while keeping one canonical Asset identity and preserving only SEO-specific state that future work will actually reuse.

## Business Outcome
Give future SEO/AEO work a trustworthy view of what owned assets exist, how they are technically/search-wise represented, and where material evidence gaps remain without rebuilding the site inventory on every task.

## Run When
Use when current owned-asset state is missing, materially stale, or needed for a concrete SEO/AEO diagnosis, plan, or measurement question.

## Do Not Run When
Do not inventory the entire site merely because an SEO task exists. Reuse current Asset/SEOAssetState evidence and inspect only the surfaces needed for the real job.

## Process
1. [HYBRID] Reuse known canonical Assets first, then inspect the relevant owned surfaces through whatever real host methods are available: sitemap/site crawl, CMS, local export, search/index evidence, analytics, or direct page inspection.
2. [AI] Resolve observed pages/items to existing canonical Assets by real identity. Create a new Asset only when an independently meaningful owned asset is genuinely missing; do not duplicate an Asset merely to attach SEO state.
3. [HYBRID] Collect only decision-relevant SEO state for the scoped assets, such as URL/status, indexability/canonical signals, render/accessibility, search performance, structured data, internal-link context, page/template type, market/language, and organic role when supported.
4. [AI] Distinguish directly observed site facts from interpretations such as severity, likely intent, opportunity, or expected impact.
5. [DETERMINISTIC] Create/update `SEOAssetState` keyed to the canonical Asset and persist material direct Observations/evidence when future work benefits. Do not copy generic Asset truth into parallel SEO objects.
6. [AI] State material unknowns or stale evidence honestly. A missing host tool is not an AURA setup/manual-action object; use another valid evidence source when sufficient or preserve the limitation.

## Deterministic local-site evidence
When the scoped evidence is a local/first-party website export, `scripts/inspect_site_evidence.py` and `scripts/persist_site_observation.py` may mechanically capture/persist material direct facts. Keep consequences, severity, and visibility implications as model/user inference unless separately measured. Follow `core/policies/local-evidence.md`.

## Verification
- Canonical Asset identity is preserved rather than duplicated.
- SEOAssetState is evidence-linked and contains SEO-specific reusable state rather than generic copies.
- Direct observations remain distinct from interpretation and forecast.
- The method does not create internal routes, manual-action fallbacks, or capability inventories.

## Completion Criteria
Future SEO/AEO work can understand the scoped owned-asset state and material unknowns without repeating unnecessary discovery, and no execution-control lifecycle was created.
