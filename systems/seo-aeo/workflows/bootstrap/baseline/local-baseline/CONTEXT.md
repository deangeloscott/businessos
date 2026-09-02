---
id: seo.bootstrap.baseline.local-baseline
type: workflow
owner_system: seo-aeo
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- location/profile data, local-result observations, and local competitors
updates:
  SEOAssetState:
  - organic_performance
---
# Local Baseline

## Purpose
Establish a trustworthy starting view of local entity, profile, site, reputation, and visibility state for the locations or service areas that materially matter.

## Business Outcome
Give later local-discovery work a useful comparison point for accurate representation, visibility, customer actions, and business opportunity without turning local SEO into a universal full-profile audit.

## Run When
Use when local discovery is applicable and current local state is missing, materially stale, or needed for a concrete diagnosis, optimization, or comparison. A user/runtime may invoke re-baselining; AURA does not own recurrence.

## Process
1. [HYBRID] Confirm the real local business model and scoped locations/service areas from organization truth before interpreting profiles or results.
2. [HYBRID] Inspect relevant owned/duplicate profiles, important citations, location pages, identity fields, and factual consistency to the depth needed for the current market question.
3. [HYBRID] Gather available profile engagement, map/local visibility, website-location, ratings/reviews, citations/backlinks, calls/bookings/directions/site actions, or other useful evidence.
4. [AI] Segment by location, service, query/task, market, language, or geographic observation point only when those dimensions materially change the diagnosis.
5. [AI] Identify material strengths, gaps, or uncertainty in relevance, prominence, reputation, website support, entity consistency, eligibility, or customer usefulness.
6. [AI] Treat local visibility as an important upstream signal where stronger presence can plausibly increase customer exposure and action opportunity; connect to calls, visits, leads, revenue, or other outcomes only when those downstream observations exist.
7. [HYBRID] Preserve the baseline evidence and any severe unresolved state when future work benefits. Use an Incident only when the issue is genuinely severe enough to require durable cross-session coordination.

## Verification
- Business/location facts are grounded before public-profile conclusions are made.
- Local visibility, profile engagement, customer actions, leads, and revenue remain distinct evidence stages.
- Scope is proportionate to the actual locations and market decision.
- No capability registry, mandatory Opportunity, or internal routing lifecycle is required.
