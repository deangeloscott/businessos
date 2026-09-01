---
id: marketing.assets.sales-letter
type: playbook
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
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
Increase the likelihood of the desired commercial action through an evidence-backed sales letter that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a sales letter is useful to remove a commercial persuasion gap or create the required conversion asset. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define audience/awareness/intent, Offer, problem/outcome, objections, proof, and desired action.
2. [AI] Choose argument architecture appropriate to market sophistication rather than formulaically applying one copy template.
3. [AI] Draft with concrete claims, evidence, examples, transition logic, objections, value, terms, risk, and CTA.
4. [HYBRID] Audit every major promise against proof and canonical Offer/Brand constraints.
5. [AI] Remove inflated language, redundant persuasion, and pressure unsupported by customer reality.
6. [HYBRID] Test message continuity and readability. Use relevant Content operating knowledge and the active harness's real document/design capabilities directly when production beyond text is needed; persist a WorkRequest only for a real durable organizational handoff.
