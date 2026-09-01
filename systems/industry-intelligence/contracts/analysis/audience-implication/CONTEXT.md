---
id: industry.analysis.audience-implication
type: playbook
owner_system: industry-intelligence
reads:
- IndustryEvent
- Insight
- Observation
- SourceRecord
writes:
- Insight
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - news.read
  - regulatory.read
  - research.paper.read
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
Give Content, Marketing, Customer Intelligence, SEO/AEO, and business operators a trustworthy factual base plus clear audience-specific implications, opportunities, and protective actions.

## Run When
Run after an IndustryEvent has been verified/materially assessed and a priority audience or business context may be affected.

## Process
1. [DETERMINISTIC] Resolve the verified IndustryEvent, strongest SourceRecords/Observations, existing Industry Insight, affected market, audience, product/offer, timeline, and unresolved factual uncertainty.
2. [AI] Write a concise factual event summary containing only supported facts: what changed, who/what is affected, when, and what remains unknown.
3. [AI] Analyze the audience/business mechanism separately: what may change in cost, risk, behavior, opportunity, compliance, technology, competition, customer expectation, or decision-making.
4. [AI] Generate the practical “so what” for the target audience: what to understand, watch, do, avoid, take advantage of, or protect against—clearly labeling scenario/hypothesis versus confirmed requirement.
5. [HYBRID] Test relevance against active Objectives, products/offers, Customer/Competitor Insights, materiality, timing, and contradictory evidence; avoid manufacturing urgency merely because the story is topical.
6. [HYBRID] Publish/update an Industry Insight containing factual basis, scoped implication, confidence, timing, and applicability; preserve sources rather than copying entire articles.
7. [DETERMINISTIC] Emit the audience-implication event so Content and other systems can evaluate the signal independently.
