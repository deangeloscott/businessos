---
id: competitor.analysis.advertising
type: playbook
version: 1.9.0
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
  - webpage.screenshot
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
  - browser.interact
  - media.video.acquire
  - media.transcript.acquire
  - media.metadata.inspect
  - media.video.process
  - media.audio.extract
  - media.frame.extract
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
Observe competitor paid creative/message patterns, destinations, persistence, and multimodal execution across relevant public advertising surfaces without equating visibility with profitability.

## Business Outcome
Improve competitive and downstream marketing decisions through evidence-backed advertising intelligence while avoiding false claims about effectiveness or copying competitor expression.

## Run When
Run when a decision requires current competitor advertising intelligence and canonical evidence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [AI] Determine which advertising surfaces are relevant to this competitor, market, audience, and question. Consider current public transparency/ad libraries (for example Meta Ad Library, Google Ads Transparency Center, LinkedIn Ad Library, TikTok Commercial Content Library) plus additional credible sources the agent discovers; do not treat the examples as a mandatory or exhaustive list.
2. [INTEGRATION] Retrieve available public observations with platform/source, resolved advertiser identity, creative, copy, CTA, landing destination, first/last seen, geography/targeting/reach or other metadata when actually exposed. Record regional/data limitations. When a material public video/audio creative cannot be acquired through the native host, inspect trusted optional local media capabilities before settling for a weaker fallback; system tool installation/update/repair remains separately authorized.
3. [HYBRID] Inspect the actual creative modalities that materially carry the ad mechanism. For image/carousel creative, inspect composition, hierarchy, product/demo/proof devices and frames; for video/audio, inspect the relevant visual/audio segments, spoken content/transcript, pacing, demonstration, on-screen text, proof and CTA when the available capability permits it. Acquisition/frame/audio/transcode tools provide mechanics, not semantic understanding. If only transcript/copy/thumbnail metadata is available, record that limitation and do not claim unobserved visual/audio mechanisms.
4. [DETERMINISTIC] Preserve support-grade evidence according to Core research-evidence policy, deduplicate creative variants, and group by concept/campaign/theme while retaining source IDs/URLs, time ranges, and relevant frame/timestamp/page context.
5. [AI] Extract audience hypothesis, awareness/funnel role, hook, problem/outcome, evidence-backed motivation hypothesis, offer, proof, CTA, format, visual/audio creative mechanism, and recurring message/offer patterns.
6. [HYBRID] Use duration, repetition, variation, visible reach, or platform prominence as weak/calibrated signals only; explicitly separate persistence/visibility from proven effectiveness and consider competing explanations such as budget, brand size, timing, targeting, or platform delivery.
7. [HYBRID] When a material ad leads to a relevant public acquisition path, route/deepen through Funnel Capture rather than analyzing the creative in isolation.
8. [AI] Compare advertising themes with competitor positioning, offers, customer criteria, and observed outcomes; create testable competitive hypotheses and transferable mechanisms rather than copying creative.
9. [DETERMINISTIC] Publish Observations/Insights, record source coverage/gaps and modality limitations, and route persuasion implications to Marketing when installed.

## Verification
Advertising conclusions identify the actual public sources and limitations, resolve the advertiser to the correct competitor, preserve landing destinations and material media evidence, and never label a visible ad a winner without supporting effectiveness evidence.
