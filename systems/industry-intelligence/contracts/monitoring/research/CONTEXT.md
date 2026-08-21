---
id: industry.monitoring.research
type: playbook
version: 1.3.0
owner_system: industry-intelligence
risk: low
autonomy_ceiling: 4
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
- Insight
capabilities:
  required:
  - research.paper.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
  - rss.read
events:
  consumes:
  - none
  emits:
  - industry.event.updated
schedule:
  class: recurring
  default: weekly
  configurable: true
context:
- Business
- Market
- Objective
- ProductService
subcontracts:
  conditional:
  - id: industry.analysis.research-quality
    when: a study/report materially supports an Insight
---
# Research Monitoring

## Purpose
Identify credible new research that could change customer, product, market, or strategy assumptions.

## Business Outcome
Improve the business response to external change through timely, evidence-backed research monitoring.

## Run When
Run when a decision or monitoring signal requires current research monitoring and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [INTEGRATION] Retrieve new prioritized peer-reviewed/preprint/standards/credible institutional research with metadata.
2. [AI] Extract research question, population/data, method, main result, limitations, effect size where meaningful, and authors stated conclusions.
3. [HYBRID] Distinguish evidence strength, replication status, external validity, and business applicability; do not equate publication with truth.
4. [AI] Compare with existing Industry/Business Learnings and contradictory research.
5. [HYBRID] Assess whether the result changes a material assumption, threat, opportunity, customer concern, or content need.
6. [DETERMINISTIC] Publish SourceRecord/Observation/Insight with research limitations preserved.
