---
id: marketing.landing-page.copy
type: playbook
version: 1.4.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 2
reads:
- Opportunity
- Insight
- ProofRecord
- Asset
- WorkRequest
writes:
- ActionPacket
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
# Landing Page Copy

## Purpose
Write the complete evidence-backed copy for an approved landing-page persuasion architecture.

## Business Outcome
Communicate the right promise, mechanism, proof, Offer, fit, objections, and CTA clearly enough for qualified visitors to decide.

## Run When
Run after landing-page architecture, message match, proof, and Offer facts are resolved. When the requested deliverable is a standalone customer-facing homepage/landing-page draft, do **not** create the bounded Run with this leaf contract as the root; execute it as the required subcontract of `marketing.assets.landing-page`.

## Process
1. [AI] Draft headline/subheadline/opening from source-message match and audience desired outcome without unsupported superlatives.
2. [AI] Write each section to perform its assigned persuasion job using customer language, concrete specifics, mechanism, examples, and proof.
3. [AI] Present Offer scope/terms/fit transparently and include qualification/disqualification where it improves customer quality.
4. [AI] Address important objections at the point they arise rather than adding a generic FAQ only.
5. [AI] Write CTA/microcopy so the user knows what happens next and what commitment is being made.
6. [HYBRID] Remove jargon, repetition, vague claims, unnecessary hype, and copy that masks journey/product problems.
7. [DETERMINISTIC] Hand final draft to claim/proof/QA checks with section→evidence relationships.
