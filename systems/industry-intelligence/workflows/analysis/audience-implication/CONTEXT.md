---
id: industry.analysis.audience-implication
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- Insight
- Observation
- SourceRecord
writes:
- Insight
context:
- AudienceSegment
- Market
- ProductService
- Offer
- Objective
---
# Audience Implication of an Industry Event

## Purpose
Separate “what happened” from “why this matters to this audience/business” so downstream communication can be useful without distorting the underlying event.

## Business Outcome
Give future organizational work a trustworthy factual base plus clear audience-specific implications without creating a cross-system dispatch event.

## Run When
Use after an IndustryEvent has been verified/materially assessed and a priority audience or business context may be affected.

## Process
1. [HYBRID] Resolve the verified IndustryEvent, strongest SourceRecords/Observations, existing Industry Insight, affected market, audience, product/offer, timeline, and unresolved factual uncertainty. Exact refs/dates are mechanical; applicability is model judgment.
2. [AI] Write a concise factual event summary containing only supported facts: what changed, who/what is affected, when, and what remains unknown.
3. [AI] Analyze the audience/business mechanism separately: what may change in cost, risk, behavior, opportunity, compliance, technology, competition, customer expectation, or decision-making.
4. [AI] Generate the practical “so what” for the target audience: what to understand, watch, do, avoid, take advantage of, or protect against—clearly labeling scenario/hypothesis versus confirmed requirement.
5. [HYBRID] Test relevance against active Objectives, products/offers, Customer/Competitor Insights, materiality, timing, and contradictory evidence; avoid manufacturing urgency merely because the story is topical.
6. [HYBRID] Preserve/update an Industry Insight containing factual basis, scoped implication, confidence, timing, and applicability; preserve source references rather than copying entire articles.

## Verification
- Factual event state and audience/business interpretation remain distinct.
- Material implications remain evidence-linked and appropriately scoped.
- Content, Marketing, Customer Intelligence, SEO/AEO, or another model-selected method may reuse the Insight normally; AURA does not emit a dispatch event to make that happen.
