---
id: marketing.strategy.objection-handling
type: playbook
version: 1.1.0
owner_system: marketing-synthesis
risk: low
autonomy_ceiling: 4
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
- ActionPacket
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
# Objection Handling Strategy

## Purpose
Address evidence-backed buyer objections honestly without manipulative dismissal.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed objection handling strategy that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires objection handling strategy to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Load scoped Customer Objection Insights and identify true underlying uncertainty/risk behind each objection.
2. [AI] Classify response mechanism: clarify fit, provide proof, explain tradeoff, reduce risk, compare alternatives, set expectation, reframe economics, or admit non-fit.
3. [HYBRID] Match each response to evidence/Offer truth and avoid pressure tactics that contradict customer interest.
4. [AI] Determine where in the funnel/asset the objection should be preempted versus handled after it arises.
5. [AI] Draft message logic and proof requirements; include honest limitations/eligibility where relevant.
6. [HYBRID] Route persistent operational objections to Customer Optimization/Product/business owner when messaging cannot fix the underlying reality.
