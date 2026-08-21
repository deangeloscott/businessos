---
id: core.measurement.design-experiment
type: playbook
version: 1.1.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Opportunity
- MetricDefinition
- Learning
writes:
- Experiment
- ActionPacket
capabilities:
  required:
  - none
  optional:
  - none
---
# Design Experiment

## Purpose
Provide a shared disciplined experiment contract while allowing domains to define their intervention and mechanism.

## Business Outcome
Increase causal confidence when an important decision can be tested safely and the expected learning is worth the experiment.
## Run When
When causal learning matters and a test is feasible/ethical enough to improve confidence beyond observational comparison.

## Process
1. [AI] State the intervention hypothesis, mechanism, eligible population, and decision the experiment must inform.
2. [HYBRID] Choose randomized/control, switchback, holdout, matched, interrupted-time-series, or other valid design based on interference and feasibility.
3. [DETERMINISTIC] Predefine treatment/control or baseline, primary metric, guardrails, sample/window, stopping rule, exclusions, and planned segment analyses.
4. [HYBRID] Identify contamination, novelty, selection, seasonality, network, and operational risks.
5. [HYBRID] Confirm ethical/compliance/customer constraints and effective autonomy/approval.
6. [DETERMINISTIC] Persist Experiment and execution actions before observing results.
