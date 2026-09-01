---
id: industry.monitoring.research
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
  - research.paper.read
  optional:
  - research.web.read
  - news.read
  - alert.read
  - market_data.read
  - rss.read
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
# Research Evidence Review

## Purpose
Find and evaluate credible research that could materially change customer, product, market, operational, or strategy assumptions.

## Business Outcome
Give the organization reusable evidence-backed understanding of relevant research without turning AURA into a background literature-monitoring service.

## Run When
Use when a current decision or saved monitoring intent needs current research evidence and existing organizational knowledge may be stale, incomplete, contradictory, or unresolved. Any recurring execution is owned by the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve the smallest useful set of relevant peer-reviewed, preprint, standards, government, or credible institutional research using the host's available capabilities. Prefer primary research when the decision depends on study findings.
2. [AI] Extract the research question, population/data, method, main result, limitations, effect size where meaningful, and the authors' stated conclusions without upgrading claims beyond the source.
3. [HYBRID] Evaluate evidence strength, replication/independence, external validity, measurement quality, freshness, and applicability. Publication status alone is not proof of truth or relevance.
4. [AI] Compare the evidence with existing organizational Insights/Learnings and materially contradictory research when that comparison affects the current decision.
5. [AI] Judge whether the research changes a material assumption, creates a useful hypothesis, narrows uncertainty, or has no decision-relevant implication for this organization.
6. [HYBRID] Persist SourceRecords/Observations and an Insight only when the evidence has durable organizational value. Preserve limitations and applicability explicitly; do not automatically create an Opportunity, content task, or downstream route from a paper/report.
7. [AI] When future review matters because evidence is likely to mature or a study/standard is pending, preserve semantic recheck intent. The active harness/runtime owns any actual recurring search or notification.

## Verification
- Study claims and limitations remain faithful to the source.
- Evidence strength and business applicability are separate judgments.
- Contradictory or inconclusive evidence remains visible when material.
- Saved review intent does not claim an active schedule exists.

## Completion Criteria
- The organization has the smallest useful current research evidence for the decision, with durable findings preserved only where future work benefits.
