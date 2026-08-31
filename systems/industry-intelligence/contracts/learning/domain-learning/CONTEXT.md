---
id: industry.learning.domain-learning
type: playbook
version: 1.1.0
owner_system: industry-intelligence
reads:
- OutcomeEvaluation
- Insight
- Learning
- MetricObservation
writes:
- Learning
capabilities:
  required:
  - none
  optional:
  - none
---
# Industry Intelligence Learning

## Purpose
Improve source coverage, materiality thresholds, event clustering, and response timing based on observed outcomes.

## Business Outcome
Improve the business response to external change through timely, evidence-backed industry intelligence learning.

## Run When
Run during periodic learning cycles or after sufficient OutcomeEvaluations/corrections accumulate.

## Process
1. [DETERMINISTIC] Review material events, non-material alerts, missed developments, timing, and downstream use.
2. [AI] Identify source classes/event types that reliably preceded material business effects.
3. [HYBRID] Calibrate relevance/urgency thresholds against false positives and missed high-impact events.
4. [AI] Capture context-specific patterns connecting external events to customer/competitor/channel effects.
5. [DETERMINISTIC] Update domain Learning without rewriting current IndustryEvent facts.
