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
# Webinar Script and Presenter Notes

## Purpose
Turn the approved teaching/persuasion architecture into a complete deliverable presenter script or structured notes.

## Business Outcome
Enable consistent delivery of teaching, proof, Offer, and CTA without the presenter inventing critical parts live.

## Run When
Run after webinar teaching/persuasion/Offer architecture is approved.

## Process
1. [AI] Draft opening/context/expectations, each teaching module, transitions, examples/demos, interaction prompts, persuasion overlays, Offer segment, CTA, and Q&A framing.
2. [AI] Write spoken language appropriate to presenter style and choose full-script versus bullet-note sections by risk/need for exact wording.
3. [AI] Make instructions/examples actionable enough to deliver the educational promise.
4. [AI] Integrate proof and claims with source context/qualifiers.
5. [HYBRID] Check timing, density, jargon, compliance-sensitive wording, guarantee/price/urgency statements, and likely audience questions.
6. [AI] Add cut points/optional material for timing variance without deleting critical teaching or Offer facts.
7. [DETERMINISTIC] Produce presenter notes with slide/demo cues and exact claim/evidence refs.
