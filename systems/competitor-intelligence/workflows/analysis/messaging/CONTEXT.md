---
id: competitor.analysis.messaging
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  domain: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
context:
- AudienceSegment
- Brand
- Business
- Market
- Objective
- Offer
- ProductService
---
# Messaging Intelligence

## Purpose
Map competitor message hierarchy, claims, proof, objections, and creative themes without copying their messaging.

## Business Outcome
Improve competitive decisions through evidence-backed messaging intelligence, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current messaging intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Gather current public marketing/sales messages from prioritized surfaces.
2. [AI] Extract message hierarchy: headline promise, benefits, features, claims, proof, objections, CTA, urgency, and emotional/functional frames.
3. [AI] Group repeated message themes across channels and distinguish persistent strategy from one campaign execution.
4. [HYBRID] Check factual claims against source context and avoid treating marketing claims as independently verified truths.
5. [AI] Compare message emphasis against known customer criteria and competitors.
6. [HYBRID] Identify gaps/overlaps as competitive evidence, not automatic recommendations.
7. [DETERMINISTIC] Publish Observations/Insights with source/surface/date.
