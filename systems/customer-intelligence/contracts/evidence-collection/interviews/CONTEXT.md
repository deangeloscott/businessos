---
id: customer.evidence-collection.interviews
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - customer_feedback.read
  optional:
  - crm.contact.read
  - analytics.read
context:
- AudienceSegment
- Market
- Offer
- ProductService
subcontracts:
  required:
  - customer.research.plan
  - customer.research.sample-design
  - customer.evidence-collection.interview-guide
  - customer.evidence-collection.interview-participants
  - customer.evidence-collection.interview-coding
---
# Customer Interview Intelligence

## Purpose
Collect and interpret interviews without turning individual anecdotes into broad customer truth.

## Business Outcome
Reduce uncertainty about customers through customer interview intelligence, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current customer interview intelligence and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [HYBRID] Define the decision question, target segment, interview inclusion/exclusion criteria, and evidence gaps before selecting participants.
2. [DETERMINISTIC] Record participant context, date, relationship stage, and consent/access constraints without adding unsupported demographic assumptions.
3. [HUMAN] Conduct or obtain the interview using open questions first; distinguish spontaneous statements from prompted reactions.
4. [AI] Extract verbatim problem/desire/objection/trigger/decision-criterion statements and retain source references/timestamps.
5. [AI] Separate what the participant experienced, what they believe caused it, and what the analyst infers.
6. [HYBRID] Compare with prior interviews and other evidence; identify repeated, segment-specific, novel, and contradictory themes.
7. [HYBRID] Update/create Customer Insights only when evidence supports scope/confidence; otherwise publish Observations and knowledge gaps.
