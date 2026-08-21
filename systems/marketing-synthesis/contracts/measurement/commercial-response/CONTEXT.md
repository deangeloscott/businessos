---
id: marketing.measurement.commercial-response
type: playbook
version: 1.1.0
owner_system: marketing-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Opportunity
- Experiment
- Asset
- MetricObservation
- type: Insight
  owner_system: customer-intelligence
- Learning
writes:
- OutcomeEvaluation
- Insight
- Learning
capabilities:
  required:
  - none
  optional:
  - marketing.performance.read
  - conversion.read
  - analytics.read
  - revenue.read
---
# Marketing Outcome Analysis

## Purpose
Interpret commercial response and return scoped marketing/customer evidence without overclaiming causality.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed marketing outcome analysis that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires marketing outcome analysis to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [DETERMINISTIC] Retrieve business outcome and diagnostic metrics for the defined audience, offer, asset/campaign, channel, and evaluation window.
2. [DETERMINISTIC] Validate tracking, denominator, attribution window, spend/exposure, and comparable baseline/control.
3. [HYBRID] Separate creative/message response from channel/media effects, offer changes, journey friction, seasonality, and audience mix.
4. [AI] Evaluate the marketing hypothesis and identify which message/proof/offer/creative mechanisms are supported, contradicted, or unresolved.
5. [HYBRID] Assign causal confidence using experiment quality or weaker observational attribution as appropriate.
6. [HYBRID] Publish Marketing Insight/Learning; contribute behavioral evidence to Customer Intelligence without declaring customer psychology solely from conversion data.
7. [DETERMINISTIC] Complete OutcomeEvaluation and update Opportunity decision.
