---
id: customer.analysis.segmentation
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
- Business
- Market
- Objective
- ProductService
workflows:
  required:
  - customer.research.evidence-coverage
  - customer.analysis.segment-brief
---
# Customer Segmentation Intelligence

## Purpose
Identify evidence-backed customer differences that warrant distinct treatment rather than inventing personas.

## Business Outcome
Reduce uncertainty about customers through customer segmentation intelligence, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current customer segmentation intelligence and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Start from canonical Audience Segments and the business decisions segmentation must improve.
2. [DETERMINISTIC] Assemble valid attributes and behavior/outcome evidence without using prohibited/sensitive characteristics improperly.
3. [AI] Look for materially different needs, criteria, language, objections, outcomes, and journey behavior across existing segments.
4. [HYBRID] Test whether proposed segment boundaries are stable, interpretable, reachable/actionable, and large/valuable enough to matter.
5. [AI] Avoid creating a new segment when the difference is merely channel behavior or a one-off preference.
6. [HYBRID] Compare alternative segmentations and document what decision would change under each.
7. [HYBRID] Submit a Context Update Proposal when canonical AudienceSegment definitions should change; do not rewrite Core directly.
