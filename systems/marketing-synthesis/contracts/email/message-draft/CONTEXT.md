---
id: marketing.email.message-draft
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
# Marketing Email Draft

## Purpose
Write one email to perform its assigned job in an approved sequence.

## Business Outcome
Move the reader one appropriate step using clear, relevant, evidence-backed communication.

## Run When
Run when a commercial email sequence requires this specific planning, drafting, logic, or QA job.

## Process
1. [DETERMINISTIC] Resolve sequence job, recipient state, prior messages/actions, Offer, Customer Insights, proof, and CTA.
2. [AI] Write the email around one primary message/action; open with context/value rather than generic greetings/filler.
3. [AI] Use customer language and specifics appropriate to awareness while avoiding claims not supported by evidence.
4. [AI] Integrate proof/objection handling only if needed for this message’s job.
5. [AI] Make CTA and what-happens-next explicit; include alternatives/exit where appropriate.
6. [HYBRID] Check consent, sensitive personalization, urgency, Offer version, tone, and frequency context.
7. [DETERMINISTIC] Output subject-body-CTA package linked to sequence position and claim/proof refs.
