---
id: marketing.email.message-draft
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
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
# Marketing Email Draft

## Purpose
Write one email to perform its assigned job in a sequence or standalone communication.

## Business Outcome
Move the reader one appropriate step using clear, relevant, evidence-backed communication.

## Run When
Use when a commercial email requires this specific drafting job. An existing sequence Asset or real durable WorkRequest may provide context but is not required.

## Process
1. [HYBRID] Resolve message job, recipient state, relevant prior messages/actions, Offer, Customer evidence, proof, and CTA from the current context available.
2. [AI] Write the email around one primary message/action; open with context/value rather than generic greetings/filler.
3. [AI] Use customer language and specifics appropriate to awareness while avoiding claims not supported by evidence.
4. [AI] Integrate proof/objection handling only if needed for this message’s job.
5. [AI] Make CTA and what-happens-next explicit; include alternatives/exit where appropriate.
6. [HYBRID] Check consent, sensitive personalization, urgency, Offer version, tone, and frequency context.
7. [AI] Preserve the useful subject/body/CTA package as an Asset with sequence position and claim/proof references when future work benefits from it. Do not create a WorkRequest merely because another AURA method may be used next.
