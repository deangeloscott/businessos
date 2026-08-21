---
id: customer.analysis.before-after-proof
type: playbook
version: 1.2.0
owner_system: customer-intelligence
risk: medium
autonomy_ceiling: 3
reads:
- SourceRecord
- Observation
- Insight
- Asset
- ProofRecord
writes:
- Observation
- ProofRecord
capabilities:
  required:
  - none
  optional:
  - webpage.screenshot
context:
- AudienceSegment
- ProductService
- Offer
---
# Before/After and Proof Extraction

## Purpose
Extract credible proof, testimonial language, and before/after states from customer evidence without exaggerating the customer's actual experience.

## Business Outcome
Create reusable, permission-aware proof that can support content, persuasion, SEO, sales enablement, and customer education while preserving what the source truly said.

## Run When
Run when a review, comment, interview, case result, support conversation, survey response, or customer metric appears to contain a useful outcome, transformation, demonstration, or endorsement.

## Process
1. [DETERMINISTIC] Resolve the original source and direct Observation; prefer the original public/first-party evidence over summaries or copied quotes.
2. [AI] Extract verbatim testimonial language, explicit starting condition, intervention/use context, resulting condition, quantified result, unexpected benefit, and any limitations actually stated.
3. [AI] Separate explicit before/after evidence from inferred narrative; leave fields unknown rather than inventing a dramatic transformation.
4. [HYBRID] Determine the narrow claim supported, audience/product/offer relevance, representativeness, contradictory evidence, and whether a customer-specific result can safely be generalized at all.
5. [HYBRID] Determine usage permission/constraints for quotation, screenshot, name/identity, advertising, derivative creative, and case-study use; restrict the record when permission is unclear.
6. [INTEGRATION] Preserve an allowed screenshot/snapshot Asset when visual proof matters and link it to the original SourceRecord.
7. [DETERMINISTIC] Deduplicate against existing ProofRecords and persist/update the canonical ProofRecord with source, Observation, Asset, before/after, supported claim, confidence, freshness, and restrictions.
8. [HYBRID] Route the resulting proof to downstream relevance evaluation; do not create Marketing or Content Opportunities merely because proof exists.
