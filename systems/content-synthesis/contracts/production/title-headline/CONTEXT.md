---
id: content.production.title-headline
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
# Content Title and Headline

## Purpose
Create a truthful, platform-appropriate title/headline that accurately signals the content’s value to the intended audience.

## Business Outcome
Improve qualified attention and expectation match without clickbait or generic labeling.

## Run When
Run when the format/platform uses a title, headline, subject-like label, or prominent first-frame text.

## Process
1. [AI] Identify the strongest true value/tension/specificity from the core message and audience context.
2. [AI] Generate materially different headline mechanisms: outcome, problem, demonstration, specificity, comparison, question, contrarian insight, or consequence as appropriate.
3. [HYBRID] Reject headlines that overpromise, remove material qualifiers, imply unsupported certainty, or attract the wrong audience.
4. [AI] Match length, syntax, and information density to the platform/profile and thumbnail/visual relationship.
5. [AI] Avoid duplicating the hook if title + first frame work better as complementary information.
6. [DETERMINISTIC] Check known content learnings/experiments and select candidates for test when stakes/volume justify it.
7. [AI] Output primary and limited alternate titles with the mechanism/rationale.
