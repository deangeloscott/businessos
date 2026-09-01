---
id: marketing.strategy.positioning
type: playbook
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
# Commercial Positioning Synthesis

## Purpose
Translate business/customer/competitive truth into a defensible commercial position for a defined audience and context.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed positioning that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a defined audience/context needs a clearer or stronger commercial position. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Load current business/product/Offer/Brand truth plus relevant Customer/Competitor evidence and proof.
2. [AI] Map customer priority outcomes/criteria, alternatives, competitor positions, business strengths, constraints, and proof strength.
3. [AI] Generate positioning options specifying target, frame/category, primary value, differentiated mechanism/advantage, alternative, and proof.
4. [HYBRID] Reject options that depend on capabilities/claims the business cannot support or that are indistinguishable in the market.
5. [HYBRID] Evaluate options for relevance, credibility, differentiation, strategic durability, economics, and downstream execution consistency.
6. [AI] Select a scoped commercial position and define where it applies; do not silently rewrite canonical Brand/business truth.
7. [HYBRID] Preserve the useful positioning as a Marketing-owned strategy Asset. If the organization actually establishes a durable Brand/Offer/business change, update that canonical truth through the normal current-context path with provenance. If the change remains merely proposed, keep it clearly candidate strategy; do not manufacture a ContextUpdateProposal, Opportunity, or WorkRequest solely because positioning was explored.
