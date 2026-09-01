---
id: marketing.assets.email-sequence
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
writes:
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
  - marketing.email.sequence-strategy
  - marketing.email.message-draft
  - marketing.email.subject-preview
  - marketing.email.branching
  - marketing.email.qa
---
# Commercial Email Sequence

## Purpose
Design a multi-email persuasion sequence where each message has a distinct job and builds appropriately on prior context.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed commercial email sequence that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires commercial email sequence to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define audience state, entry trigger/source, Offer, desired final action, sequence horizon, and known objections/questions.
2. [AI] Assign a distinct job to each email: orient, deliver value, demonstrate mechanism/proof, address objection, case/example, offer, urgency if genuine, close/follow-up.
3. [AI] Draft subject/preheader/body/CTA with continuity but without repetitive restatement.
4. [HYBRID] Match frequency and urgency to relationship/permission and avoid artificial countdown/scarcity.
5. [DETERMINISTIC] Define branching/suppression for conversion, disengagement, segment, or lifecycle state where available.
6. [HYBRID] Validate links, terms, personalization, compliance, and measurement events before send.
