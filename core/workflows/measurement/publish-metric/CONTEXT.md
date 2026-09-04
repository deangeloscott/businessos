---
id: core.measurement.publish-metric
type: workflow
owner_system: core
reads:
- MetricDefinition
- SourceRecord
writes:
- MetricObservation
---
# Publish Metric Observation

## Purpose
Create a comparable, evidence-linked metric observation from an authoritative or explicitly derived measurement without turning measurement into an internal event stream.

## Business Outcome
Make decision-relevant measurements comparable, traceable, and reusable across Opportunities, experiments, evaluations, and reporting.

## Run When
When current or future organizational work needs a durable metric value for a defined subject/population and time window.

## Process
1. [DETERMINISTIC] Resolve the MetricDefinition and its exact unit, dimensions, aggregation/formula, and source expectations where those mechanics are explicitly defined.
2. [INTEGRATION] Retrieve source data for the required population/time window and preserve source reference/query definition. Prefer an authoritative governed business-data/measurement source when available; preserve its metric semantics, coverage, freshness, evidence class, and reason codes rather than recomputing an alternate truth in the model.
3. [DETERMINISTIC] Apply only explicitly defined mechanical formula/aggregation rules and retain denominator/sample where relevant. If semantic choices are required to define population, identity, attribution, or inclusion, the model/user or authoritative source must resolve them first.
4. [DETERMINISTIC] Validate dimensions, unit, window boundaries, missingness, references, and exact duplicate persistence.
5. [AI] Describe material source/data quality limitations when the value is modeled, estimated, partial, or otherwise not a direct authoritative measurement. Preserve actual method-specific uncertainty/error bounds when the source provides them; do not manufacture a generic confidence score.
6. [DETERMINISTIC] Persist the MetricObservation when the measurement has durable organizational value. Do not emit an AURA runtime event or subscriber notification merely because a metric was recorded.

## Verification
- The MetricObservation is schema-valid, reproducible from its definition/source at the level claimed, and belongs to the correct organization.
- Semantic measurement choices are not hidden inside deterministic aggregation.

## Failure / Fallback
- If the requested metric cannot be supported by available evidence, preserve the unresolved measurement need rather than inventing a value, zero, direction, or certainty score.

## Completion Criteria
- Future work can understand the metric value, definition, source, window, material limitations, and evidence class without requiring runtime event state.
