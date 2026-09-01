---
id: marketing.webinar.slide-brief
type: playbook
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
# Webinar Slide Brief

## Purpose
Define what each webinar slide/visual must communicate so Content can produce the presentation without reconstructing persuasion strategy.

## Business Outcome
Create slides that support teaching, demonstration, proof, and Offer rather than becoming a transcript on screen.

## Run When
Run after webinar architecture/script when presentation production is required.

## Process
1. [DETERMINISTIC] Resolve final beat/script sequence, proof/demo assets, Brand, and presentation constraints.
2. [AI] Assign each slide one job and specify key message, visual/diagram/data/proof, minimal on-screen text, and speaker relationship.
3. [AI] Identify where no slide, live demo, whiteboard, screen share, or other medium is more effective.
4. [HYBRID] Check data/claim context, testimonial permissions, pricing/Offer accuracy, and accessibility.
5. [AI] Define consistent visual logic for framework steps, examples, comparisons, and Offer section.
6. [AI] Create Content WorkRequest for final slide production with reusable source Assets.
7. [DETERMINISTIC] Verify final deck against slide brief and current Offer/claims.
