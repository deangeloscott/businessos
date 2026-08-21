---
id: competitor.analysis.advertising
type: playbook
version: 1.7.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 4
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
  - browser.interact
events:
  consumes:
  - none
  emits:
  - competitor.insight.updated
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
references:
- systems/competitor-intelligence/references/source-coverage.json
---
# Advertising Intelligence

## Purpose
Observe competitor paid creative/message patterns, destinations, and persistence across relevant public advertising surfaces without equating visibility with profitability.

## Business Outcome
Improve competitive decisions through evidence-backed advertising intelligence while avoiding false claims about effectiveness.

## Run When
Run when a decision requires current competitor advertising intelligence and canonical evidence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [AI] Determine which advertising surfaces are relevant to this competitor, market, audience, and question. Consider current public transparency/ad libraries (for example Meta Ad Library, Google Ads Transparency Center, LinkedIn Ad Library, TikTok Commercial Content Library) plus additional credible sources the agent discovers; do not treat the examples as a mandatory or exhaustive list.
2. [INTEGRATION] Retrieve available public observations with platform/source, resolved advertiser identity, creative, copy, CTA, landing destination, first/last seen, geography/targeting/reach or other metadata when actually exposed. Record regional/data limitations.
3. [DETERMINISTIC] Deduplicate creative variants and group by concept/campaign/theme while preserving source IDs/URLs and time ranges.
4. [AI] Extract audience hypothesis, hook, problem/outcome, offer, proof, CTA, format, creative mechanism, and recurring message/offer patterns.
5. [HYBRID] Use duration, repetition, variation, visible reach, or platform prominence as weak signals only; explicitly separate persistence/visibility from proven effectiveness and consider competing explanations such as budget, brand size, timing, or targeting.
6. [HYBRID] When a material ad leads to a relevant public acquisition path, route/deepen through Funnel Capture rather than analyzing the creative in isolation.
7. [AI] Compare advertising themes with competitor positioning, offers, customer criteria, and observed outcomes; create testable competitive hypotheses rather than copying creative.
8. [DETERMINISTIC] Publish Observations/Insights, record source coverage/gaps, and route persuasion implications to Marketing when installed.

## Verification
Advertising conclusions identify the actual public sources and limitations, resolve the advertiser to the correct competitor, preserve landing destinations, and never label a visible ad a winner without supporting effectiveness evidence.
