---
id: marketing.landing-page.form-cta
type: playbook
version: 1.3.0
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
# Landing Page Form and CTA Persuasion Requirements

## Purpose
Define what information and expectation-setting should surround the conversion action while leaving mechanics/friction ownership to Customer Optimization.

## Business Outcome
Improve qualified completion without collecting unnecessary information or hiding next-step consequences.

## Run When
Run when a landing page includes a form, booking, checkout handoff, trial, application, or other conversion action.

## Process
1. [AI] Define the purpose of the action, minimum qualification needed before action, and what the visitor must know first.
2. [AI] Specify CTA wording, expectation/next-step copy, trust/privacy reassurance, required qualification questions, and optional fields from a persuasion perspective.
3. [HYBRID] Challenge every requested field: keep only what is operationally/qualification-required before conversion.
4. [AI] Identify friction or technical issues that belong to Customer Optimization and create WorkRequest instead of solving with copy.
5. [DETERMINISTIC] Define tracking events, success/failure states, consent requirements, and error/confirmation content needs.
6. [AI] Ensure form/CTA message matches the actual downstream process and Offer.
7. [DETERMINISTIC] Verify implemented fields/copy against approved requirements.
