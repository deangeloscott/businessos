---
id: marketing.assets.advertorial
type: playbook
version: 1.1.0
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
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
---
# Advertorial

## Purpose
Create clearly compliant editorial-style persuasion that educates while transparently serving a commercial objective.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed advertorial that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires advertorial to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define audience, publisher/context, problem, insight/story, evidence, Offer, and disclosure requirements.
2. [AI] Choose an editorial frame such as investigation, case/story, comparison, guide, or expert explanation that can be truthfully supported.
3. [HYBRID] Maintain clear advertising/sponsorship disclosure and avoid impersonating independent journalism.
4. [AI] Build narrative that delivers informational value before/while connecting to the commercial solution.
5. [HYBRID] Fact-check comparative/causal claims and ensure landing destination continues the promise.
6. [DETERMINISTIC] Package copy/media WorkRequests and measurement plan.
