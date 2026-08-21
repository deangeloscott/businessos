---
id: marketing.assets.landing-page
type: playbook
version: 1.3.0
owner_system: marketing-synthesis
risk: medium
autonomy_ceiling: 3
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- ActionPacket
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - email.send
  - social.ad.publish
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
subcontracts:
  required:
  - marketing.intake.persuasion-brief
  - marketing.landing-page.message-match
  - marketing.landing-page.information-architecture
  - marketing.landing-page.copy
  - marketing.landing-page.proof-objections
  - marketing.landing-page.form-cta
  - marketing.landing-page.qa
---
# Landing Page Persuasion

## Purpose
Design a landing-page persuasion structure that continues acquisition intent and moves the right visitor toward the desired action.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed landing page persuasion that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires landing page persuasion to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Reconstruct visitor source/intent, audience awareness, Offer, desired action, objections, proof, and current friction.
2. [AI] Define page promise/message match and hierarchy from first screen through decision: outcome → problem/context → mechanism/value → proof → objections/risk → offer/CTA.
3. [HYBRID] Determine necessary depth and sections from buyer questions rather than template length.
4. [AI] Specify copy, proof placement, CTA behavior, comparison/FAQ, and information needed for qualification.
5. [HYBRID] Separate persuasion issues from form/checkout/technical journey friction and route those to Customer Optimization.
6. [HYBRID] Verify claims/terms/tracking requirements and delegate design/media production to Content where needed.

## Decision Rules
- Preserve the visitor's acquisition promise unless evidence supports intentionally reframing it.
- Include a section only if it resolves a material question, objection, proof need, qualification need, or decision step for this audience.
- If the page is persuasive but the conversion mechanism is broken or burdensome, keep the diagnosis with Customer Optimization rather than rewriting copy indefinitely.
- Define the primary conversion and any qualification/guardrail metric before deployment.
