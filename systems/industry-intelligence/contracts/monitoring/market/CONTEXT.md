---
id: industry.monitoring.market
type: playbook
owner_system: industry-intelligence
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
  - market_data.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
context:
- Business
- Market
- Objective
- ProductService
---
# Market & Category Monitoring

## Purpose
Detect structural category/economic shifts relevant to demand, supply, pricing, customer behavior, or competitive conditions.

## Business Outcome
Improve the business response to external change through timely, evidence-backed market & category monitoring.

## Run When
Run when a decision or monitoring signal requires current market & category monitoring and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [INTEGRATION] Retrieve configured market/category indicators and authoritative contextual sources.
2. [DETERMINISTIC] Validate definitions, units, revisions, geography, seasonality, and comparable periods before calculating change.
3. [AI] Relate indicator changes to plausible customer/business mechanisms without assuming causality.
4. [HYBRID] Combine quantitative movement with corroborating customer/competitor/industry observations.
5. [AI] Identify affected audiences, products, markets, economics, and potential threat/opportunity.
6. [HYBRID] Publish scoped Insight when evidence is materially decision-relevant; otherwise maintain as Observation/watch.
