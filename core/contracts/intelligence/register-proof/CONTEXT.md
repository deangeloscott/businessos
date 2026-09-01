---
id: core.intelligence.register-proof
type: playbook
owner_system: core
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
context:
- AudienceSegment
- ProductService
- Offer
---
# Register Reusable Proof

## Purpose
Turn direct evidence into reusable ProofRecord memory without overstating what the evidence proves or losing source, permission, and usage constraints.

## Business Outcome
Make credible proof easy to find and reuse across Content, Marketing, SEO/AEO, Customer Optimization, and future work while keeping every claim traceable and defensible.

## Run When
Run when a testimonial, review, customer result, demonstration, metric, certification, case result, or third-party validation could materially support a business claim and future work benefits from preserving it.

## Process
1. [DETERMINISTIC] Confirm referenced evidence/objects belong to the active business and resolve exact SourceRecord, Observation, Asset, and MetricObservation references supplied for the proof.
2. [AI] State the narrowest claim the evidence directly supports; separate direct evidence from interpretation, causal inference, and promotional language.
3. [AI] Extract proof type, verbatim text where relevant, supported before state, after state, outcome, and the exact product/offer/audience scope without inventing missing transformation details.
4. [HYBRID] Determine actual permission status and usage constraints for quotation, screenshot, identity, advertising, case-study, and derivative use from available evidence/instructions; public availability alone is not consent.
5. [HYBRID] Assess evidence strength, freshness, source incentives, representativeness, causal limits, and material contradictory evidence.
6. [HYBRID] Retrieve possible existing ProofRecords using exact source/object references and bounded search cues. The model/user decides whether two records represent the same real proof/claim/subject/result; deterministic AURA must not merge them from textual or identifier similarity alone.
7. [DETERMINISTIC] Persist the selected ProofRecord create/update with its exact evidence/object references, lineage, review date, and restrictions.
8. [HYBRID] Verify that a downstream user can answer “what exactly does this prove, where did it come from, and may we use it this way?” from the record and linked evidence.

## Verification
- Material proof claims are traceable to actual evidence and scoped no broader than that evidence supports.
- Permission/usage status is evidence-backed or explicitly unknown/restricted.
- Semantic proof identity/deduplication remains a model/user judgment.

## Completion Criteria
- A reusable ProofRecord exists only when it improves future work, with the evidence, supported claim, scope, and usage limitations clear enough for responsible reuse.
