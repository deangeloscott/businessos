---
id: marketing.campaigns.campaign-concept
type: playbook
version: 1.2.0
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
- PreferenceProfile
---
# Campaign Concept Development

## Purpose
Create a coherent commercial campaign concept linking audience, decision context, Insight, Offer, message, creative mechanism, channels/assets, and measurable action.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed campaign concepts that match audience awareness, funnel/journey role, motivation, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires campaign concept development to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define business Objective, audience, awareness/knowledge state, funnel/journey role, Offer, primary Insight/tension, desired action, acquisition/placement context, timing, constraints, proof, and evidence-backed motivations/objections.
2. [AI] When creative uncertainty would benefit from choice, generate up to three genuinely distinct campaign territories. Vary meaningful strategic dimensions such as gain versus loss framing, certainty/control versus aspiration/status, problem versus desired-outcome lead, mechanism, proof system, structure, or visual treatment—not synonyms or cosmetic rewrites. Use fewer when one route is clearly sufficient.
3. [HYBRID] Evaluate concepts against customer relevance, applicable motivation evidence, competitive/current-field distinctiveness, Brand/operator doctrine, factual support, funnel/message continuity, fatigue risk, production feasibility, and channel context.
4. [AI] Recommend/select the strongest supported concept while preserving legitimate user choice; explain the evidence/mechanism behind the recommendation rather than treating taste as certainty.
5. [AI] Define message hierarchy, creative system, asset roles, and journey continuity. Specify what each asset is doing (for example attention, education/trust, evaluation, conversion, retention/advocacy) rather than assuming the platform or format determines funnel role.
6. [HYBRID] Identify which production tasks belong to Content Synthesis and which media buying/execution lies outside Marketing Synthesis.
7. [DETERMINISTIC] Define success/guardrail metrics and experiment structure before production. Preserve downstream quality/business outcomes so a stronger top-line proxy does not automatically become a winning campaign.
