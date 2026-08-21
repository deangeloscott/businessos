---
id: marketing.strategy.messaging
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
# Messaging Architecture

## Purpose
Define what the audience needs to understand/believe in what order across a commercial experience.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed messaging architecture that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires messaging architecture to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define audience, awareness, stage, desired action, Offer, positioning, objections, decision criteria, and proof.
2. [AI] Build message hierarchy: primary promise/outcome, problem framing, mechanism/differentiation, proof, objections/risk, offer/value, CTA.
3. [HYBRID] Map each message to customer evidence and available proof rather than writing claims first.
4. [AI] Adapt emphasis and sophistication to audience/stage without creating contradictory claims across channels.
5. [HYBRID] Define required message continuity from acquisition source to destination and follow-up.
6. [AI] Produce a reusable messaging architecture and asset-specific priorities, not merely a list of slogans.
