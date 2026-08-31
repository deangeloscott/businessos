---
id: marketing.strategy.proof
type: playbook
version: 1.2.0
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
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - none
  optional:
  - marketing.performance.read
  - conversion.read
  - analytics.read
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
Increase the likelihood of the desired commercial action through evidence-backed proof architecture that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires proof architecture to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] List material audience beliefs/claims required for conversion and identify which are likely uncertain or contested.
2. [DETERMINISTIC] Inventory approved ProofRecords and supporting Assets: testimonials, case results, data, demonstrations, credentials, certifications, third-party validation, and product evidence; preserve each record’s claim limits and usage permissions.
3. [HYBRID] Match proof type/source strength to each claim and audience sophistication; strong claims require proportionate evidence.
4. [AI] Identify proof gaps, stale evidence, overused weak social proof, and claims with no valid support.
5. [AI] Sequence proof near the question/objection it resolves rather than dumping all testimonials in one section.
6. [HYBRID] Define claim wording limits and needed new evidence requests; do not use restricted ProofRecords outside their permitted context.
