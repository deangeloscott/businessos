---
id: seo.intelligence.organic-demand.ai-prompt-expansion
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- SEOAssetState
- Asset
- MetricObservation
- Observation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
capabilities:
  required:
  - search.performance.read
  optional:
  - search.serp.read
  - ai_answer.observe
  - analytics.read
  - research.web.read
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- Market search answer evidence
- prompt/question observations, answer text, citations, mentions, and competing sources
- records topic intent evidence
updates:
  OrganicDemandUnit:
  - business_value
  - demand_evidence
---
# AI Prompt Expansion

## Purpose
Translate buyer needs into realistic conversational question/prompt families and discover follow-up constraints.

## Business Outcome
Improve valuable organic discovery through ai prompt expansion, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **ai prompt expansion** evidence.

## Process
1. [HYBRID] Start with target audience, awareness/buying stage, jobs/problems, offer, queries, objections, and comparison criteria.
2. [AI] Generate broad discovery, diagnosis, recommendation, comparison, constraint, local, budget, integration, risk, trust, implementation, and verification prompts.
3. [HYBRID] Create natural follow-up chains because users may refine an answer conversationally rather than issue one isolated query.
4. [HYBRID] Integrate observed AI grounding queries, sales/support questions, and prompt data where available.
5. [HYBRID] Cluster semantic equivalents while retaining materially different constraints and high-value intent.
6. [AI] Map each prompt cluster to relevant surface(s), business value, likely answer format, and target asset/entity.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.

## Verification
- Store the exact prompt/question, surface, timestamp, answer evidence and citation/mention status so observations are reproducible.


