---
id: industry.analysis.impact-pathway
type: workflow
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
context:
- Business
- Market
- Objective
---
# Industry Impact Pathway Analysis

## Purpose
Trace how an external development could cause concrete effects on customers, competitors, operations, economics, compliance, or discovery.

## Business Outcome
Turn broad “this matters” claims into explicit mechanisms that can be monitored and acted on.

## Run When
Run after a material Event needs business impact interpretation.

## Process
1. [AI] Start from verified factual change and list directly affected actors, rules, technologies, costs, behaviors, or constraints.
2. [AI] Map first-order effects and then only plausible second-order effects with explicit assumptions.
3. [AI] Connect each pathway to affected Markets, AudienceSegments, Products/Services, Offers, competitors, operations, or channels.
4. [AI] Identify leading indicators and observable evidence that would confirm or falsify each pathway.
5. [HYBRID] Separate likely, possible, and speculative effects; avoid collapsing scenario branches into one prediction.
6. [AI] Estimate timing, magnitude range, reversibility, and decision urgency where evidence permits.
7. [AI] Publish Industry Insights/relevance signals and monitoring requirements rather than foreign-domain Opportunities.
