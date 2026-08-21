---
id: industry.handoff.decision-brief
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
# Industry Decision Brief

## Purpose
Package the minimum verified facts, implications, uncertainty, deadlines, and decision relevance needed by a downstream domain.

## Business Outcome
Let downstream systems act on Industry Intelligence without rereading the whole news/research history.

## Run When
Run when a material Industry Insight must be consumed by Content, Marketing, Customer, Competitor, SEO, or Customer Optimization.

## Process
1. [DETERMINISTIC] Resolve the IndustryEvent, factual summary, active Insight, impact pathway, and relevant business context.
2. [AI] State what changed, why it matters to this specific downstream decision, affected audience/market/product/offer, and timing.
3. [AI] Separate facts, interpretation, scenarios, and unresolved uncertainty visibly.
4. [AI] Include the “so what” and potential protect/benefit actions as implications, not as foreign-domain prescriptions.
5. [DETERMINISTIC] Include source/evidence refs, freshness, deadlines, and conditions that would change the brief.
6. [AI] Keep only information relevant to the receiving system and create a WorkRequest when actual delegated work is required.
7. [DETERMINISTIC] Link the brief/WorkRequest to the originating Event/Insight for outcome traceability.
