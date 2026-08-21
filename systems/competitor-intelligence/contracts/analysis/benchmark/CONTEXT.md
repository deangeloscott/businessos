---
id: competitor.analysis.benchmark
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
# Competitive Benchmark

## Purpose
Compare the business and competitors on decision-relevant dimensions using transparent measures.

## Business Outcome
Create interpretable benchmarks that show where the business is truly ahead, behind, or simply different.

## Run When
Run when a business decision needs a structured competitive comparison across several dimensions.

## Process
1. [AI] Define the decision and dimensions that matter to the target customer/business outcome.
2. [DETERMINISTIC] Resolve comparable observations/metrics and normalize units where legitimate.
3. [AI] Document missing/non-comparable dimensions rather than replacing them with arbitrary scores.
4. [DETERMINISTIC] Calculate individual comparisons and historical change using transparent formulas.
5. [HYBRID] Use a composite score only when weights have explicit decision meaning and preserve component values.
6. [AI] Interpret gaps in customer/strategic context and distinguish important gaps from vanity differences.
7. [AI] Publish benchmark Asset/Insights with assumptions, sources, and refresh date.
