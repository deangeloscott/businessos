---
id: competitor.discovery.competitive-set
type: playbook
version: 1.8.0
owner_system: competitor-intelligence
reads:
- type: Insight
  owner_system: customer-intelligence
- Competitor
- SourceProfile
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
  - local_profile.read
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
Identify actual direct, substitute, emerging, attention, and decision-specific benchmark competitors relevant to defined business decisions.

## Business Outcome
Improve competitive decisions through evidence-backed competitor discovery and contextually relevant comparison sets, without mistaking observed activity for proven effectiveness or famous category players for direct competitors.

## Run When
Run when a decision requires current competitor discovery and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [AI] Define the competitive question, audience/customer job, market/geography, offer/category, channel/discovery surface, scale/market-position relevance, and time horizon before searching.
2. [INTEGRATION] Gather candidates from customer alternatives, win/loss evidence, local/search/category results, review platforms, marketplaces, analyst/category sources, known business context, and existing resolved SourceProfiles.
3. [AI] Classify each candidate by the role it plays for this decision: direct, substitute, emerging, budget/status-quo, aspirational/category benchmark, attention/content, search/local-surface, or another explicitly justified role.
4. [HYBRID] Exclude entities that merely share keywords, geography, or fame but do not meaningfully inform the relevant customer/business outcome unless their benchmark role is explicit.
5. [HYBRID] Rank decision relevance using customer overlap, offer/category overlap, geography/service area, observed consideration frequency, scale/stage, market position, business model, channel/surface overlap, and strategic relevance. Do not collapse these into one universal competitor score.
6. [HYBRID] Use `competitor.discovery.entity-resolution` to resolve/create one canonical Competitor record per true competitor and preserve evidence-backed domains, aliases, and public profiles. Reuse shared SourceProfile subject grouping where available; do not merge namesakes or ambiguous identities.
7. [AI] Create comparison cohorts appropriate to the question and state what each cohort is intended to teach. For local search/map-pack questions, prioritize the actual local discovery set; for strategic/category questions, broader or aspirational benchmarks may be appropriate.
8. [HYBRID] Mark uncertainty and schedule deeper profiling only for material candidates.
