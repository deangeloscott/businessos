---
id: competitor.research.adaptive-source-coverage
type: playbook
version: 1.7.0
owner_system: competitor-intelligence
risk: low
autonomy_ceiling: 3
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.fetch
  - webpage.snapshot
  - browser.interact
  - crawler.run
  - advertising.observe
  - social.observe
  - review.read
  - community.read
  - news.read
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
references:
- systems/competitor-intelligence/references/source-coverage.json
---
# Adaptive Competitive Source Coverage

## Purpose
Achieve decision-appropriate competitive evidence coverage without forcing every research run through the same fixed list of websites or allowing shallow model discretion to declare research complete too early.

## Business Outcome
Make competitive conclusions more complete, reproducible, and efficient while preserving the agent's ability to discover useful sources and signals not anticipated by the BusinessOS.

## Run When
Run as part of substantial competitor research, comprehensive audits, priority competitor onboarding, or whenever current evidence coverage is unclear.

## Process
1. [AI] Select/inherit depth: **Rapid**, **Standard**, **Comprehensive**, or **Continuous**. Tie depth to the business decision, time sensitivity, risk, requested thoroughness, and what additional evidence could realistically change the action.
2. [AI] Evaluate the relevant evidence classes in the source-coverage reference. Treat named platforms/sites as examples, not an exhaustive whitelist; add credible sources discovered during research when they have material decision value.
3. [HYBRID] For each relevant class, choose the strongest accessible sources by authority, directness, freshness, identity confidence, and expected information gain. Mark irrelevant/unavailable/blocked sources instead of fabricating completeness.
4. [INTEGRATION] Collect evidence from the selected sources using the narrowest appropriate capability. When a high-signal source reveals a material theme, campaign, funnel, complaint, release, or strategic change, deepen that branch rather than mechanically exhausting low-value sources.
5. [AI] Continuously test coverage for contrary evidence, snapshot bias, platform bias, regional gaps, stale data, and competing explanations. Use domain owners such as SEO/AEO for deep specialist analysis rather than duplicating their canonical intelligence.
6. [DETERMINISTIC] Maintain a coverage Observation recording evidence class, specific sources checked, status (`checked`, `partial`, `not_relevant`, `unavailable`, `blocked`, `deferred`, `unknown`), freshness, important gaps, and why deeper research was or was not warranted.
7. [AI] Stop when required depth is satisfied and additional accessible evidence is unlikely to change the decision enough to justify its cost/time. For Comprehensive work, explicitly report material uncovered gaps; for Continuous work, reuse the baseline and focus on changed/high-value areas.

## Verification
The resulting decision can show what evidence classes/sources were considered, which were materially checked, where coverage is incomplete, and why research stopped, without pretending the source examples define the universe of possible evidence.
