---
id: seo.intelligence.organic-competition.discover-answer
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
writes:
- OrganicCompetitorState
- MetricObservation
- Observation
- Competitor
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
---
# Answer Competitor / Source Discovery

## Purpose
Identify the brands, publishers, communities, databases, marketplaces, and other sources that materially shape answer-engine visibility without maintaining a duplicate broad business-competitor profile.

## Business Outcome
Understand who or what is actually earning recommendations, mentions, and citations for important questions so the organization can make better organic/AEO decisions.

## Run When
Use when answer-engine competitor/source discovery is needed to explain competitive visibility, identify important source patterns, or find material gaps.

## Process
1. [HYBRID] Select a representative set of important prompt/question clusters across the answer surfaces that materially matter to the organization. Scope depth to the business value and uncertainty of the question rather than sampling everything available.
2. [AI] Extract recommended/mentioned entities and cited domains/pages with enough context to preserve what was actually observed.
3. [AI] Aggregate mention, recommendation, and citation coverage in a way that reflects the value and relevance of the underlying prompts rather than treating every appearance equally.
4. [AI] Distinguish competitor brands from neutral authorities, communities, databases, publishers, marketplaces, and other source roles. Do not label every visible domain a business competitor.
5. [HYBRID] Link to OrganicCompetitorState and canonical Competitor records when the same real entity appears, while preserving the answer-source role and observation context.
6. [AI] Identify material patterns, gaps, or changes worth acting on or remembering. An actionable gap does not require a new Opportunity object unless that durable meaning will help future work.

## Verification
- Store or preserve the exact prompt/question, surface, timestamp, answer evidence, and citation/mention status when reproducibility matters.
- Observed answer visibility is not treated as proof of authority, profitability, causality, or customer preference.
- Competitor identity and source role remain distinct.
