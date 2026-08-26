---
id: marketing.email.sequence-strategy
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
  - id: entry-and-eligibility
    any_of: [entry trigger, eligibility, eligible audience]
  - id: exit-and-suppression
    any_of: [exit condition, suppression, stop sending]
  - id: distinct-message-jobs
    any_of: [message job, email job, sequence map]
  - id: timing-or-cadence
    any_of: [timing, cadence, delay]
  - id: success-or-terminal-state
    any_of: [success event, tracking event, terminal state]
---
# Email Sequence Strategy

## Purpose
Define entry, exit, message jobs, timing, branches, and success for a commercial email sequence.

## Business Outcome
Create a sequence where each message advances a distinct belief/action instead of repeatedly asking for the same conversion.

## Run When
Run when a commercial email sequence requires this specific planning, drafting, logic, or QA job.

## Process
1. [DETERMINISTIC] Define entry trigger, audience/eligibility, current state, desired end state, Offer/action, consent, suppression, and exit conditions.
2. [AI] Map the minimum belief/information/objection sequence required between entry and action.
3. [AI] Assign each email one distinct job and determine when behavior should branch, accelerate, pause, or stop the sequence.
4. [AI] Set timing from customer context/event/deadline and known behavior rather than arbitrary daily cadence.
5. [HYBRID] Prevent excessive frequency, contradictory messages, or sending after conversion/ineligibility.
6. [DETERMINISTIC] Define events, dynamic fields, tracking, holdouts/tests, and terminal states.
7. [AI] Produce sequence map for message drafting.
