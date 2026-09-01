---
id: industry.analysis.research-quality
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
# Industry Research Quality Assessment

## Purpose
Evaluate whether a study, report, benchmark, or dataset supports the conclusion being considered.

## Business Outcome
Prevent weak methodology or overgeneralized research from driving business decisions.

## Run When
Run when external research materially supports an Industry Insight or recommendation.

## Process
1. [AI] Identify research question, population/sample, data source, design, comparison/control, period, measures, and analysis.
2. [AI] Evaluate representativeness, selection, measurement, confounding, missing data, statistical/causal claims, and sponsor/incentive issues.
3. [DETERMINISTIC] Verify reported figures and definitions against the primary report/data where available.
4. [AI] Separate what the study measured from what commentary claims it proves.
5. [AI] Test applicability to this business’s market/audience/context and identify extrapolations.
6. [HYBRID] Grade confidence in each decision-relevant claim rather than issuing one blanket “credible/not credible” label.
7. [AI] Publish evidence-quality Observations and constrain downstream Insight scope accordingly.
