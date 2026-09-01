---
id: content.intake.content-brief
type: playbook
owner_system: content-synthesis
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - creative.avatar_video.generate
  - video.render
  - presentation.render
  - document.render
  - social.content.publish
  - social.content.schedule
  - cms.page.publish
  - email.content.publish
context:
- Brand
- AudienceSegment
- Objective
- Offer
---
# Content Brief

## Purpose
Convert an Opportunity, WorkRequest, or Insight into a precise communication brief before creative production.

## Business Outcome
Give production a complete definition of audience, purpose, message, evidence, platform, constraints, and success without rediscovering strategy.

## Run When
Run before material content production unless an equivalent approved brief is already present.

## Process
1. [DETERMINISTIC] Resolve the originating Opportunity/WorkRequest, audience, objective, platform context, fixed requirements, relevant Insights, ProofRecords, and existing Assets.
2. [AI] State the communication job: what the audience should understand, feel, remember, or do after consuming the content.
3. [AI] Define the audience starting state, context of consumption, core message, supporting points, evidence/proof, desired action, and exclusions.
4. [AI] Separate fixed constraints from creative choices and identify claims requiring factual verification.
5. [HYBRID] Resolve conflicts between Brand, platform behavior, upstream requirements, and available evidence before drafting.
6. [DETERMINISTIC] Define required deliverables/variants, format constraints, QA gates, publication destination if known, and measurement objective.
7. [AI] Produce a concise brief that references canonical intelligence instead of copying large source material.
