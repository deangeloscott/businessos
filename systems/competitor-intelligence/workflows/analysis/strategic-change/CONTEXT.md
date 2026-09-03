---
id: competitor.analysis.strategic-change
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
# Strategic Change Detection

## Purpose
Determine whether multiple competitor observations indicate a meaningful shift rather than isolated execution noise.

## Business Outcome
Improve competitive decisions through evidence-backed strategic change detection, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current strategic change detection and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [DETERMINISTIC] Gather material changes across product, pricing, packaging, positioning, offers, hiring, partnerships, content, advertising, and customer targets over a defined window.
2. [AI] Group changes by plausible strategic thesis and timeline. Draw on `competitor.analysis.strategy-hypothesis` when its hypothesis method materially improves the analysis.
3. [HYBRID] Require multiple aligned signals or one unusually direct authoritative signal before asserting strategic movement.
4. [AI] Generate alternative explanations and identify evidence that would discriminate them.
5. [HYBRID] Assess likely affected markets/audiences and potential threat/opportunity.
6. [AI] Update the durable strategic summary or preserve a candidate Insight only when the evidence supports that interpretation; keep uncertainty explicit when the signal is not strong enough.
7. [DETERMINISTIC] Persist the selected Competitor, Observation, and Insight state and validate references. Do not emit an AURA runtime event merely because strategic understanding changed.
