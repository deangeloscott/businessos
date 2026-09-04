---
id: marketing.campaigns.campaign-concept
type: workflow
owner_system: marketing-synthesis
reads:
- type: Insight
  domain: customer-intelligence
- type: Insight
  domain: competitor-intelligence
- Asset
- MetricObservation
writes:
- Asset
context:
- AudienceSegment
- Brand
- Objective
- Offer
- PreferenceProfile
---
# Campaign Concept Development

## Purpose
Create a coherent commercial campaign concept linking audience, decision context, evidence, Offer, message, creative mechanism, channels/assets, and measurable action.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed campaign concept that matches audience awareness, funnel/journey role, motivation, proof, and acquisition context.

## Run When
Use when the organization needs a coherent campaign concept or materially different campaign direction. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define business Objective, audience, awareness/knowledge state, funnel/journey role, Offer, primary evidence/tension, desired action, acquisition/placement context, timing, constraints, proof, and evidence-backed motivations/objections.
2. [AI] When creative uncertainty would benefit from choice, generate up to three genuinely distinct campaign territories. Vary meaningful strategic dimensions such as gain versus loss framing, certainty/control versus aspiration/status, problem versus desired-outcome lead, mechanism, proof system, structure, or visual treatment—not synonyms or cosmetic rewrites. Use fewer when one route is clearly sufficient.
3. [HYBRID] Evaluate concepts against customer relevance, applicable motivation evidence, competitive/current-field distinctiveness, Brand/operator doctrine, factual support, funnel/message continuity, fatigue risk, production feasibility, and channel context.
4. [AI] Recommend/select the strongest supported concept while preserving legitimate user choice; explain the evidence/mechanism behind the recommendation rather than treating taste as certainty.
5. [AI] Define message hierarchy, creative system, asset roles, and journey continuity. Specify what each asset is doing (for example attention, education/trust, evaluation, conversion, retention/advocacy) rather than assuming the platform or format determines funnel role.
6. [HYBRID] Use relevant Content operating knowledge and the active harness's production capabilities directly for downstream assets when the user wants them. Media buying/external execution remains with the real host/provider surfaces; persist a WorkRequest only for a real durable organizational handoff.
7. [HYBRID] Define useful success/guardrail metrics and an experiment structure only when measurement/testing materially improves the decision. Preserve the selected concept as an organization-owned strategy Asset; do not manufacture Insight, Opportunity, or WorkRequest objects merely because campaign strategy was developed.
