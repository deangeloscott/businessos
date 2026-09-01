---
id: customer.evidence-collection.cancellation-feedback
type: playbook
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
writes:
- SourceRecord
- Observation
capabilities:
  required:
  - customer_feedback.read
  optional: []
context:
- AudienceSegment
- Objective
---
# Cancellation Feedback Collection

## Purpose
Collect direct cancellation/churn explanations and preserve context needed to distinguish stated reasons from contributing conditions.

## Business Outcome
Create traceable customer Observations that preserve what was directly observed, what was inferred, and the limits of the source.

## Run When
Run when cancellation feedback is relevant to an active customer research question or Insight refresh.

## Process
1. [INTEGRATION] Retrieve only the cancellation feedback records relevant to the defined population, question, and time window.
2. [DETERMINISTIC] Preserve source identity, timestamp, subject/account reference when legitimately available, and raw/source pointer.
3. [AI] Extract decision-relevant statements or behaviors and keep direct evidence separate from internal interpretation.
4. [AI] Classify evidence by customer theme, journey context, segment, outcome, and evidence directness without forcing uncertain categories.
5. [HYBRID] Flag ambiguous identity, missing context, contradictory evidence, and source-specific bias rather than resolving them by guess.
6. [DETERMINISTIC] Deduplicate repeated records while preserving independently occurring evidence.
7. [AI] Publish scoped Observations and route foreign-domain facts as evidence rather than creating unsupported Customer Insights.
