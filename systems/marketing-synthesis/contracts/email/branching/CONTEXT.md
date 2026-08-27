---
id: marketing.email.branching
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
# Email Sequence Branching

## Purpose
Define how observed recipient state changes the next message or exits the sequence.

## Business Outcome
Make nurture responsive to meaningful behavior without overinterpreting noisy engagement signals.

## Run When
Run when a commercial email sequence requires this specific planning, drafting, logic, or QA job.

## Process
1. [DETERMINISTIC] List available reliable events: purchase/booked/demo, form completion, reply, qualified page/action, attendance, product/customer state, unsubscribe, hard failure; treat opens/clicks cautiously where tracking is unreliable.
2. [AI] Define which events materially change audience state, objection, eligibility, or next best message.
3. [AI] Create branch rules with mutually understandable conditions and a default path.
4. [HYBRID] Avoid creepy personalization or inference from sensitive/ambiguous behavior.
5. [DETERMINISTIC] Define suppression/exit precedence so converted/ineligible/unsubscribed contacts stop receiving incompatible messages.
6. [AI] Keep branch count as small as necessary; merge paths that do not require materially different communication.
7. [DETERMINISTIC] Validate branch logic against test contacts/events before launch.
