---
id: marketing.vsl.visual-brief
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# VSL Visual Brief

## Purpose
Specify the visual proof, demonstrations, diagrams, text, and production needs required by the VSL persuasion sequence.

## Business Outcome
Ensure the video shows evidence/mechanism instead of relying on spoken claims over generic footage.

## Run When
Run after VSL architecture/script when Content will produce the video.

## Process
1. [DETERMINISTIC] Resolve script beats, ProofRecords, product/demo Assets, brand/platform constraints, and production capabilities.
2. [AI] Identify which beats need presenter, demonstration, screenshot, case/result, diagram, comparison, text emphasis, or supporting visual.
3. [AI] Prioritize visuals that increase belief/comprehension and remove decorative B-roll with no persuasion function.
4. [HYBRID] Flag visuals that could misleadingly imply results, comparisons, or authenticity.
5. [AI] Define proof/source context that must appear on-screen and any disclaimers/qualifiers.
6. [AI] Package beat-by-beat visual requirements and delegate Content production.
7. [DETERMINISTIC] Verify produced visuals preserve the intended claim/sequence before final VSL QA.
