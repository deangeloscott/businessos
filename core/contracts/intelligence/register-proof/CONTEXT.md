---
id: core.intelligence.register-proof
type: playbook
version: 1.2.0
owner_system: core
risk: low
autonomy_ceiling: 3
reads:
- SourceRecord
- Observation
- Asset
- MetricObservation
- ProofRecord
writes:
- ProofRecord
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - proof.registered
context:
- AudienceSegment
- ProductService
- Offer
---
# Register Reusable Proof

## Purpose
Turn direct evidence into one reusable ProofRecord without overstating what the evidence proves or losing source, permission, and usage constraints.

## Business Outcome
Make credible proof easy to find and reuse across Content, Marketing, SEO/AEO, Customer Optimization, and future systems while keeping every claim traceable and defensible.

## Run When
Run when a testimonial, review, customer result, demonstration, metric, certification, case result, or third-party validation could materially support a business claim.

## Process
1. [DETERMINISTIC] Confirm the evidence belongs to the active business and resolve the original SourceRecord, supporting Observations, and any original screenshot/media Asset.
2. [AI] State the narrowest claim the evidence directly supports; separate direct evidence from interpretation, causal inference, and promotional language.
3. [AI] Extract proof type, verbatim text where relevant, supported before state, after state, outcome, and the exact product/offer/audience scope without inventing missing transformation details.
4. [HYBRID] Determine permission status and usage constraints for quotation, screenshot, identity, advertising, case-study, and derivative use; mark restricted/prohibited use rather than assuming public availability equals consent.
5. [HYBRID] Assess evidence strength, confidence, freshness, source incentives, representativeness, and any contradictory evidence.
6. [DETERMINISTIC] Search existing ProofRecords for the same source, claim, subject, or result; update/supersede rather than creating duplicate proof.
7. [DETERMINISTIC] Persist the ProofRecord with source, Observation, Asset, audience/product/offer references, lineage, review date, and restrictions.
8. [HYBRID] Verify that a downstream user could answer “what exactly does this prove, where did it come from, and may we use it this way?” from the record alone.
