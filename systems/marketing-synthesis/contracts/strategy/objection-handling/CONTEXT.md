---
id: marketing.strategy.objection-handling
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
# Objection Handling Strategy

## Purpose
Address evidence-backed buyer objections honestly without manipulative dismissal.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed objection handling that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when material buyer objections need a reusable response strategy. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Load scoped Customer objection evidence and identify the true underlying uncertainty/risk behind each objection.
2. [AI] Classify response mechanism: clarify fit, provide proof, explain tradeoff, reduce risk, compare alternatives, set expectation, reframe economics, or admit non-fit.
3. [HYBRID] Match each response to evidence/Offer truth and avoid pressure tactics that contradict customer interest.
4. [AI] Determine where in the funnel/asset the objection should be preempted versus handled after it arises.
5. [AI] Draft message logic and proof requirements; include honest limitations/eligibility where relevant.
6. [HYBRID] When an objection is caused by actual product, journey, service, price, or operational reality, use the relevant organizational evidence and operating knowledge directly to address the underlying problem rather than routing it through an internal AURA owner.
7. [AI] Preserve the reusable objection-response strategy as a Marketing-owned Asset. Create a separate Opportunity, WorkRequest, or canonical change only when that distinct organizational meaning actually exists.
