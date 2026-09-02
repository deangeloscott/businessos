---
id: marketing.strategy.proof
type: workflow
owner_system: marketing-synthesis
reads:
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- MetricObservation
- ProofRecord
writes:
- Asset
context:
- AudienceSegment
- Brand
- Objective
- Offer
---
# Proof Architecture

## Purpose
Determine which claims require what proof and how proof should be sequenced to reduce uncertainty.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed proof architecture that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a commercial experience needs a clearer proof strategy or important claims lack credible support. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] List material audience beliefs/claims required for conversion and identify which are likely uncertain or contested.
2. [HYBRID] Inventory approved ProofRecords and supporting Assets: testimonials, case results, data, demonstrations, credentials, certifications, third-party validation, and product evidence; preserve each record’s claim limits and usage permissions.
3. [HYBRID] Match proof type/source strength to each claim and audience sophistication; strong claims require proportionate evidence.
4. [AI] Identify proof gaps, stale evidence, overused weak social proof, and claims with no valid support.
5. [AI] Sequence proof near the question/objection it resolves rather than dumping all testimonials in one section.
6. [HYBRID] Define claim wording limits and the smallest useful new evidence need; do not use restricted ProofRecords outside their permitted context.
7. [AI] Preserve the reusable claim-to-proof architecture as a Marketing-owned strategy Asset. Create a separate research task, Opportunity, or durable WorkRequest only when a real unresolved organizational need warrants it.
