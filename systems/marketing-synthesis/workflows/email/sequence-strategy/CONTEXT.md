---
id: marketing.email.sequence-strategy
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
# Email Sequence Strategy

## Purpose
Define entry, exit, message jobs, timing, branches, and success for a commercial email sequence.

## Business Outcome
Create a sequence where each message advances a distinct belief/action instead of repeatedly asking for the same conversion.

## Run When
Use when a commercial email sequence needs planning, message-job design, timing, or logic. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [HYBRID] Define entry trigger, audience/eligibility, current state, desired end state, Offer/action, consent, suppression, and exit conditions from the real customer/communication context.
2. [AI] Map the minimum belief/information/objection sequence required between entry and action.
3. [AI] Assign each email one distinct job and determine when behavior should branch, accelerate, pause, or stop the sequence.
4. [AI] Set timing from customer context/event/deadline and known behavior rather than arbitrary daily cadence.
5. [HYBRID] Prevent excessive frequency, contradictory messages, or sending after conversion/ineligibility.
6. [HYBRID] Define useful events, dynamic fields, tracking, holdouts/tests, and terminal states without turning AURA into the scheduler or sending runtime.
7. [AI] Preserve the sequence map as a Marketing-owned Asset for direct use by drafting, branching, subject/preview, QA, and real send/schedule execution. Do not create a WorkRequest merely to move between those methods.
