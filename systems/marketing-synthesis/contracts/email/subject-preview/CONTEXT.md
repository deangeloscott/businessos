---
id: marketing.email.subject-preview
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
completion_evidence:
  required_text_components:
  - id: exact-email-linkage
    any_of: [sequence position, message job, email 1, email 2]
  - id: subject
    any_of: [subject line, "subject:"]
  - id: preview
    any_of: [preview text, preheader, "preview:"]
---
# Email Subject and Preview

## Purpose
Create subject/preview combinations that accurately signal the email’s value and context.

## Business Outcome
Improve qualified opens without misleading curiosity or disconnect from the body.

## Run When
Run when a commercial email sequence requires this specific planning, drafting, logic, or QA job.

## Process
1. [AI] Identify the real reason the recipient should open this specific message now.
2. [AI] Generate materially different truthful mechanisms: context, benefit, question, specificity, update, consequence, or direct label.
3. [AI] Pair subject and preview so they add information instead of duplicating each other.
4. [HYBRID] Reject deceptive RE/FWD, false personal familiarity, fake urgency, or claims absent from the email.
5. [AI] Match tone to relationship/sequence state and sender identity.
6. [DETERMINISTIC] Check length/render risk/dynamic-field fallback and select limited test variants if justified.
7. [AI] Attach selected subject/preview to the exact email Asset/version.
