---
id: content.strategy.audience-context
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
# Content Audience and Consumption Context

## Purpose
Define who is consuming the content, what state they are in, and how the platform/medium changes what will work.

## Business Outcome
Ensure content is designed for the actual audience and consumption environment rather than generic repurposing.

## Run When
Run when the audience, platform context, or consumption state is not already explicit in the content brief.

## Process
1. [DETERMINISTIC] Resolve the target AudienceSegment and relevant Customer Insights, platform profile, acquisition/context signals, and prior performance.
2. [AI] State what the audience already knows, cares about, misunderstands, resists, and is trying to accomplish in this moment.
3. [AI] Identify likely attention state, device/context, expected depth, interaction behavior, and time/effort tolerance for the platform/medium.
4. [AI] Determine what context must be supplied inside the asset versus what can be assumed.
5. [HYBRID] Reconcile audience needs with platform-native behavior without sacrificing factual accuracy or brand standards.
6. [AI] Identify segment/context variations that justify different versions instead of one compromised asset.
7. [DETERMINISTIC] Record the audience/context decisions in the content brief/ActionPacket.
