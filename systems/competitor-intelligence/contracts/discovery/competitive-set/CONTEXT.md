---
id: competitor.discovery.competitive-set
type: playbook
version: 1.7.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 4
reads:
- type: Insight
  owner_system: customer-intelligence
- Competitor
writes:
- Competitor
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - crm.opportunity.read
  - review.read
  - search.observe
  - social.observe
  - advertising.observe
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - competitor.discovery.entity-resolution
---
# Competitor Discovery

## Purpose
Identify actual direct, substitute, emerging, and attention competitors relevant to defined business decisions.

## Business Outcome
Improve competitive decisions through evidence-backed competitor discovery, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor discovery and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [AI] Define the competitive question, audience, market, offer/category, and time horizon before searching.
2. [INTEGRATION] Gather candidates from customer alternatives, win/loss evidence, search/category results, review platforms, marketplaces, analyst/category sources, and known business context.
3. [AI] Classify each candidate as direct, substitute, emerging, budget/status-quo, or attention competitor with evidence.
4. [HYBRID] Exclude entities that merely share keywords but do not compete for the relevant customer/business outcome unless another domain needs them.
5. [HYBRID] Rank competitors by customer overlap, offer/category overlap, observed consideration frequency, and strategic relevance.
6. [HYBRID] Use `competitor.discovery.entity-resolution` to resolve/create one canonical Competitor record per entity and preserve evidence-backed domains, aliases, and public profiles; do not merge namesakes or ambiguous identities.
7. [HYBRID] Mark uncertainty and schedule deeper profiling only for material candidates.
