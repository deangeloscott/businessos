---
id: marketing.assets.sales-letter
type: playbook
version: 1.2.0
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
---
# Sales Letter

## Purpose
Create long-form written persuasion appropriate to audience sophistication and Offer complexity.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed sales letter that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires sales letter to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define audience/awareness/intent, Offer, problem/outcome, objections, proof, and desired action.
2. [AI] Choose argument architecture appropriate to market sophistication rather than formulaically applying one copy template.
3. [AI] Draft with concrete claims, evidence, examples, transition logic, objections, value, terms, risk, and CTA.
4. [HYBRID] Audit every major promise against proof and canonical Offer/Brand constraints.
5. [AI] Remove inflated language, redundant persuasion, and pressure unsupported by customer reality.
6. [HYBRID] Test message continuity and readability; package for final content/design production as needed.
