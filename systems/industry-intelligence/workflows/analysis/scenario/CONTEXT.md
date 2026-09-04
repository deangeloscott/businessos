---
id: industry.analysis.scenario
type: workflow
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
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Scenario Analysis

## Purpose
Model materially different plausible futures when uncertainty is too high for one-point prediction.

## Business Outcome
Improve the business response to external change through timely, evidence-backed scenario analysis.

## Run When
Run when a decision or monitoring signal requires current scenario analysis and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Define the focal uncertainty and decision horizon; choose only uncertainties that would materially alter action.
2. [HYBRID] Identify key drivers, current evidence, dependencies, and plausible bounded states for each driver.
3. [AI] Construct a small set of internally coherent scenarios rather than combinatorial permutations.
4. [AI] For each scenario state observable indicators, affected business assumptions, risks/opportunities, and decisions that would change.
5. [HYBRID] Identify robust actions that perform acceptably across scenarios versus contingent actions requiring triggers.
6. [DETERMINISTIC] Record monitoring indicators and trigger thresholds without assigning probabilities not supported by evidence.
