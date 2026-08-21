---
id: competitor.analysis.strength-weakness
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 2
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - review.read
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Strength and Weakness Assessment

## Purpose
Synthesize evidence into scoped competitive strengths and weaknesses tied to customer and business context.

## Business Outcome
Create useful competitive interpretation rather than generic SWOT labels.

## Run When
Run after sufficient competitor/customer evidence exists or when a strategic comparison must be refreshed.

## Process
1. [AI] Define the customer scenario, market, and objective against which strength/weakness is being judged.
2. [AI] Gather supported evidence across offer, product/service, customer sentiment, distribution, funnel, search, proof, operations, and strategic movement.
3. [AI] Distinguish structural strengths from temporary tactics and advertised claims from observed/customer-supported advantages.
4. [AI] Identify where an apparent strength creates tradeoffs or where a weakness is irrelevant to target customers.
5. [HYBRID] Test alternative explanations and contrary evidence before final classification.
6. [AI] Scope each assessment by audience/market/time and assign confidence/evidence links.
7. [AI] Publish Insights and whitespace/threat signals; downstream systems decide intervention.
