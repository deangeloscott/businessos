---
id: competitor.analysis.capability-comparison
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Capability Comparison

## Purpose
Compare product/service capabilities in the customer context that makes them valuable.

## Business Outcome
Support competitive decisions without reducing nuanced capabilities to a misleading feature checklist.

## Run When
Run when product/service capability differences materially affect customer choice, positioning, or response.

## Process
1. [AI] Define the customer workflows/outcomes being compared and the minimum relevant capability dimensions.
2. [INTEGRATION] Collect current first-party documentation/demos/claims and dates for each capability.
3. [AI] Distinguish advertised availability, actual documented functionality, integrations/dependencies, service-delivered capability, and unknown/private details.
4. [AI] Compare fit, limits, prerequisites, effort, maturity, and outcome relevance—not just presence/absence.
5. [HYBRID] Treat unverifiable performance/quality claims as claims, not facts.
6. [AI] Cross-reference customer evidence to identify which capability differences matter in real decisions.
7. [AI] Publish scoped competitive Observations/Insights and unresolved validation needs.
