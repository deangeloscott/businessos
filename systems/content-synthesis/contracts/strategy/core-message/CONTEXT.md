---
id: content.strategy.core-message
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
# Content Core Message

## Purpose
Distill the source intelligence into the single central idea the audience should retain.

## Business Outcome
Prevent content from becoming a collection of facts without a clear takeaway.

## Run When
Run when source material contains multiple possible ideas or the communication takeaway is not yet explicit.

## Process
1. [AI] Review the originating Insight/Opportunity and separate the essential conclusion from supporting evidence/background.
2. [AI] State the audience-relevant core message in one plain sentence without headline theatrics.
3. [AI] Identify the minimum supporting ideas required for the message to be understood and believed.
4. [AI] Remove adjacent ideas that belong in separate content unless they are necessary context.
5. [HYBRID] Check that the message is supported by sources/proof and does not overstate causal or factual certainty.
6. [AI] Adapt wording to the audience’s language/awareness while preserving meaning.
7. [DETERMINISTIC] Record the approved core message and source refs for downstream structure/production.
