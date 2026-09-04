---
id: marketing.vsl.qa
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# VSL Persuasion QA

## Purpose
Review the actual VSL as consumed—not only the script—for persuasion integrity, evidence, pacing, and action accuracy.

## Business Outcome
Catch material edits, visuals, claims, delivery choices, or technical defects that weaken or misrepresent the intended persuasion system.

## Run When
Use on a substantive VSL draft/render or live implementation when end-to-end QA can materially improve readiness or identify defects.

## Process
1. [HYBRID] Inspect the actual available render against the intended script/architecture, current Offer, supporting evidence, and destination. If only a script/partial render exists, constrain QA to what was actually inspected.
2. [AI] Evaluate hook payoff, belief sequence, clarity, proof timing, objection handling, Offer transition, pacing, and CTA understanding.
3. [HYBRID] Check material spoken/on-screen claims, captions, testimonial context, demos, urgency, price/terms, and visual implications against current organizational truth/evidence.
4. [AI] Identify repetition, pacing, confusion, or production choices that could cause qualified drop-off without shortening for its own sake.
5. [HYBRID] Verify player/link/CTA/tracking and downstream message match where the available artifact and host capabilities permit it.
6. [AI] Report material defects, lower-severity improvements, and the evidence/check behind each conclusion. A material defect may justify recommending against release of that version, but AURA does not authorize or block publication.
7. [HYBRID] If publication/deployment is explicitly requested and actually performed through the host, verify the live version/measurement state when practical. Otherwise keep deployment and outcome unknown/separate.
8. [AI] Preserve useful QA/readiness meaning on or alongside the Asset when future work benefits from it. Do not create a WorkRequest, Run record, or generic verification lifecycle merely because QA occurred.

## Completion Criteria
- The inspected VSL version has a clear evidence-backed QA result with material limitations explicit, and no internal AURA handoff or permission gate is required.
