---
id: seo.intelligence.organic-demand.intent-classification
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- OrganicDemandUnit
writes:
- OrganicDemandUnit
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
evidence_inputs:
- Market search answer evidence
- records topic intent evidence
updates:
  OrganicDemandUnit:
  - business_value
  - demand_evidence
---
# Intent and Journey Classification

## Purpose
Understand what the user is actually trying to accomplish and where that need sits in the customer journey rather than relying on keyword syntax alone.

## Business Outcome
Match important organic/search/answer demand to the right kind of experience, information, and next step so visibility is more likely to create useful attention and downstream opportunity.

## Run When
Use when intent or journey role is uncertain, mixed, changing, or materially affects what asset, answer, or business pathway would be useful.

## Process
1. [HYBRID] Review the query or prompt together with observed results/answers, modifiers, related questions, audience/market context, and first-party behavior when available.
2. [AI] Describe the primary task in plain language before assigning any convenient label. Labels such as informational, commercial investigation, transactional, navigational, local, comparison, troubleshooting, or post-purchase are useful summaries, not rigid boxes.
3. [AI] Infer awareness/readiness or journey stage only to the resolution that changes the decision. Use the organization’s preferred model when one exists; do not force a universal funnel taxonomy.
4. [AI] Identify the plausible next useful action or assisted role and distinguish demand that can legitimately connect to the organization from traffic that is interesting but commercially irrelevant.
5. [HYBRID] Preserve mixed or ambiguous intent when the evidence supports multiple tasks rather than forcing a single classification.
6. [AI] Revisit the interpretation when current search/answer composition, customer behavior, conversion evidence, or market context materially contradicts the prior understanding.
7. [HYBRID] Update durable demand context only when future work benefits from remembering the classification and its evidence.

## Verification
- Intent is inferred from evidence and context, not modifiers alone.
- Classification does not constrain the capable model from recognizing a better or more nuanced task interpretation.
- Journey stage, desired next action, and business value remain related but distinct.
- No competitor refresh, Opportunity, or routing step is required merely because intent was classified.
