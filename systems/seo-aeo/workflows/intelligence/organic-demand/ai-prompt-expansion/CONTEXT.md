---
id: seo.intelligence.organic-demand.ai-prompt-expansion
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- Observation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
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
Translate real buyer needs into realistic conversational prompt/question families, including the constraints and follow-ups that can change what a useful answer requires.

## Business Outcome
Understand demand that may appear in AI-answer and conversational discovery so the organization can earn more relevant visibility, attention, and downstream business opportunity without mistaking generated prompt volume for observed demand.

## Run When
Use when conversational or AI-answer demand is materially relevant and existing search/customer evidence does not fully represent how people may ask, refine, compare, or constrain the problem.

## Process
1. [HYBRID] Start from established audience, problem/job, awareness or buying stage, Offer, search queries, objections, comparison criteria, sales/support language, and observed prompt evidence where available.
2. [AI] Expand into realistic discovery, diagnosis, recommendation, comparison, constraint, local, budget, integration, risk, trust, implementation, and verification questions that a real user could plausibly ask.
3. [AI] Model useful follow-up chains when the answer changes as the user adds constraints; do not treat every wording variation as a distinct need.
4. [HYBRID] Use observed AI prompts, answer behavior, grounding queries, site/customer language, or other evidence to calibrate generated possibilities. Keep generated hypotheses distinguishable from observed demand.
5. [AI] Cluster semantic equivalents while preserving materially different constraints, intents, audiences, markets, or decision stages.
6. [AI] Map useful prompt clusters to relevant answer surfaces, business-value pathways, likely answer needs, and owned or missing assets/entities only to the depth needed for the current decision.
7. [HYBRID] Preserve material OrganicDemandUnits or observations when future work benefits; do not create records for every generated prompt variant.

## Verification
- Generated prompts are labeled as hypotheses unless supported by observed evidence.
- Exact observed prompts/questions, surfaces, timestamps, answers, citations, and mention status remain reproducible when material.
- AI visibility is treated as a meaningful upstream opportunity signal when it can increase exposure or consideration, while downstream traffic, leads, or revenue remain separate observed outcomes.
- Competitor research or Opportunity creation is optional and used only when it materially improves the next decision.
