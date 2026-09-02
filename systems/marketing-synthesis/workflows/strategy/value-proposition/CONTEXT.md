---
id: marketing.strategy.value-proposition
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
- Asset
context:
- AudienceSegment
- Brand
- Objective
- Offer
---
# Value Proposition Synthesis

## Purpose
Express why the defined audience should choose the Offer relative to alternatives using supported value and proof.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed value proposition that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a defined audience/context needs a clearer or stronger value proposition. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Identify the audience desired outcome, existing alternatives/status quo, switching cost, decision criteria, and business advantage.
2. [AI] Separate feature, mechanism, benefit, outcome, economic value, emotional value, and proof.
3. [HYBRID] Quantify value only where evidence/economics support it; avoid fabricated ROI precision.
4. [AI] Generate value proposition variants emphasizing materially different customer value mechanisms.
5. [HYBRID] Evaluate relevance, differentiation, credibility, proof availability, and fit to Offer/Brand.
6. [AI] Select primary/secondary proposition and define scope/context.
7. [AI] Preserve the useful proposition and its evidence/usage scope as a Marketing-owned strategy Asset. Create a separate Opportunity, WorkRequest, or canonical context change only when that distinct meaning actually exists.
