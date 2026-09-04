---
id: marketing.email.subject-preview
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Email Subject and Preview

## Purpose
Create subject/preview combinations that accurately signal the email’s value and context.

## Business Outcome
Improve qualified opens without misleading curiosity or disconnect from the body.

## Run When
Use when a commercial email needs subject/preview work. An existing email/sequence Asset or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Identify the real reason the recipient should open this specific message now.
2. [AI] Generate materially different truthful mechanisms: context, benefit, question, specificity, update, consequence, or direct label.
3. [AI] Pair subject and preview so they add information instead of duplicating each other.
4. [HYBRID] Reject deceptive RE/FWD, false personal familiarity, fake urgency, or claims absent from the email.
5. [AI] Match tone to relationship/sequence state and sender identity.
6. [HYBRID] Check likely length/render risk/dynamic-field fallback and select limited test variants if justified.
7. [AI] Attach the selected subject/preview to the exact email Asset/version. Do not create a WorkRequest merely to continue drafting, QA, or sending.
