---
id: seo.intelligence.organic-demand.business-value-mapping
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- Observation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- Market search answer evidence
- location/profile data, local-result observations, and local competitors
- records topic intent evidence
updates:
  OrganicDemandUnit:
  - business_value
  - demand_evidence
---
# Demand Business-Value Mapping

## Purpose
Connect every pursued demand unit to a plausible business-value pathway.

## Business Outcome
Improve valuable organic discovery through demand business-value mapping, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run during initial or recurring demand research when the system must discover, classify, or update **demand business-value mapping** evidence.

## Process
1. [AI] Map the demand unit to audience, awareness/buying stage, problem/goal, relevant offer, and desired next action.
2. [DETERMINISTIC] Join observed conversion/revenue data for current traffic when available.
3. [HYBRID] Estimate relative business relevance and value using offer economics, lead quality, customer fit, market priority, and conversion proximity; label assumptions.
4. [AI] Identify supporting/assisted content where direct conversion is unlikely but the asset can legitimately move users to the next stage.
5. [HYBRID] Reject or downweight high-volume demand with weak/unsupported business pathways.
6. [AI] Write an interpretable value rationale used by the Opportunity Engine rather than a black-box score.

## Decisions / Routing
- Route → Competitor Intelligence refresh only when canonical competitor intelligence is missing or stale.
- Route → Core Opportunity qualification when an SEO intervention is evidence-supported.

## Verification
- Verify location eligibility and business facts before changing public profile/location data.


