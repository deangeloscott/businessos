---
id: industry.analysis.trend-validation
type: playbook
owner_system: industry-intelligence
reads:
- IndustryEvent
- SourceRecord
- Observation
- Insight
writes:
- IndustryEvent
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - rss.read
  - regulatory.read
  - research.paper.read
  - market_data.read
  - social.listen
  - webpage.snapshot
  - webpage.compare
  - alert.read
context:
- Business
- Market
- Objective
---
# Industry Trend Validation

## Purpose
Determine whether a perceived trend reflects a sustained underlying change rather than repeated coverage, seasonality, or a short-lived spike.

## Business Outcome
Surface actionable market trends without converting attention cycles into false strategic certainty.

## Run When
Run when monitoring suggests a recurring or accelerating industry/category behavior or narrative.

## Process
1. [DETERMINISTIC] Define the proposed trend, measure, baseline period, geography/population, and earliest observed change.
2. [AI] Gather independent evidence streams rather than counting syndicated articles or reposted claims as independent support.
3. [DETERMINISTIC] Compare magnitude, persistence, rate of change, seasonality, and historical variance where data exists.
4. [AI] Test competing explanations including one-off events, platform changes, sampling shifts, measurement changes, and media amplification.
5. [AI] Identify who/where the trend applies and counterexamples where it does not.
6. [HYBRID] Classify as signal, emerging trend, established trend, uncertain, or contradicted based on evidence—not excitement.
7. [AI] Define indicators/review date and publish a scoped Industry Insight only when warranted.
