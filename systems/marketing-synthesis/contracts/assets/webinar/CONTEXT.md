---
id: marketing.assets.webinar
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
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
subcontracts:
  required:
  - marketing.webinar.objective
  - marketing.webinar.teaching-architecture
  - marketing.webinar.persuasion-architecture
  - marketing.webinar.offer-transition
  - marketing.webinar.script
  - marketing.webinar.slide-brief
  - marketing.webinar.qa
  conditional:
  - id: marketing.webinar.registration
    when: the session requires registration
  - id: marketing.webinar.reminders
    when: registered attendees should receive reminders
  - id: marketing.webinar.follow-up
    when: post-session follow-up is permitted and valuable
---
# Webinar Persuasion

## Purpose
Design a webinar that creates genuine understanding/value while logically leading qualified attendees to an Offer.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed webinar matched to audience awareness, Offer, proof, acquisition context, and the actual session experience.

## Run When
Use when the organization needs a webinar to educate, persuade, demonstrate, or support a commercial decision. An Opportunity, prior Asset, or real WorkRequest may provide context but is not required.

## Process
1. [AI] Define audience starting beliefs, desired transformation, teaching promise, Offer, objections, proof, session format, and commercial action.
2. [AI] Use the authored webinar submethods as relevant composition/quality knowledge to structure a value-first narrative: why topic matters → useful framework/demo/case → implications → transition to solution/Offer → proof → fit/terms → CTA/Q&A.
3. [HYBRID] Ensure the educational content stands on its own and material outward claims are supported; do not manufacture urgency, scarcity, proof, or outcomes.
4. [AI] Create the speaker logic/script and slide-level teaching/persuasion jobs. If slide production is within the user's request and the harness can create the presentation, produce it directly; otherwise preserve a usable slide brief or create a WorkRequest only for a real durable handoff to another actor.
5. [AI] Build the objection/proof/FAQ plan and registration/reminder/follow-up content only where those parts are relevant to the requested webinar and real communication permissions/constraints.
6. [HYBRID] Define useful attendance, engagement, conversion, quality, and follow-up measurement without pretending a configured schedule or campaign exists merely because the plan describes one.
7. [HYBRID] Apply customer-facing claim/QA checks appropriate to the produced Assets and preserve only the durable webinar materials/decisions future work benefits from. Sending, scheduling, hosting, publishing, and measurement execution belong to the active harness/external systems.

## Verification
- Teaching creates genuine standalone value and the transition to the Offer is coherent rather than deceptive.
- Claims, proof, Offer terms, urgency, reminders, and follow-up remain within current organizational truth and real constraints.
- Slide/content production is composed directly when available rather than delegated between AURA domains.
- Planned registration/reminder/follow-up behavior is not represented as active runtime state unless the external system actually implements it.

## Completion Criteria
- The organization has the requested usable webinar system or the precise remaining real-world handoff needed to finish it, without an internal AURA request chain.
