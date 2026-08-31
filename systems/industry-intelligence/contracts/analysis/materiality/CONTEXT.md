---
id: industry.analysis.materiality
type: playbook
version: 1.3.0
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
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - news.read
  - regulatory.read
  - research.paper.read
  - market_data.read
events:
  consumes:
  - none
  emits:
  - industry.insight.updated
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
subcontracts:
  conditional:
  - id: industry.analysis.impact-pathway
    when: materiality depends on a multi-step causal pathway
---
# Materiality Assessment

## Purpose
Determine whether an external development is important enough to change business attention or decisions.

## Business Outcome
Improve the business response to external change through timely, evidence-backed materiality assessment.

## Run When
Run when a decision or monitoring signal requires current materiality assessment and existing Industry Intelligence is missing, stale, or unresolved.

## Process
1. [AI] Identify affected markets, audiences, products, capabilities, economics, compliance, channels, competitors, and timelines.
2. [HYBRID] Assess magnitude, probability, timing, persistence, reversibility, uncertainty, and proximity to active Objectives.
3. [AI] Distinguish direct operational effect, customer-behavior effect, competitive effect, narrative/content relevance, and speculative second-order effect.
4. [HYBRID] Compare against configured materiality thresholds and current portfolio priorities.
5. [AI] Generate alternative interpretations and what evidence would change the assessment.
6. [HYBRID] Set relevance/urgency/confidence and affected-domain candidates; do not prescribe each domain response.
7. [DETERMINISTIC] Emit material Industry Insight only when threshold is met.
