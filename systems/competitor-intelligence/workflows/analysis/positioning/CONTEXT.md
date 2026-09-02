---
id: competitor.analysis.positioning
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
- Brand
- Business
- Market
- Objective
- Offer
- ProductService
---
# Positioning Intelligence

## Purpose
Determine the audience, problem frame, category, alternatives, differentiated value, and proof competitors emphasize.

## Business Outcome
Improve competitive decisions through evidence-backed positioning intelligence, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current positioning intelligence and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Gather homepage, product, campaign, about, sales, review, and other current positioning evidence.
2. [AI] Extract target audience, category frame, primary problem, desired outcome, differentiators, alternatives/opponents, proof, and repeated claims.
3. [HYBRID] Separate explicit positioning from analyst inference and assign evidence references.
4. [AI] Compare positioning by page/channel and determine whether differences are segment-specific or inconsistent.
5. [HYBRID] Compare with historical snapshots to identify strategic movement.
6. [AI] Map crowded claims versus distinctive positions and unaddressed customer criteria.
7. [HYBRID] Publish competitor positioning Insights; downstream Marketing decides our response.
