---
id: content.qa.platform
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
# Platform-Native QA

## Purpose
Verify that the final Asset actually conforms to the intended platform’s consumption behavior and technical constraints.

## Business Outcome
Prevent “platform adaptation” from being a superficial resize or repost.

## Run When
Run before publication of a platform-specific Asset or after a meaningful PlatformProfile change.

## Process
1. [DETERMINISTIC] Resolve final Asset, target PlatformProfile, brief, and required technical specs.
2. [AI] Evaluate opening/attention pattern, pacing, information density, visual framing, interaction/CTA, depth, and native format grammar.
3. [DETERMINISTIC] Check aspect/size/duration/file/caption/link/metadata/safe-area/technical constraints that can be validated exactly.
4. [AI] Identify signs the asset was merely repurposed without adapting the idea to the platform context.
5. [HYBRID] Ensure platform optimization did not compromise accuracy, brand, accessibility, or audience value.
6. [AI] Recommend the smallest revisions required for native fit; do not chase every transient convention.
7. [DETERMINISTIC] Mark QA pass/fail and the PlatformProfile version used.
