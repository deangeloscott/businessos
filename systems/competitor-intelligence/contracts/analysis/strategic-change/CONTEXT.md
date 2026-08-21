---
id: competitor.analysis.strategic-change
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 4
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - review.read
  - crm.opportunity.read
  - social.observe
events:
  consumes:
  - none
  emits:
  - competitor.insight.updated
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - competitor.analysis.strategy-hypothesis
---
# Strategic Change Detection

## Purpose
Determine whether multiple competitor observations indicate a meaningful shift rather than isolated execution noise.

## Business Outcome
Improve competitive decisions through evidence-backed strategic change detection, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current strategic change detection and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [DETERMINISTIC] Gather material changes across product, pricing, packaging, positioning, offers, hiring, partnerships, content, advertising, and customer targets over a defined window.
2. [AI] Group changes by plausible strategic thesis and timeline.
3. [HYBRID] Require multiple aligned signals or one unusually direct authoritative signal before asserting strategic movement.
4. [AI] Generate alternative explanations and identify evidence that would discriminate them.
5. [HYBRID] Assess likely affected markets/audiences and potential threat/opportunity.
6. [DETERMINISTIC] Update strategic_summary only when confidence threshold is met; otherwise maintain a candidate Insight.
7. [DETERMINISTIC] Emit competitor.insight.updated when material.
