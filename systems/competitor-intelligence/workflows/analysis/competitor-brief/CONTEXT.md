---
id: competitor.analysis.competitor-brief
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Current Competitor Brief

## Purpose
Assemble a concise current view of a priority competitor from canonical state and active Insights.

## Business Outcome
Give downstream decisions a current, evidence-linked competitive picture without creating another competitor database.

## Run When
Run when a human/agent needs the current competitive state for planning, sales, marketing, SEO, or strategy.

## Process
1. [DETERMINISTIC] Resolve canonical Competitor, current facts, recent changes, and active Insights.
2. [AI] Summarize products/offers/pricing/positioning/audience, major strengths/weaknesses, current moves, and known customer sentiment.
3. [AI] Separate current fact, strategic inference, and unresolved unknowns visibly.
4. [DETERMINISTIC] Include freshness/review dates and the source/evidence refs behind material claims.
5. [AI] Highlight only implications relevant to the requesting context rather than dumping all intelligence.
6. [AI] Note material changes since the previous brief and what is being monitored.
7. [DETERMINISTIC] Produce a reusable Asset that references canonical objects rather than copying them as new truth.
