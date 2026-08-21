---
id: marketing.campaigns.campaign-concept
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
# Campaign Concept Development

## Purpose
Create a coherent commercial campaign concept linking audience, Insight, offer, message, creative mechanism, channels/assets, and measurable action.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed campaign concept development that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires campaign concept development to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define business Objective, audience, Offer, primary Insight/tension, desired action, timing, and constraints.
2. [AI] Generate distinct campaign territories with core promise, angle, creative mechanism, proof, CTA, and why now.
3. [HYBRID] Evaluate concepts against customer relevance, competitive distinctiveness, brand fit, evidence, fatigue risk, production feasibility, and channel context.
4. [AI] Select concept and define message hierarchy, creative system, asset roles, and journey continuity.
5. [HYBRID] Identify which production tasks belong to Content Synthesis and which media buying/execution lies outside Marketing Synthesis.
6. [DETERMINISTIC] Define success/guardrail metrics and experiment structure before production.
