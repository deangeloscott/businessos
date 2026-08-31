---
id: marketing.strategy.value-proposition
type: playbook
version: 1.1.0
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
capabilities:
  required:
  - none
  optional:
  - marketing.performance.read
  - conversion.read
  - analytics.read
context:
- AudienceSegment
- Brand
- Objective
- Offer
---
# Value Proposition Synthesis

## Purpose
Express why the defined audience should choose the offer relative to alternatives using supported value and proof.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed value proposition synthesis that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires value proposition synthesis to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Identify the audience desired outcome, existing alternatives/status quo, switching cost, decision criteria, and business advantage.
2. [AI] Separate feature, mechanism, benefit, outcome, economic value, emotional value, and proof.
3. [HYBRID] Quantify value only where evidence/economics support it; avoid fabricated ROI precision.
4. [AI] Generate value proposition variants emphasizing materially different customer value mechanisms.
5. [HYBRID] Evaluate relevance, differentiation, credibility, proof availability, and fit to Offer/Brand.
6. [AI] Select primary/secondary proposition and define scope/context.
