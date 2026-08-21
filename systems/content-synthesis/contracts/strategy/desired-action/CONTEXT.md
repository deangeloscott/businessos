---
id: content.strategy.desired-action
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
# Content Desired Action

## Purpose
Define the appropriate next behavior or takeaway for content based on its communication objective.

## Business Outcome
Ensure content has a purposeful ending without forcing every asset into a sales CTA.

## Run When
Run when the content brief does not specify what should happen after consumption.

## Process
1. [AI] Identify the primary objective: understand, remember, discuss, save, share, subscribe, explore, respond, apply, or take a commercial step.
2. [AI] Determine what action is proportionate to audience awareness, trust, platform context, and content value delivered.
3. [AI] Separate primary action from optional secondary actions; avoid multiple competing CTAs.
4. [HYBRID] Route commercial persuasion design to Marketing when the action requires substantial offer/objection/proof architecture.
5. [AI] Design the ending/payoff so the action follows naturally from the content rather than being appended abruptly.
6. [DETERMINISTIC] Specify measurable action/event where instrumentation is available.
7. [AI] Record the selected action and any required WorkRequest to another system.
