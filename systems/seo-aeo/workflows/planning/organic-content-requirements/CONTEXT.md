---
id: seo.planning.organic-content-requirements
type: workflow
owner_system: seo-aeo
reads:
- Opportunity
- OrganicDemandUnit
- SEOAssetState
- type: Insight
  domain: customer-intelligence
- type: Insight
  domain: competitor-intelligence
- OrganicCompetitorState
writes:
- Asset
context:
- Brand
- Offer
---
# Organic Content Requirements

## Purpose
Turn current organic-demand, search/answer, customer, competitor, and business evidence into the requirements a useful content asset should satisfy without making another model rediscover the SEO/AEO problem.

## Business Outcome
Improve the quality and business relevance of content intended for organic/search/AI-answer discovery while keeping SEO requirements separate from creative execution and persuasion judgment.

## Run When
Use when a new or revised content asset needs materially important organic-discovery requirements. An existing Opportunity may provide context but is not required merely to use this method.

## Do Not Run When
Do not add an SEO requirements layer when organic/search/answer discovery is not material to the asset or when current requirements are already sufficient and fresh.

## Process
1. [AI] Define the target audience/market, organic demand or question, intent/user task, desired business pathway, and why an owned asset is needed or needs revision.
2. [HYBRID] Inspect current search/answer expectations, owned overlap/cannibalization, relevant competitors/sources, citation patterns, first-party performance, and information gaps only to the depth that can change the requirements.
3. [AI] Specify must-answer questions, factual/entity coverage, differentiated/original evidence needs, proof, useful media/demonstration, exclusions, and uncertainty that the content must preserve.
4. [HYBRID] Define search-presentation needs, internal-link/architecture context, structured-data eligibility, localization, crawl/index considerations, and AI-answer/source requirements only where actually relevant.
5. [AI] Keep organic-discovery requirements separate from creative format and persuasion strategy. Reuse current Brand/Offer/Customer/Marketing context directly where useful rather than routing a request to another AURA system.
6. [AI] Define the measurements/observations that would later show whether the intended organic mechanism occurred, without forecasting unobserved rankings, citations, traffic, leads, or revenue.
7. [AI] Produce a concise requirements brief that references durable evidence instead of copying upstream research. Persist it as an organization-owned `Asset` only when future sessions/actors materially benefit; otherwise use the requirements directly in the current work.
8. [AI] If a real handoff across people/models/sessions must survive the current runtime, `core.continuity.manage-handoff` may preserve that organizational handoff separately. This playbook does not create a WorkRequest merely to move work from SEO to Content.

## Verification
- Requirements trace to current business/search/customer/competitor evidence where those dimensions materially matter.
- SEO requirements do not invent company claims, ranking guarantees, citation guarantees, or persuasion strategy.
- The requirements are specific enough to materially improve production but do not dictate unnecessary creative choices.
- No internal routing, return contract, manual-action fallback, or downstream event is required.

## Completion Criteria
- A capable model can produce or revise the intended content without rebuilding the organic-discovery analysis, and any persisted brief is durable organizational knowledge rather than an internal delegation packet.
