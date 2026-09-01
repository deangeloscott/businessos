---
id: customer.learning.domain-learning
type: playbook
owner_system: customer-intelligence
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
# Customer Intelligence Learning

## Purpose
Improve which customer evidence sources, methods, segment scopes, and assumptions produce reliable customer understanding.

## Business Outcome
Reduce uncertainty about customers through customer intelligence learning, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run during periodic learning cycles or after sufficient OutcomeEvaluations/corrections accumulate.

## Process
1. [AI] Review Customer Insights that were strengthened, contradicted, narrowed, or repeatedly corrected and the methods/sources that produced them.
2. [HYBRID] Identify method/source conditions associated with reliable versus misleading conclusions without generalizing from one study.
3. [AI] Capture stable customer-domain lessons such as source coverage needs, segment differences, question effects, or recurring evidence gaps.
4. [HYBRID] Keep customer truths as Insights; record methodological/decision guidance as Customer Intelligence Learning.
5. [DETERMINISTIC] Promote/deprecate Learning under Core maturity rules and preserve applicability.
