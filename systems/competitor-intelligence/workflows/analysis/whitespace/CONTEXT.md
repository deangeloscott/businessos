---
id: competitor.analysis.whitespace
type: workflow
owner_system: competitor-intelligence
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
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Competitive Whitespace Analysis

## Purpose
Identify customer needs, positions, offers, or market spaces that relevant competitors serve poorly.

## Business Outcome
Improve competitive decisions through evidence-backed competitive whitespace analysis, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitive whitespace analysis and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [AI] Define the decision scope and combine Customer Insights with current competitor products, positioning, offers, sentiment, and strategy.
2. [DETERMINISTIC] Create a comparison matrix of evidence-backed customer criteria versus competitor coverage/strength.
3. [AI] Identify gaps where a valuable criterion is weakly addressed, poorly proven, or structurally difficult for competitors.
4. [HYBRID] Exclude gaps that customers do not value or the business cannot credibly serve.
5. [HYBRID] Distinguish market whitespace from merely different messaging.
6. [AI] Generate downstream implication hypotheses without assigning another domain its action.
7. [HYBRID] Publish a Competitor Insight with confidence, evidence, and affected-domain candidates.
