---
id: industry.analysis.narrative-vs-fact
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
# Industry Narrative vs Fact Analysis

## Purpose
Separate what is objectively changing from what the market is repeatedly saying or believing about it.

## Business Outcome
Let the business respond appropriately to influential narratives without confusing popularity with factual truth.

## Run When
Run when an industry topic is highly discussed, polarized, or framed more strongly than available evidence supports.

## Process
1. [AI] Extract the major recurring narratives/claims and the audiences/sources spreading them.
2. [DETERMINISTIC] Link each factual component to verified evidence and mark unsupported/disputed components.
3. [AI] Measure/describe narrative prevalence separately from factual confidence.
4. [AI] Identify incentives, frames, terminology, and emotional/customer implications influencing the narrative.
5. [HYBRID] Allow the conclusion “narrative is influential even though factual support is weak” when evidence supports perception impact.
6. [AI] Identify business/customer risks from both the factual situation and the perception situation.
7. [AI] Publish distinct Insights for fact/impact versus narrative/perception when both matter.
