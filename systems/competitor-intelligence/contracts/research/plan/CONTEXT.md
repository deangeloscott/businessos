---
id: competitor.research.plan
type: playbook
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
  - browser.interact
  - crawler.run
  - community.read
  - news.read
context:
- Business
- Market
- AudienceSegment
- Offer
subcontracts:
  required:
  - competitor.research.adaptive-source-coverage
---
# Competitor Research Plan

## Purpose
Turn a competitive decision or uncertainty into an adaptive, bounded research plan with explicit depth and evidence-coverage expectations.

## Business Outcome
Collect enough competitive evidence to make the decision well without either shallow research or unnecessary exhaustive collection.

## Run When
Run before substantial competitor research when scope, competitor set, depth, evidence, or stopping conditions are not explicit.

## Process
1. [AI] State the competitive decision, current hypothesis, affected market/audience/offer, and what evidence could change the decision.
2. [AI] Select research depth: **Rapid** for a narrow answer, **Standard** for normal competitive analysis, **Comprehensive** for broad strategic due diligence/audit, or **Continuous** for monitoring from an existing baseline. Infer from the request unless the user specifies depth.
3. [AI] Define the competitor set including direct, substitute, emerging, and relevant category benchmarks; do not assume the supplied list is complete.
4. [AI] Identify fact/evidence classes needed: product, price, packaging, offer, positioning, funnel, content/social, advertising, customer/public sentiment, releases, strategic signals, independent corroboration, or specialist domain evidence.
5. [HYBRID] Use `competitor.research.adaptive-source-coverage` to choose decision-relevant sources and coverage; examples in the source registry guide discovery but do not limit it.
6. [AI] Specify historical comparison, contrary evidence, customer evidence, identity-resolution needs, and competing explanations needed to avoid snapshot-only conclusions.
7. [DETERMINISTIC] Define freshness, coverage, stopping, output, and unresolved-gap requirements; reuse current canonical competitor intelligence and collect only material gaps.

## Verification
The plan makes research depth, evidence classes, coverage expectations, and stopping logic explicit while leaving room for the agent to discover higher-value sources.
