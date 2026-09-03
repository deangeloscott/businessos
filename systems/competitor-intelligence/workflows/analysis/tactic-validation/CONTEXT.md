---
id: competitor.analysis.tactic-validation
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  domain: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Competitor Tactic Validation

## Purpose
Assess whether an observed competitor tactic has credible evidence of effectiveness before imitation.

## Business Outcome
Improve competitive decisions through evidence-backed competitor tactic validation, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor tactic validation and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [AI] Define the tactic precisely, intended mechanism, audience/context, and what success evidence would look like. Draw on `competitor.analysis.tactic-mechanism` when its mechanism-analysis method materially improves the judgment.
2. [DETERMINISTIC] Gather direct observable performance proxies, persistence/history, customer response, market movement, and independent evidence where available.
3. [HYBRID] Separate adoption/popularity from effectiveness and control for brand scale, budget, channel, timing, and selection effects.
4. [AI] Identify alternative explanations for apparent success.
5. [HYBRID] Grade evidence as unsupported, weak signal, plausible, supported, or contradicted with confidence.
6. [AI] State applicability constraints for our business rather than recommending blind copying.
7. [DETERMINISTIC] Publish/refresh Competitor Insight and candidate Learning only when evidence warrants.
