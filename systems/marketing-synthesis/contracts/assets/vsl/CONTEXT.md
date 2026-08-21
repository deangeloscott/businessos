---
id: marketing.assets.vsl
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 3
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- ActionPacket
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - email.send
  - social.ad.publish
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
subcontracts:
  required:
  - marketing.intake.persuasion-brief
  - marketing.vsl.persuasion-architecture
  - marketing.vsl.script
  - marketing.vsl.visual-brief
  - marketing.vsl.offer-cta
  - marketing.vsl.qa
---
# Video Sales Letter

## Purpose
Build a sustained video persuasion narrative tied to an offer and measurable commercial action.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed video sales letter that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires video sales letter to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define prospect state, desired action, Offer, dominant problem/desire, mechanism, objections, proof, and expected viewing context.
2. [AI] Design persuasion arc: pattern/context → stakes/problem → desired future → mechanism/new understanding → proof → objections → offer/value/risk → CTA.
3. [HYBRID] Ensure each claim/proof segment is evidence-backed and no fabricated scarcity/urgency is introduced.
4. [AI] Script spoken language with demonstrations, visual proof, pacing, transitions, and CTA moments.
5. [HYBRID] Match length to complexity/awareness rather than arbitrary VSL convention.
6. [DETERMINISTIC] Delegate rendering/visual/audio production to Content with complete success criteria.
