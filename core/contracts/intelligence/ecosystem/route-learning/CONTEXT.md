---
id: core.intelligence.ecosystem.route-learning
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Objective
- Insight
- Learning
- Opportunity
- Experiment
- OutcomeEvaluation
writes:
- WorkRequest
- Opportunity
- Insight
capabilities:
  required:
  - none
  optional:
  - none
context:
- Business
- Objective
---
# Route External Evidence to Action or Learning

## Purpose
Turn a triangulated external finding into the smallest justified next state without confusing interesting evidence with authorization, business applicability, or proven causal value.

## Business Outcome
Focus BusinessOS on external findings worth watching, investigating, testing, or adopting while cheaply closing noise and avoiding premature implementation.

## Run When
Run after triangulation or domain interpretation produces a decision-relevant external Insight.

## Process
1. [DETERMINISTIC] Load the triangulated Insight, existing overlapping Opportunities/Learnings/Experiments, active Objective, and the canonical domain owner; reuse existing work before creating anything new.
2. [AI] Evaluate domain mechanism, active-business applicability, evidence independence/strength, freshness, novelty, causal ambiguity, policy status, reversibility, implementation cost/risk, and expected business/learning value.
3. [HYBRID] Choose one primary disposition: ignore, watch, investigate, test, adopt through an already-supported domain Learning/action path, or block/deprecate; use stronger thresholds as cost, harm, irreversibility, or policy risk rises.
4. [HYBRID] For `investigate`, create the smallest owner-domain WorkRequest that could resolve the uncertainty; for `test`, create/update a candidate Opportunity and route to the domain's existing experiment design rather than prescribing a universal experiment.
5. [HYBRID] For `adopt`, require evidence/maturity/applicability sufficient under Core/domain learning rules and normal authorization; external evidence alone never mutates customer-facing or operational state.
6. [AI] For `watch`, state the specific future evidence/change that would trigger re-evaluation and an appropriate freshness horizon; do not schedule it inside BusinessOS when the host lacks scheduling capability.
7. [DETERMINISTIC] Persist disposition, rationale, owner, evidence refs, and next-route refs so later cycles can resume incrementally and avoid reopening closed noise without new evidence.
8. [HYBRID] Route broad reusable conclusions to Core learning governance only when cross-domain/cross-context evidence supports that scope; otherwise keep the Learning with the narrowest valid domain/business owner.

## Verification
- Every expensive next step is justified by decision value and uncertainty reduction.
- No external finding bypasses semantic ownership, authorization, experiment, measurement, or Learning maturity rules.

## Completion Criteria
- The finding has exactly one current disposition, owner, rationale, and inspectable next state.
