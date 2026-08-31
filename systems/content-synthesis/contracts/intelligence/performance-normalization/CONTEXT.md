---
id: content.intelligence.performance-normalization
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
# Content Performance Normalization

## Purpose
Normalize observed content performance so unusually large distribution or creator baseline does not masquerade as creative effectiveness.

## Business Outcome
Improve creative learning by comparing content in the context of its normal reach, format, audience, and distribution.

## Run When
Run before declaring an observed piece/pattern a strong performer or using it to justify a Content Learning.

## Process
1. [DETERMINISTIC] Collect available views/impressions/reach, engagement/watch/completion/save/share/click signals, account/creator baseline, post age, format, audience size, and known paid/support distribution.
2. [DETERMINISTIC] Compare performance with the creator/account’s own recent comparable content and platform/format norms where reliable.
3. [AI] Identify confounders such as paid promotion, collaboration, news event, giveaway, celebrity, unusually large distribution, timing, or existing audience affinity.
4. [AI] Separate reach success from retention, response, conversion, and value signals.
5. [HYBRID] Avoid precision normalization when the denominator/context is unknown; lower confidence instead.
6. [AI] Determine whether the creative mechanism remains notable after contextual factors.
7. [DETERMINISTIC] Attach normalized observations/confounders to pattern validation and future Learning.
