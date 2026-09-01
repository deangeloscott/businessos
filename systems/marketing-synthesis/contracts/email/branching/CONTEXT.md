---
id: marketing.email.branching
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
# Email Sequence Branching

## Purpose
Define how observed recipient state changes the next message or exits the sequence.

## Business Outcome
Make nurture responsive to meaningful behavior without overinterpreting noisy engagement signals.

## Run When
Use when an email sequence needs behavior/state-dependent branching or suppression logic.

## Process
1. [HYBRID] List available reliable events: purchase/booked/demo, form completion, reply, qualified page/action, attendance, product/customer state, unsubscribe, hard failure; treat opens/clicks cautiously where tracking is unreliable.
2. [AI] Define which events materially change audience state, objection, eligibility, or next best message.
3. [AI] Create branch rules with mutually understandable conditions and a default path.
4. [HYBRID] Avoid creepy personalization or inference from sensitive/ambiguous behavior.
5. [HYBRID] Define suppression/exit precedence so converted/ineligible/unsubscribed contacts stop receiving incompatible messages.
6. [AI] Keep branch count as small as necessary; merge paths that do not require materially different communication.
7. [HYBRID] Preserve the branch logic in the sequence Asset and test it against representative events when the real automation system is available. The host owns live automation; no WorkRequest is needed merely because drafting or QA follows.
