---
id: content.production.demo-plan
type: playbook
version: 1.3.0
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
# Demonstration Plan

## Purpose
Design a demonstration that visibly proves or teaches the intended mechanism, use case, or result.

## Business Outcome
Create credible demonstrations that reduce abstraction without cherry-picking or staging misleading evidence.

## Run When
Run when showing the thing working is more useful than merely explaining or claiming it.

## Process
1. [AI] State exactly what the demo must teach/prove, for which use case, and what would count as a fair representative example.
2. [DETERMINISTIC] Resolve product/process access, sample data/materials, permissions, ProofRecords, and safety/privacy constraints.
3. [AI] Define setup, starting state, sequence of actions, expected observations, edge cases, and final state.
4. [HYBRID] Avoid hidden edits, unrealistic data, omitted prerequisites, or selection of an exceptional case presented as typical.
5. [AI] Plan capture views/annotations needed so the audience can see the causal/functional mechanism clearly.
6. [DETERMINISTIC] Define verification of the demo result and record conditions/limitations.
7. [AI] Produce the demo runbook and downstream storyboard/shot requirements.
