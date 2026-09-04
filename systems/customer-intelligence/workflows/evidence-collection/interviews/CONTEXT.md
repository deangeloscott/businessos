---
id: customer.evidence-collection.interviews
type: workflow
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
context:
- AudienceSegment
- Market
- Offer
- ProductService
---
# Customer Interview Intelligence

## Purpose
Collect and interpret interviews without turning individual anecdotes into broad customer truth.

## Business Outcome
Reduce uncertainty about customers through customer interview intelligence, so future decisions reflect current customer evidence rather than assumption.

## Run When
Use when a decision requires current customer interview intelligence and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [HYBRID] Define the decision question, target segment, interview inclusion/exclusion criteria, and evidence gaps before selecting participants. Draw on research planning/sample-design operating knowledge when it materially improves the study rather than as mandatory setup.
2. [DETERMINISTIC] Record participant context, date, relationship stage, and consent/access constraints without adding unsupported demographic assumptions.
3. [HUMAN] Conduct or obtain the interview using open questions first; use interview-guide and participant-recruiting methods when useful, not as required AURA stages. Distinguish spontaneous statements from prompted reactions.
4. [AI] Extract verbatim problem/desire/objection/trigger/decision-criterion statements and retain source references/timestamps.
5. [AI] Separate what the participant experienced, what they believe caused it, and what the analyst infers.
6. [HYBRID] Compare with prior interviews and other evidence; identify repeated, segment-specific, novel, and contradictory themes. Structured interview-coding methods may help when evidence volume warrants them.
7. [HYBRID] Update/create Customer Insights only when evidence supports the claimed scope; otherwise preserve Observations and knowledge gaps without manufacturing a confidence score.
