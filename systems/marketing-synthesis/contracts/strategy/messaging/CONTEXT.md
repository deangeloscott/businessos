---
id: marketing.strategy.messaging
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
- PreferenceProfile
---
# Messaging Architecture

## Purpose
Define what the audience needs to notice, understand, believe, and do in what order across a commercial experience.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed messaging architecture that matches audience awareness, funnel/journey role, motivation, Offer, proof, and acquisition/placement context.

## Run When
Use when a commercial experience needs a reusable messaging architecture or material message correction. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define audience, awareness/knowledge state, funnel/journey role, acquisition source/placement, desired next action, Offer, positioning, objections, decision criteria, proof/risk needs, and applicable Brand/operator doctrine. Keep awareness and funnel role distinct rather than mapping them mechanically.
2. [AI] Resolve evidence-backed decision/motivation mechanisms that may matter in this context (for example desired gain, loss avoidance, certainty, control, speed, simplicity/effort, financial outcome, status/identity, autonomy, belonging, or convenience). Treat unsupported mechanisms as hypotheses, not customer truth.
3. [AI] Build message hierarchy appropriate to the communication job: primary idea/outcome, problem or opportunity framing, mechanism/differentiation, proof, objections/risk, Offer/value, and next action. Do not force product detail or a high-commitment CTA before the audience/context justifies it.
4. [HYBRID] Map material messages to customer evidence, approved business claims, Offer reality, and available proof rather than writing persuasive claims first.
5. [AI] Adapt emphasis, sophistication, proof density, friction, and CTA to audience/stage/context without creating contradictory claims across channels. The same format may legitimately have TOF attention, MOF education/trust, or BOF conversion versions.
6. [HYBRID] Apply organization/user marketing preferences only inside the truth/authorization boundary. A preferred framework may shape analysis; it cannot create a guarantee, scarcity, urgency, testimonial, price, capability, or customer motive.
7. [HYBRID] Define required message continuity from acquisition source/creative to destination and follow-up so the promise, proof, audience expectation, and CTA remain coherent.
8. [AI] Preserve the reusable messaging architecture and asset-specific priorities as a Marketing-owned strategy Asset when future work benefits from it. Create a separate Opportunity, WorkRequest, or canonical context change only when that distinct meaning actually exists.
