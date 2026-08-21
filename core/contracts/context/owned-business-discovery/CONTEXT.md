---
id: core.context.owned-business-discovery
type: playbook
version: 1.8.0
owner_system: core
risk: low
autonomy_ceiling: 2
reads:
- Business
- Brand
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
- SourceRecord
- Observation
writes:
- Business
- Brand
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
- SourceRecord
- Observation
- ContextUpdateProposal
capabilities:
  required:
  - none
  optional:
  - webpage.fetch
  - webpage.snapshot
  - crawler.run
  - browser.interact
  - research.web.read
  - social.observe
  - review.read
  - news.read
  - search.observe
  - document.read
  - business.data.query
  - business.data.explain
context:
- Business
- Brand
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
---
# Adaptive Owned Business Discovery

## Purpose
Build an evidence-backed map of the business and its official/public surfaces at the depth needed for the current job, instead of repeatedly asking the user for information the system can safely discover.

## Business Outcome
Give every installed module reliable Business Context from minimal input while preserving the difference between owned facts, provisional inference, public perception, and unknowns.

## Run When
Run during initial business setup, when the business changes materially, or when the active job needs broader owned-business context than is currently canonical.

## Process
1. [AI] Set discovery depth from the decision/job: **Rapid** for only the context needed to unblock one bounded task, **Standard** for a normal new installation, or **Comprehensive** when the user asks the system to learn/map the business broadly. Do not perform exhaustive onboarding when it cannot change the current decision.
2. [HYBRID] Establish the business identity and authoritative first-party anchors: primary domain, supplied files, explicit user statements, known legal/product/brand identities, confirmed owned properties, and relevant authoritative facts already available through connected governed business-data sources. Reuse those sources before asking the user or rediscovering the same fact publicly.
3. [INTEGRATION] Discover relevant first-party surfaces through navigation, sitemaps, crawl/search, docs/help, products/services, pricing/offers, landing pages, case studies/proof, resources, releases, careers, legal/about/contact, locations, and public conversion paths as depth warrants. Examples are non-exhaustive; pursue additional credible owned surfaces when useful.
4. [HYBRID] Resolve official external properties such as social profiles, app/marketplace listings, public business profiles, and review profiles using first-party links plus corroborating identity evidence. Similar names alone are insufficient.
5. [AI] Extract explicit owned facts into candidate Business/Brand/ProductService/Offer/AudienceSegment/Market/Objective state. Keep public reputation, reviews, social discussion, search presentation, and news as Observations rather than silently rewriting what the business officially is or claims.
6. [AI] Compare discovered state with current canonical context. Label each material item as observed/explicit, provisional inference, contradictory/stale, or unknown; create ContextUpdateProposal when an inferred change would overwrite a material existing business decision.
7. [HYBRID] Identify installed-module baselines that would materially improve the user's goal (for example competitor, customer, industry, SEO/AEO, content, marketing, or customer-journey analysis). Route those as next jobs to their semantic owners instead of putting their domain intelligence into Core.
8. [DETERMINISTIC] Record source coverage, retrieval time, relevant snapshots/hashes/references, provider query/artifact references where used, schema-valid writes, and unresolved gaps. Keep large/raw connected-system history in its authoritative system rather than duplicating it locally. Stop when additional discovery is unlikely to change the current job or when the requested depth is satisfied.

## Verification
The active business has enough current, evidence-linked context for the requested work; owned facts are not conflated with public perception, and the system can state what surfaces were checked, skipped, unavailable, or still unknown.
