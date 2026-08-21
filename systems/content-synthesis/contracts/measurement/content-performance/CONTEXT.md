---
id: content.measurement.content-performance
type: playbook
version: 1.1.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Asset
- MetricObservation
- Opportunity
- WorkRequest
- Learning
writes:
- Insight
- Learning
- OutcomeEvaluation
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - social.observe
  - marketing.performance.read
---
# Content Performance Learning

## Purpose
Interpret content response in the context of platform, format, audience, objective, and distribution rather than one universal engagement score.

## Business Outcome
Create or improve content performance learning so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires content performance learning and existing Assets do not already satisfy the communication need.

## Process
1. [DETERMINISTIC] Retrieve objective-linked metrics with platform, asset, audience/segment, distribution, and comparable time-window context.
2. [DETERMINISTIC] Validate tracking/data completeness and distinguish paid distribution or unusual exposure where relevant.
3. [HYBRID] Compare against appropriate baselines/peer assets and metrics matched to objective: qualified attention, completion, saves/shares, response, subscribers, clicks, assisted outcomes, etc.
4. [AI] Analyze topic/angle/format/hook/depth/platform hypotheses without claiming customer psychology from engagement alone.
5. [HYBRID] Identify confounders such as distribution, timing, creator/account growth, trend effects, or promotion.
6. [HYBRID] Publish Content Insight/Learning at appropriate scope and return measurement evidence to originating WorkRequest/Opportunity.
