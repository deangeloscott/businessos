---
id: seo.diagnosis.local-gap
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- location/profile data, local-result observations, and local competitors
---
# Local Visibility Gap

## Purpose
Identify material local discovery or conversion gaps by location, service, query, profile, reputation, or local competitive context and distinguish controllable causes from geography or other constraints.

## Business Outcome
Focus local SEO/AEO effort on gaps that can realistically improve customer/business outcomes rather than treating every visibility difference as an optimization problem.

## Run When
Use when current local-result, profile, reputation, location-page, or conversion evidence can help explain an important local discovery gap.

## Process
1. [HYBRID] Define the actual local market from established business location/service-area truth, realistic customer behavior, query intent, and the observed result environment. Do not impose an arbitrary radius when the business or query works differently.
2. [HYBRID] Relate local query/map observations, profiles, location pages, reviews, citations/links, customer actions/conversions, and relevant local competitors at the depth needed for the decision.
3. [AI] Identify the observed gap: absent/weak high-value query coverage, incomplete/incorrect profile, weak or missing location page, reputation/review disadvantage, inconsistent identity, competitor prominence, or another evidenced condition.
4. [HYBRID] Separate uncontrollable or weakly controllable proximity/distance effects from controllable relevance, prominence, profile, reputation, entity consistency, asset, and conversion-path factors.
5. [AI] Define a specific intervention hypothesis only where the mechanism appears controllable and materially valuable. Avoid generic “improve local SEO” work or copying a competitor whose prominence comes from a different geography/business model.
6. [AI] Preserve an Opportunity only when expected local customer/business value, realistic service/location capacity, and evidence justify attention. Do not fabricate uplift from improved visibility.
7. [HYBRID] Evaluate later results with the strongest trustworthy local business signals available—such as calls, bookings, directions, leads, visits, or site conversions—with visibility and rank as supporting evidence rather than the sole outcome.

## Verification
- Location eligibility, services, hours, addresses, and other public business facts are established before public changes.
- Local visibility difference alone does not prove a controllable opportunity.
- Competitors/benchmarks are geographically and commercially relevant to the question; broader benchmarks are used only when they serve a distinct useful purpose.
