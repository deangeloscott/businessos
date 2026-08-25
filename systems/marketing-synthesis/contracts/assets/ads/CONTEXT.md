---
id: marketing.assets.ads
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
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
  - marketing.ads.angle-matrix
  - marketing.ads.copy
  - marketing.ads.creative-brief
  - marketing.ads.message-match
  - marketing.ads.variant-plan
  - marketing.ads.qa
---
# Advertising Creative & Copy

## Purpose
Create persuasive ad concepts/copy/creative requirements matched to audience, awareness, channel context, and destination.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed advertising creative & copy that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires advertising creative & copy to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define channel placement/context, audience, awareness, Offer, desired action, landing destination, and message continuity.
2. [AI] Generate concept families with distinct hook/angle/mechanism/proof rather than cosmetic headline variants.
3. [HYBRID] Check claims, policy/compliance, proof, and whether the creative promise is fulfilled by the destination.
4. [AI] Write copy/creative brief variants sized to placement and platform behavior; specify visual/audio requirements.
5. [HYBRID] Design a test matrix isolating meaningful variables where possible.
6. [DETERMINISTIC] Create WorkRequests to Content for media production and package tracking/measurement requirements.
