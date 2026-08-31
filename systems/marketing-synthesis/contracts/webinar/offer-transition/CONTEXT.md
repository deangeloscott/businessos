---
id: marketing.webinar.offer-transition
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Webinar Offer Transition

## Purpose
Design the transition from teaching into the commercial Offer so it follows logically from what attendees just learned.

## Business Outcome
Avoid abrupt “now for the pitch” transitions while making the commercial decision explicit.

## Run When
Run when a sales-oriented webinar reaches the point where the Offer should be presented.

## Process
1. [AI] Summarize the problem/mechanism/framework attendees now understand and the gap between knowing it and implementing/achieving it.
2. [AI] Introduce the Offer as one appropriate way to close that gap, not as the only conceivable solution.
3. [AI] Define fit/disqualification, scope, process, outcomes, proof, terms, risk reversal, and why now where genuine.
4. [DETERMINISTIC] Validate all price/terms/guarantee/availability facts against the current Offer.
5. [AI] Address the highest remaining objections and explain the exact next step after CTA.
6. [HYBRID] Remove artificial value stacks, unsupported outcome certainty, or pressure inconsistent with the evidence.
7. [DETERMINISTIC] Produce the Offer/CTA beat sequence for script/slides.
