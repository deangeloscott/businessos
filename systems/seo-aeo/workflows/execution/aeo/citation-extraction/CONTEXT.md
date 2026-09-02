---
id: seo.execution.aeo.citation-extraction
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- backlink/referring-domain/mention evidence and prospect records
---
# AI Citation and Link Extraction

## Purpose
Determine which sources and owned assets are cited or linked in answer-system observations and in what question contexts.

## Business Outcome
Make citation/source patterns interpretable enough to support useful AEO decisions without treating citation count as endorsement, traffic, or business value.

## Run When
Use when current Answer Observations contain citations, links, source cards, or source patterns relevant to a material AEO question.

## Process
1. Parse the relevant observations for explicit links, citations, source cards, or other attributable source references and normalize destination URLs/domains where useful.
2. Resolve important redirects/canonicals and classify sources as owned, competitor, neutral authority, community, marketplace, local/review, or another meaningful category when that distinction helps the decision.
3. Map a citation to the claim or answer section it appears to support when observable rather than assuming every source supports the whole answer.
4. Aggregate citation frequency and coverage by the dimensions that materially matter—such as prompt cluster, surface, topic, asset, competitor, or time period—without collapsing unlike contexts into one opaque score.
5. Distinguish citation presence from mention, recommendation, endorsement, referral traffic, and business outcome.
6. When the evidence reveals a meaningful source/information gap, use the relevant source-gap or other operating knowledge directly. Preserve an Opportunity only when durable coordination around the gap is useful.

## Proportionate Scope
Extract and aggregate only the source evidence needed for the current decision. Broaden across more prompts, surfaces, or time periods when the pattern is unstable or the additional evidence could materially change the conclusion.

## Verification
- Material citations remain traceable to the underlying observation and question context.
- Source identity and canonical resolution are accurate enough for the conclusion being drawn.
- Citation presence is never presented as proof of endorsement, traffic, profitability, or guaranteed future inclusion.
