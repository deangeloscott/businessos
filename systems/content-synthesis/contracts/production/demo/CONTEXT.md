---
id: content.production.demo
type: playbook
version: 1.3.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 2
reads:
- Insight
- Opportunity
- WorkRequest
- ProofRecord
- Asset
- PlatformProfile
writes:
- Asset
- ActionPacket
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
# Demonstration Asset Production

## Purpose
Execute an approved demonstration plan and produce a clear, verifiable demonstration Asset.

## Business Outcome
Show a product, service, workflow, result, or mechanism working under stated conditions.

## Run When
Run after an approved demo plan and required access/materials are available.

## Process
1. [DETERMINISTIC] Verify the starting state, sample data/materials, permissions, version/configuration, and recording/generation setup.
2. [INTEGRATION] Execute/capture the planned steps or coordinate the approved human/generative execution.
3. [DETERMINISTIC] Record the actual observed result, deviations, failures/retries, and conditions rather than editing toward a predetermined result.
4. [AI] Select/annotate the clearest sequence that shows the mechanism and relevant outcome without hiding prerequisites.
5. [HYBRID] Verify that the final edit is representative, truthful, privacy-safe, and not synthetic evidence presented as real.
6. [DETERMINISTIC] Link verification evidence and create/update ProofRecord if the demo legitimately supports a reusable claim.
7. [AI] Package the demo for the intended format/platform and route derivative content if valuable.
