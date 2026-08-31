---
id: customer.analysis.pain-desire
type: playbook
version: 1.1.0
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
  - none
  optional:
  - customer_feedback.read
  - crm.opportunity.read
  - support.ticket.read
  - sales_call.read
  - survey.read
  - review.read
  - analytics.read
events:
  consumes:
  - none
  emits:
  - customer.insight.updated
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Pain, Desire & Outcome Analysis

## Purpose
Determine which problems and desired outcomes materially matter to defined customer segments.

## Business Outcome
Reduce uncertainty about customers through pain, desire & outcome analysis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current pain, desire & outcome analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Gather customer evidence that describes current-state problems, emotional/functional consequences, desired future states, and success definitions.
2. [AI] Separate surface symptoms from underlying jobs/outcomes; do not infer root causes without corroboration.
3. [HYBRID] Score themes by evidence breadth, intensity, decision relevance, frequency, and segment specificity rather than frequency alone.
4. [AI] Map relationships: pain → consequence → desired outcome → current alternative/workaround.
5. [HYBRID] Identify tensions where customers want conflicting outcomes such as speed vs control or price vs service.
6. [AI] Compare across audience segments and journey stages to avoid flattening materially different needs.
7. [HYBRID] Create/update Customer Insights with explicit scope, confidence, and evidence links.
