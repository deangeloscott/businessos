---
id: competitor.analysis.offer-comparison
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
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
# Competitor Offer Comparison

## Purpose
Compare what customers actually receive, risk, commit to, and must do across competing offers.

## Business Outcome
Reveal meaningful competitive offer differences rather than comparing headline price alone.

## Run When
Run when pricing, packaging, positioning, or sales decisions require a competitive offer comparison.

## Process
1. [AI] Define the customer job, audience, and comparable buying scenario before selecting offers.
2. [DETERMINISTIC] Gather price-normalized commercial facts, included deliverables, limits, implementation, support, terms, guarantees, trial, and bonuses where public.
3. [AI] Separate factual offer components from inferred value or quality.
4. [AI] Compare customer effort, risk, time-to-value, flexibility, switching cost, and proof required.
5. [AI] Identify advantages, disadvantages, and non-comparable dimensions by scenario rather than declaring one universal winner.
6. [HYBRID] Cross-check with customer evidence about which differences actually affect decisions.
7. [AI] Publish competitive Insights/whitespace with explicit evidence and scope.
