---
id: marketing.measurement.commercial-response
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Experiment
- Asset
- MetricObservation
- type: Insight
  domain: customer-intelligence
- Learning
writes:
- OutcomeEvaluation
- Insight
- Learning
---
# Marketing Outcome Analysis

## Purpose
Interpret commercial response and preserve scoped marketing/customer evidence without overclaiming causality.

## Business Outcome
Improve future commercial decisions by separating what the observed response actually supports from channel effects, offer effects, customer/journey factors, and unresolved attribution.

## Run When
Use when consequential marketing work has enough outcome evidence to evaluate what happened and what should be learned from it.

## Process
1. [DETERMINISTIC] Retrieve business outcome and diagnostic metrics for the defined audience, offer, asset/campaign, channel, and evaluation window.
2. [DETERMINISTIC] Validate tracking, denominator, attribution window, spend/exposure, and comparable baseline/control where available.
3. [HYBRID] Separate creative/message response from channel/media effects, offer changes, journey friction, seasonality, and audience mix.
4. [AI] Evaluate the marketing hypothesis and identify which message/proof/offer/creative mechanisms are supported, contradicted, or unresolved.
5. [HYBRID] Describe the attribution basis, experiment quality, confounders, and material uncertainty at the level the evidence supports. Preserve real method-specific statistical uncertainty when available; do not manufacture a universal causal-confidence score.
6. [HYBRID] Preserve durable Insight/Learning only when the evidence supports a reusable organizational conclusion. Customer-behavior implications may be classified in the customer-intelligence domain when useful, without declaring customer psychology solely from conversion data or creating an internal handoff.
7. [DETERMINISTIC] Persist an OutcomeEvaluation when the result has durable organizational value and update related decision state only where that state genuinely changed.
