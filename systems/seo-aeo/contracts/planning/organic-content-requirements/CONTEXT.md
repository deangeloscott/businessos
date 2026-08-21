---
id: seo.planning.organic-content-requirements
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- Opportunity
- OrganicDemandUnit
- SEOAssetState
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- OrganicCompetitorState
writes:
- WorkRequest
- ActionPacket
capabilities:
  required:
  - none
  optional:
  - search.serp.read
  - ai_answer.observe
  - search.performance.read
context:
- Brand
- Offer
---
# Organic Content Requirements

## Purpose
Translate a qualified SEO content Opportunity into a complete organic-discovery requirement set that Content Synthesis can execute without rediscovering SEO strategy.

## Business Outcome
Establish or execute the SEO/AEO capability needed to improve valuable organic discovery.

## Run When
Run when the scoped SEO/AEO job is required by bootstrap, diagnosis, Opportunity planning, or delegated execution.

## Do Not Run When
Do not use this contract to duplicate canonical customer, competitor, industry, content, marketing, or journey ownership.

## Process
1. [AI] Restate target organic demand, audience/market, intent, user task, business conversion path, and why a new/updated Asset is needed.
2. [HYBRID] Analyze current result/answer expectations, owned overlap/cannibalization, organic competitors/sources, AEO citation patterns, and information gaps.
3. [AI] Specify must-answer questions, factual/entity coverage, differentiated/original evidence needs, proof, media/demonstration, and exclusions.
4. [HYBRID] Define search presentation needs, internal links, architecture placement/URL constraints, structured-data eligibility, localization, and AEO/source requirements.
5. [AI] Define CTA/commercial handoff requirements without inventing persuasion strategy; request Marketing input where material.
6. [HYBRID] Define SEO success/guardrail metrics and verification assertions.
7. [DETERMINISTIC] Create a Content Synthesis WorkRequest with exact requirements and return contract; retain SEO Opportunity ownership.

## Verification
- Validate all written objects and independently verify external state changes.

## Measurement
- Define the SEO mechanism metric and relevant business outcome before execution when this contract changes external state.

## Learning
- Return OutcomeEvaluation evidence to SEO Domain Learning and relevant upstream/downstream systems.

## Failure / Fallback
- Missing tools create manual work; missing upstream intelligence permits bounded provisional SEO research with source provenance.

## Completion Criteria
- The required SEO output exists, validates, and has explicit lineage/next route.
