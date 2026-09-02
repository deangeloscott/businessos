---
id: marketing.landing-page.proof-objections
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
# Landing Page Proof and Objection Architecture

## Purpose
Place the right evidence and objection resolution into the landing page at the moments of highest doubt.

## Business Outcome
Increase credible belief without overwhelming visitors or making unsupported rebuttals.

## Run When
Use when a landing page requires material proof and objection handling.

## Process
1. [AI] Map each major claim/decision stage to likely doubt/objection using Customer evidence and traffic context.
2. [HYBRID] Resolve eligible ProofRecords and actual claim support.
3. [AI] Select proof type/subject/context most similar to the visitor’s doubt and define how much context it needs.
4. [AI] Decide whether each objection is best handled through explanation, proof, demonstration, comparison, guarantee/terms, qualification, or a real product/process change.
5. [HYBRID] Avoid dismissing legitimate objections or presenting exceptional outcomes as typical.
6. [AI] Specify proof/objection placement and any useful visual/content production requirements.
7. [HYBRID] Preserve the useful proof/objection architecture and claim relationships in the relevant Asset, then use Content or final claim-validation methods directly as needed. Persist a WorkRequest only for a real durable organizational handoff.
