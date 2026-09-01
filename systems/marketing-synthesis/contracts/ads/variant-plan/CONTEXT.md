---
id: marketing.ads.variant-plan
type: playbook
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - tracking.read
  - conversion.read
  - marketing.performance.read
  - experiment.run
  - cms.page.publish
  - email.send
  - social.ad.publish
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Advertising Variant Test Plan

## Purpose
Define creative/copy variants so each comparison teaches something interpretable.

## Business Outcome
Increase useful learning while avoiding large grids of arbitrary variants.

## Run When
Use when an advertising campaign needs a bounded, interpretable variant plan; media buying/targeting execution remains outside this method unless separately available and requested.

## Process
1. [AI] Choose the specific variable/hypothesis to test: angle, hook, proof, creative mechanism, CTA, or execution element.
2. [AI] Hold other material persuasion variables stable where causal interpretation matters.
3. [HYBRID] Define variant IDs, allocation/measurement needs, success/guardrail metrics, and minimum evaluation conditions appropriate to actual available traffic.
4. [AI] Prioritize high-information contrasts before minor optimizations.
5. [HYBRID] Account for placement/audience/delivery algorithm differences and avoid overclaiming causality from uncontrolled comparisons.
6. [AI] Define stopping/iteration logic and what decision each result will inform without turning the plan into an AURA scheduler or experiment runtime.
7. [HYBRID] Preserve the test/variant plan as an Asset and use the active harness's real creative/experiment capabilities directly when execution is requested and available. Persist a WorkRequest only for a real durable organizational handoff to a separate executor.
