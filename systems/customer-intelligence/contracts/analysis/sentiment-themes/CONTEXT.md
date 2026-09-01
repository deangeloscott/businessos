---
id: customer.analysis.sentiment-themes
type: playbook
owner_system: customer-intelligence
reads:
- Observation
- SourceRecord
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - none
  optional:
  - none
context:
- AudienceSegment
- ProductService
- Offer
---
# Sentiment and Theme Analysis

## Purpose
Explain what public or first-party customer evidence is positive, negative, mixed, or changing at the level of specific experiences and topics rather than reducing people to a single sentiment score.

## Business Outcome
Identify which parts of the customer experience, offer, product, or category are creating enthusiasm, uncertainty, frustration, or unmet demand and make those patterns usable by downstream systems.

## Run When
Run when enough current customer Observations exist to compare sentiment/themes or when a material change in public/customer conversation needs interpretation.

## Process
1. [DETERMINISTIC] Select a defensible evidence set by source, time window, audience/product/market scope, and lifecycle context; retain source counts and missing-coverage notes.
2. [AI] Classify sentiment at the aspect/theme level, including mixed statements such as “hard setup but excellent result,” rather than assigning one label to the entire person or review.
3. [AI] Extract the reason behind each sentiment where directly stated and separate stated cause from analyst inference.
4. [DETERMINISTIC] Compare frequency, intensity, freshness, source diversity, and trend direction without letting a high-engagement post count as many independent customers.
5. [AI] Identify persistent themes, emerging changes, segment differences, contradictions, and issues where the evidence is too sparse or biased for a conclusion.
6. [HYBRID] Compare findings against existing Customer Insights and update, narrow, contradict, or create Insights only when the evidence warrants it.
7. [DETERMINISTIC] Preserve direct Observations and scope/confidence so Marketing, Content, Product/future systems, and Customer Optimization can use the result without mistaking sentiment for causal proof.
