---
id: competitor.analysis.strategy-hypothesis
type: playbook
version: 1.3.0
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
capabilities:
  required:
  - research.web.read
  optional:
  - webpage.snapshot
  - webpage.compare
  - advertising.observe
  - social.observe
  - review.read
  - search.observe
  - document.read
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Strategy Hypothesis

## Purpose
Infer a competitor’s likely strategic direction from multiple observable changes while preserving uncertainty.

## Business Outcome
Help the business anticipate competitor movement without presenting inference as known internal strategy.

## Run When
Run when a sequence of competitor changes suggests a material strategic shift.

## Process
1. [DETERMINISTIC] Assemble dated changes in products, pricing, packaging, messaging, hiring, partnerships, distribution, content, and market focus.
2. [AI] Identify patterns that could be explained by a coherent strategic objective.
3. [AI] Generate at least one plausible alternative explanation and evidence that would distinguish them.
4. [AI] State the primary strategy hypothesis, supporting/contradicting evidence, scope, and confidence.
5. [AI] Define observable predictions that should occur if the hypothesis is correct.
6. [HYBRID] Avoid claims about private intent, finances, or plans beyond observable evidence.
7. [DETERMINISTIC] Schedule monitoring of discriminating signals and update/contradict the Insight when evidence changes.
