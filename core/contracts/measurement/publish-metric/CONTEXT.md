---
id: core.measurement.publish-metric
type: playbook
version: 1.8.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- MetricDefinition
- SourceRecord
writes:
- MetricObservation
capabilities:
  required:
  - none
  optional:
  - business.measurement.read
  - business.data.query
  - business.data.explain
---
# Publish Metric Observation

## Purpose
Create comparable metric observations from external or derived measurements using canonical definitions.

## Business Outcome
Make decision-relevant measurements comparable, traceable, and reusable across Opportunities, experiments, evaluations, and reporting.
## Run When
When a workflow needs a decision-relevant metric value for a subject and time window.

## Process
1. [DETERMINISTIC] Resolve the canonical MetricDefinition and required unit, dimensions, aggregation, and source expectations.
2. [INTEGRATION] Retrieve source data for the exact population/time window and preserve source reference/query definition. Prefer an authoritative governed business-data/measurement source when available; preserve its metric semantics, coverage, freshness, evidence class, and reason codes rather than recomputing an alternate truth in the model.
3. [DETERMINISTIC] Apply formula/aggregation exactly and retain denominator/sample where relevant.
4. [DETERMINISTIC] Validate dimensions, unit, window boundaries, missingness, and duplicate publication.
5. [HYBRID] Assign source quality/confidence when the metric is modeled/estimated rather than directly measured.
6. [DETERMINISTIC] Persist MetricObservation and emit metric.observed when thresholds/subscribers require it.
