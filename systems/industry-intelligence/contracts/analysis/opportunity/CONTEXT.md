---
id: industry.analysis.opportunity
type: playbook
owner_system: industry-intelligence
reads:
- IndustryEvent
- Observation
- SourceRecord
- Insight
writes:
- IndustryEvent
- Observation
- Insight
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - news.read
  - regulatory.read
  - research.paper.read
  - market_data.read
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# External Opportunity Analysis

## Purpose
Identify business upside created by an industry development without claiming another domain owns the response.

## Business Outcome
Improve the business response to external change through timely, evidence-backed external opportunity analysis.

## Run When
Run when a decision or monitoring signal requires current external opportunity analysis and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Define what changed and which customer/business outcome could improve because of it.
2. [HYBRID] Test customer relevance, competitive availability, timing window, business capability/credibility, and economic significance.
3. [AI] Identify multiple plausible response domains and distinguish content/news relevance from durable strategic opportunity.
4. [HYBRID] Estimate opportunity range, confidence, urgency, dependencies, and disconfirming evidence.
5. [DETERMINISTIC] Publish Industry Insight and let each domain evaluate independent Opportunities.
