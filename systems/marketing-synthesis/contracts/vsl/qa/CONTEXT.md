---
id: marketing.vsl.qa
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 2
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- ActionPacket
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
# VSL Persuasion QA

## Purpose
Review the final VSL as consumed—not only the script—for persuasion integrity, evidence, pacing, and action accuracy.

## Business Outcome
Catch edits, visuals, claims, or delivery choices that break the approved persuasion mechanism.

## Run When
Run before VSL launch/publication and after material edits.

## Process
1. [DETERMINISTIC] Review the final render with approved script/architecture, Offer version, ProofRecords, and destination.
2. [AI] Evaluate hook payoff, belief sequence, clarity, proof timing, objection handling, Offer transition, and CTA understanding.
3. [HYBRID] Check rendered claims, captions/on-screen text, testimonial context, demos, urgency, price/terms, and visual implications.
4. [AI] Identify pacing/repetition/confusion that can cause qualified drop-off without shortening for its own sake.
5. [DETERMINISTIC] Verify links/player/CTA/tracking and downstream page message match.
6. [DETERMINISTIC] Block release on material claim/Offer/destination errors and record QA result.
7. [DETERMINISTIC] After launch verify live version and measurement baseline.
