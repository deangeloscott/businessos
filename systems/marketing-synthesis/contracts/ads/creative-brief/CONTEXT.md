---
id: marketing.ads.creative-brief
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
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
# Advertising Creative Brief

## Purpose
Specify the visual/audio demonstration required to express an approved ad angle in the placement.

## Business Outcome
Enable strong native creative without forcing a separate internal domain to reconstruct the commercial persuasion strategy.

## Run When
Use when an ad angle needs clear visual/audio production requirements; media buying/targeting execution remains outside this method unless separately available and requested.

## Process
1. [HYBRID] Resolve angle, copy, audience, Offer, ProofRecords, destination, and placement/platform requirements.
2. [AI] Define the first-frame/attention mechanism, demonstration/story/visual proof, key message beats, required on-screen text, and CTA.
3. [AI] Identify what should be shown rather than claimed and which real Proof/Asset must be used.
4. [HYBRID] Prevent misleading synthetic testimonials/results, visual bait, or creative that targets an irrelevant audience.
5. [AI] Define format/duration/variant requirements and what is fixed versus open to creative execution.
6. [HYBRID] Preserve the useful creative brief as an Asset and use relevant Content operating knowledge plus the active harness's real generation/rendering capabilities directly when available. Persist a WorkRequest only for a real durable organizational handoff to a separate executor.
7. [HYBRID] Verify produced creative against angle, claims, and destination before activation when the media is available.
