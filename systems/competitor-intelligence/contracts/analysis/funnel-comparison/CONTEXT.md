---
id: competitor.analysis.funnel-comparison
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
# Competitor Funnel Comparison

## Purpose
Compare observed competitor funnels by customer path, persuasion, friction, qualification, and offer transition.

## Business Outcome
Identify transferable competitive lessons and whitespace without copying surface tactics.

## Run When
Run after comparable competitor funnel captures exist.

## Process
1. [DETERMINISTIC] Align funnels to comparable entry intent, audience, and desired commercial action.
2. [AI] Compare path length, message continuity, proof, education, qualification, offer timing, friction, risk reversal, and follow-up.
3. [AI] Separate differences caused by business model or traffic source from potentially transferable mechanisms.
4. [AI] Identify where competitor choices appear to optimize for different customer quality, economics, or sales motion.
5. [HYBRID] Require performance/customer evidence before claiming a funnel is better merely because it is sophisticated.
6. [AI] Extract testable mechanism hypotheses and competitive whitespace relevant to this business.
7. [AI] Route Marketing/Customer Optimization implications without creating those Opportunities inside Competitor Intelligence.
