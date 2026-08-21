---
id: industry.analysis.competitor-response
type: playbook
version: 1.3.0
owner_system: industry-intelligence
risk: low
autonomy_ceiling: 2
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
# Industry Event Competitor Response Analysis

## Purpose
Track how material competitors respond to an external Event without duplicating canonical competitor strategy.

## Business Outcome
Use competitor response as evidence of event impact while preserving Competitor Intelligence ownership.

## Run When
Run when a material IndustryEvent is likely to force or incentivize competitor changes.

## Process
1. [DETERMINISTIC] Resolve affected canonical Competitors and the specific Event implications relevant to them.
2. [INTEGRATION] Monitor public competitor actions/communications tied to the Event and capture dated Observations.
3. [AI] Separate direct Event response from unrelated concurrent changes.
4. [AI] Compare response timing/types across competitors and identify common versus differentiated behavior.
5. [HYBRID] Avoid inferring internal motives beyond observable evidence; publish competitor Observations to Competitor Intelligence.
6. [AI] Use response patterns as contextual evidence for Event impact and scenario updates.
7. [DETERMINISTIC] End special monitoring when response window closes or fold it into normal competitor monitoring.
