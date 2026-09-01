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
- WorkRequest
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
Run when an advertising campaign requires this persuasion or QA sub-process; media buying/targeting execution remains outside this OS.

## Process
1. [AI] Choose the specific variable/hypothesis to test: angle, hook, proof, creative mechanism, CTA, or execution element.
2. [AI] Hold other material persuasion variables stable where causal interpretation matters.
3. [DETERMINISTIC] Define variant IDs, allocation/measurement handoff, success/guardrail metrics, and minimum evaluation conditions appropriate to available traffic.
4. [AI] Prioritize high-information contrasts before minor optimizations.
5. [HYBRID] Account for placement/audience/delivery algorithm differences and avoid overclaiming causality from uncontrolled comparisons.
6. [DETERMINISTIC] Define stopping/iteration rule and what decision each result will inform.
7. [AI] Create variant production WorkRequests tied to one test plan.
