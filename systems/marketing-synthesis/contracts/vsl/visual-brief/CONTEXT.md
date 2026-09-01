---
id: marketing.vsl.visual-brief
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
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
Use after VSL architecture/script when visual production requirements are useful.

## Process
1. [HYBRID] Resolve script beats, ProofRecords, product/demo Assets, brand/platform constraints, and the active harness's real production capabilities.
2. [AI] Identify which beats need presenter, demonstration, screenshot, case/result, diagram, comparison, text emphasis, or supporting visual.
3. [AI] Prioritize visuals that increase belief/comprehension and remove decorative B-roll with no persuasion function.
4. [HYBRID] Flag visuals that could misleadingly imply results, comparisons, or authenticity.
5. [AI] Define proof/source context that must appear on-screen and any disclaimers/qualifiers.
6. [HYBRID] Package beat-by-beat visual requirements as an Asset/brief and use relevant Content operating knowledge plus real rendering/generation capabilities directly when the model/harness can produce the media. Persist a WorkRequest only for a real durable organizational handoff.
7. [HYBRID] Verify produced visuals preserve the intended claim/sequence before final VSL QA when the produced media is available.
