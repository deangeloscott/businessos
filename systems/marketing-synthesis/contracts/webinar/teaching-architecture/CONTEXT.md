---
id: marketing.webinar.teaching-architecture
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
# Webinar Teaching Architecture

## Purpose
Design the educational framework, sequence, examples, and exercises that deliver the webinar’s promised transformation.

## Business Outcome
Make the webinar genuinely useful and create the understanding required for informed commercial consideration.

## Run When
Run after webinar objective is approved.

## Process
1. [AI] Define what attendees should know/be able to do by the end and the misconceptions/prerequisites blocking that state.
2. [AI] Break the transformation into the smallest coherent teaching sequence with clear concepts, examples, demonstrations, and checkpoints.
3. [AI] Choose a memorable framework only if it simplifies real structure rather than inventing arbitrary acronyms.
4. [AI] Add cases/examples/exercises where application is needed and identify evidence/source requirements.
5. [HYBRID] Confirm the teaching delivers standalone value and remove material that exists only to prolong presentation or hide useful details until the pitch.
6. [AI] Identify natural bridges where the business solution becomes relevant without interrupting education.
7. [DETERMINISTIC] Produce module/beat architecture and Content slide/demo requirements.
