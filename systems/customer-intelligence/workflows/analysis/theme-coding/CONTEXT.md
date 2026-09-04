---
id: customer.analysis.theme-coding
type: workflow
owner_system: customer-intelligence
reads:
- Observation
writes:
- Insight
context:
- AudienceSegment
- Objective
---
# Customer Theme Coding

## Purpose
Group customer evidence into stable, interpretable themes without losing contradictory or segment-specific meaning.

## Business Outcome
Turn many observations into comparable evidence structures that support reliable customer Insights.

## Run When
Run when a body of customer Observations is large enough that recurring patterns must be compared systematically.

## Process
1. [AI] Review the research question and existing theme taxonomy; do not reuse categories that no longer fit the evidence.
2. [AI] Open-code a representative subset to identify recurring concepts, language, causes, outcomes, and exceptions.
3. [AI] Define theme boundaries and inclusion/exclusion rules so similar-but-different concepts are not merged.
4. [HYBRID] Recode the wider evidence set and inspect ambiguous/multi-theme cases rather than forcing one label.
5. [DETERMINISTIC] Count coverage by source, segment, journey stage, and outcome while keeping frequency separate from importance.
6. [AI] Identify co-occurrence, contradictions, and negative cases that change the interpretation.
7. [AI] Produce theme summaries with supporting Observation refs and clear scope; route candidate Insights to insight validation.
