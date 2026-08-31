---
id: customer-optimization.experimentation.lifecycle-test
type: playbook
version: 1.1.0
owner_system: customer-optimization
reads:
- Opportunity
- CustomerJourney
- MetricDefinition
- Learning
writes:
- Experiment
capabilities:
  required:
  - none
  optional:
  - experiment.run
  - analytics.read
  - product_analytics.read
---
# Lifecycle Experiment Design

## Purpose
Test a customer-journey intervention while protecting customer outcomes and business guardrails.

## Business Outcome
Improve customer progression and value realization through lifecycle experiment design, while protecting customer and business guardrails.

## Run When
Run when journey evidence or an active Opportunity requires lifecycle experiment design to improve a defined customer transition or outcome.

## Process
1. [AI] State diagnosed friction, intervention mechanism, target journey transition, eligible population, and expected customer/business effect.
2. [HYBRID] Select controlled/randomized or strongest feasible quasi-experimental design; identify contamination/spillover risks.
3. [DETERMINISTIC] Predefine primary progression metric, downstream value metric, guardrails, sample/window, stopping rules, and segment analysis.
4. [HYBRID] Check fairness, customer harm, compliance, service capacity, and reversibility.
5. [INTEGRATION] Implement assignment/treatment when authorized or create manual procedures.
6. [DETERMINISTIC] Verify treatment delivery and instrumentation before interpreting outcomes.
7. [HYBRID] Route final data through OutcomeEvaluation and domain Learning.
