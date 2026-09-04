---
id: industry.event.follow-up
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- IndustryEvent
- Observation
- Insight
context:
- Business
- Market
- Objective
---
# Industry Event Follow-Up

## Purpose
Determine and monitor the unresolved facts or future milestones that could change an Event’s relevance.

## Business Outcome
Keep important developing intelligence current without repeatedly researching settled facts.

## Run When
Run after a developing Event is created/updated or when a scheduled checkpoint is reached.

## Process
1. [AI] List unresolved questions and future milestones that could alter materiality, timing, scope, or response.
2. [AI] Map each question to the most authoritative likely source and expected date/trigger.
3. [DETERMINISTIC] Schedule checks according to event velocity/deadline rather than a universal cadence.
4. [INTEGRATION] At each checkpoint retrieve only the sources/signals relevant to unresolved items.
5. [AI] Apply update-diff and close resolved questions; add newly material unknowns.
6. [HYBRID] Escalate only if the new information can change a business/customer/domain decision.
7. [DETERMINISTIC] Close or reduce monitoring when the Event is settled and review conditions are met.
