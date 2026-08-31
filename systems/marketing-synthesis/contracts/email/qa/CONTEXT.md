---
id: marketing.email.qa
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
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
# Email Sequence QA

## Purpose
Verify the complete email sequence, logic, content, links, consent, and terminal behavior before sending.

## Business Outcome
Prevent broken automation, wrong personalization, stale Offers, or inappropriate follow-up from reaching prospects/customers.

## Run When
Run when a commercial email sequence requires this specific planning, drafting, logic, or QA job.

## Process
1. [DETERMINISTIC] Validate audience/entry, sender, consent/suppression, sequence order, delays, branches, exits, Offer version, and tracking.
2. [HYBRID] Review every message for claim/proof, tone, personalization, urgency, legal/compliance, and alignment with its assigned job.
3. [DETERMINISTIC] Test dynamic fields/fallbacks, links, forms/calendar/pages, mobile rendering, unsubscribe/preferences, and reply handling.
4. [AI] Inspect the sequence as one conversation for repetition, contradictions, missing context, or too many asks.
5. [DETERMINISTIC] Simulate key behavior branches including conversion, no action, reply, unsubscribe, and failure.
6. [HYBRID] Block launch for material consent/logic/Offer errors and assign unresolved issues.
7. [DETERMINISTIC] Verify live automation version after activation and define monitoring/rollback.
