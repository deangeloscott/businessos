---
id: marketing.strategy.ethical-urgency
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
# Urgency and Scarcity Validation

## Purpose
Use genuine timing, capacity, availability, or consequence only when it is real and relevant.

## Business Outcome
Help qualified prospects act when delay has real cost without manufacturing pressure.

## Run When
Use when an asset/campaign proposes urgency, scarcity, countdowns, deadlines, limited capacity, or time-sensitive action.

## Process
1. [AI] Identify the real reason timing matters: deadline, inventory/capacity, event, enrollment window, price change, regulation, season, opportunity cost, or customer consequence.
2. [HYBRID] Verify the condition, source, start/end time, inventory/capacity logic, timezone, and what happens after expiry using the strongest available business/source evidence.
3. [AI] Distinguish urgency from scarcity and explain the consequence of delay accurately.
4. [HYBRID] Reject evergreen fake deadlines, resetting countdowns, invented limited seats, hidden extensions, or pressure unrelated to customer value.
5. [AI] Write urgency in proportion to evidence and allow a clear path for people who are not ready/eligible.
6. [HYBRID] Ensure the real operational system can honor the stated deadline/capacity when that can be verified, and treat changing conditions as a reason to update the affected Asset/business truth rather than as an AURA scheduling rule.
7. [AI] Preserve the validated urgency/scarcity guidance and evidence linkage in the relevant Asset when useful. Include material urgency claims in final claim validation; do not create a WorkRequest merely to move the result to another AURA method.
