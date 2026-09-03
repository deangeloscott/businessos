---
id: marketing.assets.email-sequence
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- type: Insight
  domain: customer-intelligence
- type: Insight
  domain: competitor-intelligence
- Asset
- WorkRequest
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Commercial Email Sequence

## Purpose
Design a multi-email persuasion sequence where each message has a distinct job and builds appropriately on prior context.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed sequence matched to audience awareness, Offer, proof, acquisition context, and the actual relationship/permission state.

## Run When
Use when the organization needs a commercial email sequence or nurture/follow-up sequence. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. Define audience state, entry trigger/source, Offer, desired final action, sequence horizon, known objections/questions, and real communication permission/relationship constraints.
2. Use relevant email operating knowledge—such as sequence strategy, message drafting, subject/preheader work, branching, or QA—only where it materially improves the requested sequence. Assign a distinct job to each message, such as orient, deliver value, demonstrate mechanism/proof, address objection, present a case/example, make the Offer, communicate genuine urgency, or close/follow up.
3. Draft subject/preheader/body/CTA with continuity but without repetitive restatement or unsupported personalization.
4. Match frequency, urgency, and segmentation to the relationship and evidence rather than maximum contact frequency; do not manufacture countdowns, scarcity, or behavioral knowledge the organization does not actually have.
5. Define branching/suppression for conversion, disengagement, segment, or lifecycle state only where those states/signals really exist. The active email/CRM system owns automation/runtime state.
6. Validate claims, links, Offer terms, personalization, compliance, and useful measurement before any send.
7. Preserve the usable sequence Asset(s). If sending/automation is explicitly requested and the harness has the real capabilities/permissions, perform it through the external system; otherwise do not create an internal WorkRequest merely because execution remains outside AURA. Use a WorkRequest only for a genuine durable handoff to another actor.

## Proportionate Scope
Use only the number of emails, branches, segments, personalization fields, and measurement detail justified by the audience state, Offer, relationship, uncertainty, and expected value of additional messages. Do not add messages or branches merely to make the sequence look complete.

## Verification
- Each email has a distinct useful job and the sequence builds coherent context.
- Claims, personalization, urgency, frequency, and Offer terms stay within current evidence and real constraints.
- Relevant Workflows are reusable operating knowledge, not required execution stages.
- Branching/suppression logic is a design unless it has actually been configured in the external system.
- AURA does not treat the sequence as an internal request pipeline.

## Completion Criteria
- The organization has a usable evidence-bounded email sequence at the requested level of fidelity, with sending/automation state reported truthfully and separately.
