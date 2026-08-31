---
id: marketing.ads.creative-brief
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
# Advertising Creative Brief

## Purpose
Specify the visual/audio demonstration required to express an approved ad angle in the placement.

## Business Outcome
Let Content produce native creative without reconstructing commercial persuasion strategy.

## Run When
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [DETERMINISTIC] Resolve angle, copy, audience, Offer, ProofRecords, destination, and placement/platform specs.
2. [AI] Define the first-frame/attention mechanism, demonstration/story/visual proof, key message beats, required on-screen text, and CTA.
3. [AI] Identify what should be shown rather than claimed and which real Proof/Asset must be used.
4. [HYBRID] Prevent misleading synthetic testimonials/results, visual bait, or creative that targets an irrelevant audience.
5. [AI] Define format/duration/variant requirements and what is fixed versus open to Content creativity.
6. [AI] Create Content WorkRequest with exact persuasion/evidence constraints.
7. [DETERMINISTIC] Verify returned creative against angle/claim/destination before activation.
