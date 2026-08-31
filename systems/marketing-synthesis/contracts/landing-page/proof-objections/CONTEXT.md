---
id: marketing.landing-page.proof-objections
type: playbook
version: 1.3.0
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
# Landing Page Proof and Objection Architecture

## Purpose
Place the right evidence and objection resolution into the landing page at the moments of highest doubt.

## Business Outcome
Increase credible belief without overwhelming visitors or making unsupported rebuttals.

## Run When
Run when a landing page requires material proof and objection handling.

## Process
1. [AI] Map each major claim/decision stage to likely doubt/objection using Customer Insights and traffic context.
2. [DETERMINISTIC] Resolve eligible ProofRecords and claim support.
3. [AI] Select proof type/subject/context most similar to the visitor’s doubt and define how much context it needs.
4. [AI] Decide whether each objection is best handled through explanation, proof, demonstration, comparison, guarantee/terms, qualification, or product/process change.
5. [HYBRID] Avoid dismissing legitimate objections or presenting exceptional outcomes as typical.
6. [AI] Specify proof/objection placement and Content production needs.
7. [DETERMINISTIC] Feed all claims/proof into final validation.
