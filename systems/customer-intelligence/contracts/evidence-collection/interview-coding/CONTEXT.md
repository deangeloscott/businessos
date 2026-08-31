---
id: customer.evidence-collection.interview-coding
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- SourceRecord
writes:
- Observation
capabilities:
  required:
  - document.read
  optional:
  - sales_call.read
context:
- AudienceSegment
- Objective
---
# Customer Interview Coding

## Purpose
Convert completed interviews into comparable evidence while preserving direct language and context.

## Business Outcome
Create reliable interview Observations that support cross-case analysis without flattening nuance or inventing motives.

## Run When
Run after interviews are completed and recordings/transcripts/notes are available.

## Process
1. [DETERMINISTIC] Link each interview to participant/sample metadata, recording/transcript source, date, and research question.
2. [AI] Extract direct statements, concrete events, decisions, alternatives, before/after states, objections, outcomes, and language.
3. [AI] Code primary and secondary themes using existing taxonomy where appropriate while allowing new themes to emerge.
4. [HYBRID] Separate participant statements from interviewer interpretation and mark uncertain interpretation explicitly.
5. [AI] Capture negative cases and contradictions instead of coding only evidence that supports the hypothesis.
6. [DETERMINISTIC] Preserve exact source locations/timestamps for material quotations or claims.
7. [AI] Publish interview Observations and an evidence-coverage update; do not promote themes to Insights solely because they are vivid.
