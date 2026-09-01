---
id: marketing.webinar.script
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
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Webinar Script and Presenter Notes

## Purpose
Turn the chosen teaching/persuasion architecture into a complete deliverable presenter script or structured notes.

## Business Outcome
Enable consistent delivery of teaching, proof, Offer, and CTA without requiring the presenter to invent critical parts live.

## Run When
Use when a webinar needs a complete presenter script or structured notes. Existing teaching/persuasion architecture, Assets, or a real WorkRequest may provide context but are not required when the necessary context is otherwise available.

## Process
1. [AI] Draft opening/context/expectations, each teaching module, transitions, examples/demos, interaction prompts, persuasion overlays, Offer segment, CTA, and Q&A framing.
2. [AI] Write spoken language appropriate to presenter style and choose full-script versus bullet-note sections by the need for exact wording, consistency, and natural delivery.
3. [AI] Make instructions/examples actionable enough to deliver the educational promise.
4. [AI] Integrate proof and material business claims with their source context/qualifiers; do not enlarge established promises.
5. [HYBRID] Check timing, density, jargon, guarantee/price/urgency statements, real compliance/platform constraints, and likely audience questions.
6. [AI] Add cut points/optional material for timing variance without deleting critical teaching or Offer facts.
7. [AI] Preserve the usable script/presenter-notes Asset with slide/demo cues and evidence links when future work benefits from them. Do not create a WorkRequest merely because slide/media production may also be useful; use the current harness directly when that production is in scope, or create a WorkRequest only for a genuine durable handoff.

## Completion Criteria
- The presenter has a usable evidence-bounded script or notes that can deliver the intended teaching and persuasion coherently, with no internal AURA handoff required.
