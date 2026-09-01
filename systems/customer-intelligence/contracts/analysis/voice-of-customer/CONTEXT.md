---
id: customer.analysis.voice-of-customer
type: playbook
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
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Voice-of-Customer Synthesis

## Purpose
Build a reusable evidence-backed language and theme map for a defined customer scope.

## Business Outcome
Reduce uncertainty about customers through voice-of-customer synthesis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current voice-of-customer synthesis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Retrieve relevant customer Observations across interviews, sales, support, surveys, reviews, and communities for the defined scope.
2. [DETERMINISTIC] Preserve source counts and source diversity so one prolific source does not masquerade as broad agreement.
3. [AI] Cluster semantically equivalent statements while keeping meaningfully different customer wording variants.
4. [AI] Classify each cluster as pain, desire, outcome, objection, trigger, question, decision criterion, complaint, alternative, or language pattern.
5. [HYBRID] Compare recurrence, intensity, specificity, segment concentration, recency, and source diversity.
6. [AI] Extract representative exact-language examples without converting memorable wording into prevalence claims.
7. [HYBRID] Create/update scoped Customer Insights and a reusable vocabulary map; flag contradictions and missing segments.
