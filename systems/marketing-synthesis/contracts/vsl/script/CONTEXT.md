---
id: marketing.vsl.script
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
# VSL Script

## Purpose
Write the complete conversion-focused VSL script from an approved persuasion architecture.

## Business Outcome
Produce a clear, credible, record-ready VSL that earns the commercial action through value and evidence.

## Run When
Run after VSL architecture and proof/Offer facts are ready.

## Process
1. [AI] Draft each persuasion beat in spoken language while preserving source-message match and evidence limitations.
2. [AI] Open with a true high-relevance hook and establish who the message is for/why it matters quickly.
3. [AI] Explain problem/outcome/mechanism with concrete examples and transitions that make the Offer a logical solution rather than abrupt pitch.
4. [AI] Integrate proof/demos where specific doubts arise and present fit, price/terms, risk reversal, and CTA accurately.
5. [AI] Address material objections without strawmen or pressure and disqualify poor-fit customers where appropriate.
6. [HYBRID] Review tone, claims, urgency, guarantees, comparative statements, and testimonial context.
7. [DETERMINISTIC] Produce final full script plus evidence/visual cues for Content.
