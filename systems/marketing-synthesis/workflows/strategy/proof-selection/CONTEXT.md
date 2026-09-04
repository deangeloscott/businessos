---
id: marketing.strategy.proof-selection
type: workflow
owner_system: marketing-synthesis
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Marketing Proof Selection

## Purpose
Select the proof most capable of resolving the audience’s specific doubt at each persuasion point.

## Business Outcome
Use credible, relevant proof instead of dumping testimonials or selecting only dramatic results.

## Run When
Use when a marketing asset needs testimonials, demonstrations, cases, metrics, authority, or third-party proof. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Map the persuasion sequence to the specific doubts/beliefs that need evidence.
2. [HYBRID] Retrieve eligible ProofRecords/SourceRecords with audience/product/Offer relevance, freshness, permissions, and usage constraints.
3. [AI] Rank proof by relevance, directness, representativeness, specificity, similarity to target audience, and ability to demonstrate mechanism/outcome.
4. [AI] Use diverse proof types where different doubts require different evidence; avoid repetitive testimonial volume as substitute for fit.
5. [HYBRID] Exclude expired/restricted/confidential/unrepresentative proof or add necessary qualifiers.
6. [AI] Place each proof immediately where it resolves the corresponding doubt and define display/context requirements.
7. [AI] Preserve selected proof references and claim relationships in the relevant Marketing strategy/Asset so downstream Content/final QA can consume them directly. Persist a WorkRequest only for a real durable organizational handoff.
