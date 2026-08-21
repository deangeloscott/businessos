---
id: customer.evidence-collection.behavioral
type: playbook
version: 1.3.0
owner_system: customer-intelligence
risk: low
autonomy_ceiling: 2
reads:
- SourceRecord
- Observation
writes:
- SourceRecord
- Observation
capabilities:
  required:
  - analytics.read
  optional: []
context:
- AudienceSegment
- Objective
---
# Customer Behavioral Evidence Collection

## Purpose
Convert customer behavior into scoped observations that can support or challenge customer hypotheses without pretending behavior directly reveals motive.

## Business Outcome
Create traceable customer Observations that preserve what was directly observed, what was inferred, and the limits of the source.

## Run When
Run when behavioral data is relevant to an active customer research question or Insight refresh.

## Process
1. [INTEGRATION] Retrieve only the behavioral data records relevant to the defined population, question, and time window.
2. [DETERMINISTIC] Preserve source identity, timestamp, subject/account reference when legitimately available, and raw/source pointer.
3. [AI] Extract decision-relevant statements or behaviors and keep direct evidence separate from internal interpretation.
4. [AI] Classify evidence by customer theme, journey context, segment, outcome, and evidence directness without forcing uncertain categories.
5. [HYBRID] Flag ambiguous identity, missing context, contradictory evidence, and source-specific bias rather than resolving them by guess.
6. [DETERMINISTIC] Deduplicate repeated records while preserving independently occurring evidence.
7. [AI] Publish scoped Observations and route foreign-domain facts as evidence rather than creating unsupported Customer Insights.
