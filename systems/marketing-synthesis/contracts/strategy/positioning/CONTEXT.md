---
id: marketing.strategy.positioning
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
# Commercial Positioning Synthesis

## Purpose
Translate business/customer/competitive truth into a defensible commercial position for a defined audience and context.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed commercial positioning synthesis that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires commercial positioning synthesis to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Load canonical business/product/offer positioning plus current Customer/Competitor Insights and proof.
2. [AI] Map customer priority outcomes/criteria, alternatives, competitor positions, business strengths, constraints, and proof strength.
3. [AI] Generate positioning options specifying target, frame/category, primary value, differentiated mechanism/advantage, alternative, and proof.
4. [HYBRID] Reject options that depend on capabilities/claims the business cannot support or that are indistinguishable in the market.
5. [HYBRID] Evaluate options for relevance, credibility, differentiation, strategic durability, economics, and downstream execution consistency.
6. [AI] Select a scoped commercial position and define where it applies; do not silently rewrite canonical Brand/business positioning if a strategic context change is required.
7. [HYBRID] Create Context Update Proposal for true business-positioning changes; otherwise store Marketing Insight/Opportunity-specific strategy.
