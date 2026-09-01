---
id: marketing.webinar.persuasion-architecture
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
# Webinar Persuasion Architecture

## Purpose
Overlay the necessary belief, proof, objection, and Offer progression onto the educational structure without corrupting it.

## Business Outcome
Move qualified attendees toward an informed Offer decision while preserving the webinar’s standalone value.

## Run When
Run after teaching architecture and persuasion brief are available.

## Process
1. [AI] Map the beliefs/objections required for the commercial action against the teaching modules that naturally influence them.
2. [AI] Decide where to seed problem cost, mechanism, differentiation, proof, fit, and future possibility through useful examples rather than repeated pitching.
3. [AI] Select ProofRecords/demos that belong within teaching and proof that should remain in the explicit Offer section.
4. [AI] Identify the exact transition point where education has made the solution category/Offer relevant.
5. [HYBRID] Prevent manipulation such as false open loops, exaggerated pain, or education intentionally crippled to force purchase.
6. [AI] Define Q&A/objection strategy and what should be answered before versus after Offer presentation.
7. [DETERMINISTIC] Produce persuasion overlay linked to teaching beats and proof.
