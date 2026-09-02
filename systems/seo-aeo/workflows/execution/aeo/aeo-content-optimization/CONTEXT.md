---
id: seo.execution.aeo.aeo-content-optimization
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
- OrganicDemandUnit
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- records topic intent evidence
---
# Answer-Oriented Content Optimization

## Purpose
Improve owned information so it is clear, useful, evidence-rich, retrievable, and appropriate for both human search and answer systems.

## Business Outcome
Improve valuable organic discovery through answer-oriented content optimization, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **Answer-Oriented Content Optimization**, or when an authorized incident response requires it.

## Process
1. [AI] Start from a diagnosed prompt/answer/source gap and the existing target asset; do not create a separate 'AI page' without user need.
2. [HYBRID] Ensure the page directly resolves the target question/intent with clear terminology, scoped answers, supporting explanation, and useful next actions.
3. [HYBRID] Add or improve original evidence, citations to authoritative sources, product/service facts, definitions, comparisons, tables/lists only when useful, and entity relationships.
4. [HYBRID] Remove unsupported claims, filler, hidden content, or machine-targeted text that reduces human usefulness.
5. [HYBRID] Verify crawl/index eligibility, internal linking, canonical consistency, structured data matching visible content, and conversion alignment.
6. [AI] Define SEO measurement / Core OutcomeEvaluation for search, answer citations/mentions/recommendations, referral traffic, and business outcomes separately.


