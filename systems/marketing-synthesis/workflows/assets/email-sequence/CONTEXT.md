---
id: marketing.assets.email-sequence
type: workflow
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
- Asset
context:
- AudienceSegment
- Brand
- Offer
workflows:
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
Increase the likelihood of the desired commercial action through an evidence-backed sequence matched to audience awareness, Offer, proof, acquisition context, and the actual relationship/permission state.

## Run When
Use when the organization needs a commercial email sequence or nurture/follow-up sequence. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. [AI] Define audience state, entry trigger/source, Offer, desired final action, sequence horizon, known objections/questions, and real communication permission/relationship constraints.
2. [AI] Use the authored email submethods as relevant composition/quality knowledge. Assign a distinct job to each message: orient, deliver value, demonstrate mechanism/proof, address objection, case/example, Offer, genuine urgency where applicable, close/follow-up.
3. [AI] Draft subject/preheader/body/CTA with continuity but without repetitive restatement or unsupported personalization.
4. [HYBRID] Match frequency, urgency, and segmentation to the relationship and evidence rather than maximum contact frequency; do not manufacture countdowns, scarcity, or behavioral knowledge the organization does not actually have.
5. [AI] Define branching/suppression for conversion, disengagement, segment, or lifecycle state only where those states/signals really exist. The active email/CRM system owns automation/runtime state.
6. [HYBRID] Validate claims, links, Offer terms, personalization, compliance, and useful measurement before any send.
7. [HYBRID] Preserve the usable sequence Asset(s). If sending/automation is explicitly requested and the harness has the real capabilities/permissions, perform it through the external system; otherwise do not create an internal WorkRequest merely because execution remains outside AURA. Use a WorkRequest only for a genuine durable handoff to another actor.

## Verification
- Each email has a distinct useful job and the sequence builds coherent context.
- Claims, personalization, urgency, frequency, and Offer terms stay within current evidence and real constraints.
- Branching/suppression logic is a design unless it has actually been configured in the external system.
- AURA does not treat the sequence as an internal request pipeline.

## Completion Criteria
- The organization has a usable evidence-bounded email sequence at the requested level of fidelity, with sending/automation state reported truthfully and separately.
