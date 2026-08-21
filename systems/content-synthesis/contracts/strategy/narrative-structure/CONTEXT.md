---
id: content.strategy.narrative-structure
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
# Content Narrative Structure

## Purpose
Sequence ideas, evidence, examples, and payoff so the audience can follow and retain the message.

## Business Outcome
Improve comprehension and engagement by making each section earn the next rather than listing information.

## Run When
Run for content whose structure is not trivial or already prescribed by another domain contract.

## Process
1. [AI] Identify audience starting state, core message, required supporting ideas, evidence, examples, objections/confusion, and desired ending state.
2. [AI] Choose a structure appropriate to the communication job: problem→mechanism→solution, demonstration→explanation, story→lesson, question→evidence→answer, sequence/tutorial, comparison, or another justified form.
3. [AI] Define the job of each beat/section and the transition that makes the next beat necessary.
4. [AI] Place evidence/examples where they resolve the specific doubt or abstraction they support rather than collecting proof at the end.
5. [HYBRID] Remove tangents, repeated setup, premature detail, and unsupported dramatic claims.
6. [AI] Match pacing/depth to format/platform and identify where visual/audio demonstration should replace exposition.
7. [DETERMINISTIC] Produce an ordered structure/outline ready for production.
