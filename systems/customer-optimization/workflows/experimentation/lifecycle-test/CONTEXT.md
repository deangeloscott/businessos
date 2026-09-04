---
id: customer-optimization.experimentation.lifecycle-test
type: workflow
owner_system: customer-optimization
reads:
- Opportunity
- CustomerJourney
- MetricDefinition
- Learning
writes:
- Experiment
---
# Lifecycle Experiment Design

## Purpose
Design an interpretable test of a customer-journey intervention while protecting customer outcomes and business guardrails and, when actually requested, run it through the active harness.

## Business Outcome
Improve customer progression and value realization through defensible evidence rather than treating a plausible intervention or one observed improvement as causal truth.

## Run When
Use when journey evidence suggests a material intervention hypothesis and a bounded experiment can improve the decision. An Opportunity may provide durable context but is not required merely to design the test.

## Process
1. [AI] State the diagnosed friction, intervention mechanism, target journey transition, eligible population, and customer/business decision the test should inform.
2. [HYBRID] Choose a randomized/control design or the strongest feasible quasi-experimental comparison; keep the treatment difference as narrow as practical and identify contamination/spillover risks.
3. [HYBRID] Predefine the primary progression metric, downstream value metric, guardrails, sample/window assumptions, stopping rules, and planned segment analysis appropriate to the actual setting.
4. [HYBRID] Check customer harm, fairness, compliance, service capacity, reversibility, and interpretation risks before execution.
5. [DETERMINISTIC] Persist the Experiment before observing results when durable experiment state will materially help future interpretation or continuity. Do not require an Action, approval object, or internal execution lifecycle.
6. [INTEGRATION] If running the experiment is inside the user's current request and the active harness has the necessary real system access, implement the bounded assignment/treatment through that system. Otherwise preserve the complete design and create a genuine durable handoff only when another actor needs to execute it; do not manufacture manual procedures or an AURA fallback merely because execution is unavailable now.
7. [HYBRID] Verify treatment delivery and measurement state when needed for valid interpretation. Use observed results with the relevant OutcomeEvaluation and Learning methods directly; do not route data through an internal AURA chain or treat launch as success.

## Verification
- The design can answer the stated customer/business question at the confidence claimed.
- Treatment, comparison, metrics, guardrails, stopping rules, and interpretation limits are explicit.
- Any claimed execution is grounded in actual host/system state rather than AURA bookkeeping.

## Completion Criteria
- A defensible Experiment/design exists, and any execution or outcome claim remains bounded by observed evidence without a fabricated authorization, fallback, routing, or lifecycle layer.
