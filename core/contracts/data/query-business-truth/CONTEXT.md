---
id: core.data.query-business-truth
type: playbook
owner_system: core
reads:
- Business
- SourceRecord
- MetricDefinition
writes:
- SourceRecord
- Observation
- MetricObservation
capabilities:
  required:
  - none
  optional:
  - business.data.query
  - business.data.explain
  - business.data.export
  - business.data.artifact.create
  - analytics.read
  - marketing.performance.read
  - tracking.read
  - conversion.read
  - revenue.read
context:
- Business
---
# Query Business Truth

## Purpose
Answer a decision-relevant question from authoritative first-party business data without unnecessarily re-deriving provider-specific joins, metrics, identity, or attribution semantics when a trustworthy semantic source is available.

## Business Outcome
Turn first-party business data into evidence-linked inputs that AURA processes can interpret, compare, and build upon.

## Run When
When work needs internal business evidence, especially a cross-domain analytical answer, metric, cohort, journey, comparison, or time-series result.

## Process
1. [HYBRID] Define the business question, required measures/dimensions/population/window, intended use, and evidence authority needed; reuse current results when they already answer it.
2. [HYBRID] Use the strongest appropriate first-party source/tool available to the active model/harness. ViralTrac may be useful when connected, but AURA does not require or select it. Prefer a governed semantic query when it materially reduces ambiguity in joins, metric definitions, attribution, identity, or coverage.
3. [INTEGRATION] Execute the smallest trustworthy query/read needed using the active runtime. Preserve definitions, time/window, units, attribution/identity assumptions, coverage, freshness, quality limits, reason codes, and evidence references. Never treat unavailable data as zero.
4. [DETERMINISTIC] Persist a SourceRecord pointing to the authoritative result/artifact/export rather than bulk-copying operational history into AURA. Publish canonical metric values through the appropriate MetricDefinition/measurement semantics when needed.
5. [AI] Create only bounded Observations needed by the active job. Provider narrative or recommendations are evidence inputs, not automatic AURA Insight/Opportunity truth.
6. [HYBRID] If the preferred source is unsupported, partial, stale, or unavailable, use another valid source or method and preserve the limitation honestly.
7. [DETERMINISTIC] Validate persisted SourceRecord/Observation/MetricObservation state, business isolation, lineage, and reproducible external references.

## Verification
The answer is tied to an authoritative or explicitly qualified source/result, its meaning and coverage are reproducible, and AURA persists only the durable evidence/intelligence needed for future organizational work.
