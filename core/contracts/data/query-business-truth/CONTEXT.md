---
id: core.data.query-business-truth
type: playbook
version: 1.8.0
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
# Query Governed Business Truth

## Purpose
Answer a decision-relevant question from the active business's authoritative/connected data without making the model re-derive provider-specific joins, metrics, identity, or attribution semantics when a governed semantic plane is available.

## Business Outcome
Turn connected first-party business data into evidence-linked inputs that BusinessOS domain processes can safely interpret, compare, and act on.

## Run When
When a BusinessOS job needs internal business evidence, especially a cross-domain analytical answer, metric, cohort, journey, comparison, or time-series result.

## Process
1. [HYBRID] Define the business decision/question, required measures/dimensions/population/window, intended use, and evidence authority needed; reuse existing current results when they already answer the question.
2. [DETERMINISTIC] Inspect active capability bindings and provider readiness. When `business.data.query` is available, follow `core/policies/viraltrac-native-companion.md` or the equivalent provider contract and prefer a governed semantic query for cross-domain first-party analysis; use a more specialized bounded tool when it is materially better suited.
3. [INTEGRATION] Plan/execute the smallest authorized query or bounded read needed. Preserve interpreted definitions, time/window, currency/unit, attribution/identity policy, coverage, freshness, quality/confidence, reason codes, evidence references, and partial/unavailable status. Never treat missing/unavailable data as zero.
4. [DETERMINISTIC] Persist a SourceRecord pointing to the authoritative query/run/result/artifact/export rather than bulk-copying operational history into the BusinessOS workspace. If the job needs a canonical metric value, publish it through the matching MetricDefinition and `core.measurement.publish-metric` semantics.
5. [AI] Create only bounded Observations needed by the active job. Do not promote provider narrative/recommendations directly into canonical Insight or Opportunity; route interpretation to the semantic owner.
6. [HYBRID] If the governed semantic surface is unsupported, partial, stale, policy-denied, or unavailable, use a relevant specialized binding, another compatible provider, or manual/assisted evidence while preserving the gap and source boundary.
7. [DETERMINISTIC] Validate SourceRecord/Observation/MetricObservation writes, business isolation, lineage, and reproducible external references; return the evidence packet to the requesting process.

## Verification
The answer is tied to an authoritative or explicitly qualified source/result, its semantics and coverage are reproducible, and BusinessOS persisted only the durable evidence/intelligence needed for the decision rather than a second copy of the provider's operational database.
