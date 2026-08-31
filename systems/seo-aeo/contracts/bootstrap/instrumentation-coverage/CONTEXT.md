---
id: seo.bootstrap.instrumentation-coverage
type: playbook
version: 1.1.0
owner_system: seo-aeo
reads: []
writes:
- Observation
capabilities:
  required:
  - none
  optional:
  - search.performance.read
  - analytics.read
  - search.rank.read
  - search.serp.read
  - search.index.inspect
  - crawler.run
  - backlink.read
  - local_profile.read
  - ai_answer.observe
  - revenue.read
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- Effective Capability Profile
---
# SEO Instrumentation Coverage

## Purpose
Assess whether available capabilities/data are sufficient to observe, diagnose, execute, and measure organic discovery.

## Business Outcome
Establish or execute the SEO/AEO capability needed to improve valuable organic discovery.

## Run When
Run when the scoped SEO/AEO job is required by bootstrap, diagnosis, Opportunity planning, or delegated execution.

## Do Not Run When
Do not use this contract to duplicate canonical customer, competitor, industry, content, marketing, or journey ownership.

## Process
1. [DETERMINISTIC] Compile SEO-required capabilities for applicable surfaces: search performance, analytics, rank/SERP, index inspection, crawl, backlinks, local, AI answers, CMS, revenue.
2. [DETERMINISTIC] Record available/partial/unavailable/approval-required coverage and data history/freshness for each.
3. [HYBRID] Identify which SEO diagnoses/measurements become unreliable or impossible under current coverage.
4. [AI] Prioritize missing instrumentation by expected decision value and whether a manual or lower-fidelity substitute exists.
5. [DETERMINISTIC] Create setup/manual actions for blocking gaps and declare confidence adjustments for partial data.
6. [HYBRID] Do not block unrelated SEO work when sufficient alternative evidence exists.

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
