---
id: customer.evidence-collection.site-search
type: playbook
version: 1.3.0
owner_system: customer-intelligence
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
# Site Search Evidence Collection

## Purpose
Use internal search behavior as evidence of customer questions, terminology, and unmet information needs without inferring motive from queries alone.

## Business Outcome
Create traceable customer Observations that preserve what was directly observed, what was inferred, and the limits of the source.

## Run When
Run when site-search behavior is relevant to an active customer research question or Insight refresh.

## Process
1. [INTEGRATION] Retrieve only the site-search behavior records relevant to the defined population, question, and time window.
2. [DETERMINISTIC] Preserve source identity, timestamp, subject/account reference when legitimately available, and raw/source pointer.
3. [AI] Extract decision-relevant statements or behaviors and keep direct evidence separate from internal interpretation.
4. [AI] Classify evidence by customer theme, journey context, segment, outcome, and evidence directness without forcing uncertain categories.
5. [HYBRID] Flag ambiguous identity, missing context, contradictory evidence, and source-specific bias rather than resolving them by guess.
6. [DETERMINISTIC] Deduplicate repeated records while preserving independently occurring evidence.
7. [AI] Publish scoped Observations and route foreign-domain facts as evidence rather than creating unsupported Customer Insights.
