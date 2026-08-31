---
id: core.measurement.design-experiment
type: playbook
version: 2.0.0
owner_system: core
reads:
- Opportunity
- MetricDefinition
- Learning
- DecisionRecord
writes:
- Experiment
capabilities:
  required:
  - none
  optional:
  - none
---
# Design Experiment

## Purpose
Design a disciplined experiment when causal learning would materially improve a business decision.

## Business Outcome
Increase causal confidence without turning experiment design into a generic execution-control lifecycle.

## Run When
When causal learning matters and a feasible, ethical test can improve confidence beyond observational comparison.

## Process
1. [AI] State the intervention hypothesis, mechanism, eligible population, and decision the experiment must inform.
2. [HYBRID] Choose randomized/control, switchback, holdout, matched, interrupted-time-series, or another defensible design based on the actual setting and interference risk.
3. [DETERMINISTIC] Predefine treatment/control or baseline, primary metric, guardrails, sample/window, stopping rule, exclusions, and planned segment analyses where material.
4. [HYBRID] Identify contamination, novelty, selection, seasonality, network effects, ethical constraints, and other threats to interpretation.
5. [HYBRID] Record real business/legal/platform/customer constraints that affect the experiment. Do not create AURA authority tiers or permission objects.
6. [DETERMINISTIC] Persist the Experiment before observing results. Execution is performed by the active model/harness or another real owner using its actual tools and constraints.
7. [HYBRID] Persist a DecisionRecord only when the organization makes a material decision about whether/how to run, change, stop, or adopt the experiment and future work benefits from remembering it.

## Verification
- The design can answer the stated decision question at an appropriate level of confidence.
- Outcome and implementation evidence remain distinct.
- Constraints and causal limitations are explicit rather than hidden in an execution packet.

## Completion Criteria
- A schema-valid Experiment contains the minimum information needed to run and later interpret the test without requiring an ActionPacket or generic approval lifecycle.
