---
id: competitor.analysis.competitive-implications
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
# Competitive Implication Analysis

## Purpose
Translate supported competitor changes and strengths/weaknesses into implications for this business without deciding foreign-domain actions.

## Business Outcome
Make competitive intelligence actionable while preserving semantic ownership of Marketing, SEO, Customer, Product, and other interventions.

## Run When
Run when a Competitor Insight is materially relevant to current objectives, offers, audiences, or risks.

## Process
1. [AI] Resolve the Competitor Insight and the business objectives/audiences/offers it could affect.
2. [AI] Identify potential threat, opportunity, customer-expectation, differentiation, pricing/offer, content, search, or journey implications.
3. [AI] Distinguish direct implication from speculative second-order effects and state assumptions.
4. [HYBRID] Check whether canonical Customer/Industry/SEO evidence supports or contradicts the implication.
5. [AI] Estimate urgency and reversibility based on observed competitor movement, not fear of competition.
6. [AI] Publish scoped Insight relationships/relevance signals to the correct downstream systems.
7. [DETERMINISTIC] Do not create foreign-domain Opportunities; record refresh triggers where the implication depends on future evidence.
