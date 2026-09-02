---
id: marketing.diagnosis.persuasion-barrier
type: workflow
owner_system: marketing-synthesis
reads:
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- MetricObservation
writes:
- Insight
- Opportunity
- WorkRequest
context:
- AudienceSegment
- Brand
- Objective
- Offer
---
# Persuasion Barrier Diagnosis

## Purpose
Determine why the current commercial communication may not move the right audience toward the desired action before generating new copy.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed persuasion barrier diagnosis that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires persuasion barrier diagnosis to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define target audience, awareness/buyer stage, desired action, Offer, acquisition context, and current message/asset path.
2. [HYBRID] Load relevant Customer Insights, Competitor Insights, Brand, proof Assets, performance, and journey observations.
3. [AI] Diagnose possible barriers: problem relevance, outcome clarity, differentiation, credibility/proof, objection, risk, effort, price/value, urgency, CTA, awareness mismatch, or message continuity.
4. [DETERMINISTIC] Compare funnel/asset metrics to locate where response deteriorates; distinguish persuasion from technical/journey friction.
5. [HYBRID] Test diagnosis against direct customer evidence and competing explanations.
6. [AI] State the smallest plausible persuasion intervention and what result would support/refute it.
7. [HYBRID] Create/update Marketing Opportunity only when the primary problem is persuasion/commercial communication; route journey problems to Customer Optimization.
