---
id: content.strategy.audience-context
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
# Content Audience and Consumption Context

## Purpose
Define who is consuming the content, what state they are in, what the asset needs to accomplish, and how the platform/medium changes what will work.

## Business Outcome
Ensure content is designed for the actual audience, awareness/journey state, communication job, and consumption environment rather than generic repurposing.

## Run When
Run when the audience, platform context, awareness/journey role, or consumption state is not already explicit in the content brief.

## Process
1. [DETERMINISTIC] Resolve the target AudienceSegment and relevant Customer Insights, platform profile, acquisition/context signals, originating Opportunity/WorkRequest, and prior performance.
2. [AI] State what the audience already knows, cares about, misunderstands, resists, and is trying to accomplish in this moment. Distinguish awareness/knowledge state from funnel/journey role rather than assuming they are identical.
3. [AI] Define the asset's communication job and next appropriate action: for example earn attention/discovery, deepen problem/solution understanding, build trust/proof, support evaluation, or enable conversion/retention/advocacy.
4. [AI] Identify evidence-backed motivations/risks that matter in this context (for example gain, loss avoidance, certainty, control, effort, speed, status/identity) without forcing a framework or treating a hypothesis as customer truth.
5. [AI] Identify likely attention state, device/context, expected depth, interaction behavior, and time/effort tolerance for the platform/medium.
6. [AI] Determine what context must be supplied inside the asset versus what can be assumed, and how hook/depth/proof/CTA should change with the communication job.
7. [HYBRID] Reconcile audience needs with platform-native behavior without sacrificing factual accuracy, evidence, or brand standards.
8. [AI] Identify segment/context variations that justify genuinely different versions instead of one compromised asset.
9. [DETERMINISTIC] Record the audience/context decisions in the content brief/ActionPacket.
