---
id: marketing.landing-page.information-architecture
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
# Landing Page Information Architecture

## Purpose
Sequence the beliefs, proof, offer information, objections, and action components needed to convert the intended visitor.

## Business Outcome
Create a page where each section resolves the next major decision question instead of following a generic template.

## Run When
Run after persuasion brief/message match and before final landing-page copy/design.

## Process
1. [AI] List the visitor’s ordered decision questions from “is this for me?” through outcome/mechanism/proof/fit/terms/risk/action.
2. [AI] Prioritize questions by audience awareness, Offer complexity, price/risk, traffic source, and evidence.
3. [AI] Assign each section one persuasion job and the evidence/visual/CTA it requires.
4. [AI] Place proof immediately around the claims/doubts it resolves; avoid testimonial dumps.
5. [HYBRID] Route process/form/checkout complexity to Customer Optimization rather than compensating with more copy.
6. [AI] Define mobile/scan hierarchy, repeated CTA points only where visitor readiness naturally changes, and optional FAQ/technical detail placement.
7. [DETERMINISTIC] Produce section architecture and content/creative WorkRequests.
