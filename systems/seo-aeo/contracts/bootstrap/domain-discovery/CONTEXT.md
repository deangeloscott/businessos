---
id: seo.bootstrap.domain-discovery
type: playbook
owner_system: seo-aeo
reads:
- Asset
writes:
- OrganicDemandUnit
- SEOAssetState
- OrganicCompetitorState
- Observation
capabilities:
  required:
  - webpage.fetch
  optional:
  - crawler.run
  - search.performance.read
  - analytics.read
context:
- Brand
- Business
- Market
- Offer
- ProductService
---
# SEO Domain Discovery

## Purpose
Initialize SEO-specific scope from minimal business information without recreating general Business Context, host capability state, or a parallel context-change workflow.

## Business Outcome
Establish the owned web/discovery surfaces and SEO-specific state needed for useful organic-discovery work while preserving organization truth boundaries.

## Run When
Run when SEO/AEO bootstrap or later diagnosis needs a grounded view of the owned web presence and relevant discovery surfaces.

## Do Not Run When
Do not use this contract to duplicate canonical customer, competitor, industry, content, marketing, journey, or general Business Context ownership.

## Process
1. [INTEGRATION] Using the active harness's available web capabilities, fetch the owned website/domain and resolve canonical host/protocol, reachable subdomains, locale/location variants, and obvious public site boundaries.
2. [AI] Identify SEO-relevant products/services, markets, page types, discovery surfaces, and likely commercial/informational entry points while treating business facts not established in Core context as provisional.
3. [DETERMINISTIC] Inventory mechanically observable URL/template, robots/sitemap, redirect, and existing analytics/search identifiers when actually available. Technology/CMS identity stays provisional when it requires interpretation rather than exact evidence.
4. [AI] Judge search/AEO/local applicability, major technical constraints, known migrations, and properties requiring separate SEO state from the evidence available.
5. [AI] If owned-surface evidence reveals a material possible correction to general Business Context, surface the evidence and proposed correction explicitly rather than silently rewriting Core-owned truth or creating an SEO-specific approval/proposal lifecycle. Persist an Observation when the evidence itself has future value. A current authoritative correction can be applied through normal Core memory semantics; an unresolved ContextUpdateProposal is optional only when remembering the unresolved possibility would materially help future work.
6. [DETERMINISTIC] Persist only the SEO-specific state and exact observations that future organizational work would materially benefit from.

## Verification
- Validate written AURA state, preserve evidence lineage, and keep unavailable host/tool data explicitly unknown rather than inventing capability state.
- General Business Context is not duplicated or controlled by SEO.

## Measurement
- Establish relevant baseline measures when trustworthy first-party or observable evidence is available and downstream work actually needs them.

## Learning
- Later OutcomeEvaluation evidence may inform SEO Domain Learning when it materially changes what the organization should remember about its organic-discovery work.

## Failure / Fallback
- If a preferred tool is unavailable, use another valid method available to the active harness when practical. Otherwise preserve the unresolved evidence need honestly; do not create a fake CapabilityBinding or pretend the inspection occurred.

## Completion Criteria
- Useful SEO-specific bootstrap state exists, validates, and preserves the boundary between observed owned-surface evidence and general organization truth.
