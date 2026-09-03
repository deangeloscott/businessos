---
id: marketing.assets.nurture
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- type: Insight
  domain: customer-intelligence
- type: Insight
  domain: competitor-intelligence
- Asset
- WorkRequest
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Lead Nurture Strategy

## Purpose
Move not-yet-ready prospects toward a better-informed decision over time rather than repeatedly asking for the sale.

## Business Outcome
Increase qualified progression through useful evidence-backed nurture matched to audience awareness, Offer, proof, acquisition context, and relationship state.

## Run When
Use when the organization needs a nurture strategy or sequence for prospects/customers who are not ready for the desired action. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. Define entry source, awareness, why the audience may not be ready based on actual evidence, likely information/experience needed, buying horizon, and useful exit criteria.
2. Build content/message progression across education, proof, comparison, objection resolution, use cases, customer outcomes, and appropriate Offers.
3. Personalize or branch only on reliable available signals; do not pretend to know motives, lifecycle state, or intent that has not been established.
4. Determine cadence from decision cycle, relationship, and value delivery rather than maximum contact frequency. Cadence here is communication design; the external system/runtime owns actual scheduling.
5. Define useful lifecycle transitions and suppression/next-action behavior where the necessary real signals exist. If later customer-progression or sales work is needed, use the relevant operating knowledge directly; create a WorkRequest only when a real durable handoff across actors/sessions/time is actually needed.
6. Measure progression to qualified intent/value where possible rather than opens or clicks alone.
7. Preserve the useful nurture Asset/strategy. If sending or automation is explicitly requested and the harness has real capability/permission, configure it through the external system; otherwise report the remaining execution state truthfully without manufacturing AURA runtime state.

## Proportionate Scope
Use only the cadence, content breadth, segmentation, branching, and measurement needed for the actual buying horizon and relationship. Expand when audience heterogeneity or decision complexity makes additional nurture materially useful; do not maximize touch count.

## Verification
- Nurture content provides real value and progression rather than repetitive pressure.
- Personalization, lifecycle assumptions, urgency, frequency, and claims stay within evidence and real constraints.
- Designed cadence/branching is not represented as active automation unless the external system actually implements it.
- AURA domains do not hand the prospect around through internal WorkRequests.

## Completion Criteria
- The organization has a usable nurture strategy/Asset at the requested fidelity, with external execution state and measurement clearly separated from the plan.
