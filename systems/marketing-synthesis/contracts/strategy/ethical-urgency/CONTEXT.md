---
id: marketing.strategy.ethical-urgency
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
# Urgency and Scarcity Validation

## Purpose
Use genuine timing, capacity, availability, or consequence only when it is real and relevant.

## Business Outcome
Help qualified prospects act when delay has real cost without manufacturing pressure.

## Run When
Run when an asset/campaign proposes urgency, scarcity, countdowns, deadlines, limited capacity, or time-sensitive action.

## Process
1. [AI] Identify the real reason timing matters: deadline, inventory/capacity, event, enrollment window, price change, regulation, season, opportunity cost, or customer consequence.
2. [DETERMINISTIC] Verify the condition, source, start/end time, inventory/capacity logic, timezone, and what happens after expiry.
3. [AI] Distinguish urgency from scarcity and explain the consequence of delay accurately.
4. [HYBRID] Reject evergreen fake deadlines, resetting countdowns, invented limited seats, hidden extensions, or pressure unrelated to customer value.
5. [AI] Write urgency in proportion to evidence and allow a clear path for people who are not ready/eligible.
6. [DETERMINISTIC] Ensure operational systems can honor the stated deadline/capacity and update the Asset when conditions change.
7. [DETERMINISTIC] Include urgency claims in final claim-validation/verification.
