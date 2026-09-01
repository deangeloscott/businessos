---
id: marketing.assets.lead-magnet
type: playbook
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
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
# Lead Magnet

## Purpose
Create an exchange-worthy asset that solves a bounded valuable problem and naturally relates to the next commercial step.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed lead magnet that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires lead magnet to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define audience problem/job, urgency, current alternatives, and what useful standalone outcome can be delivered.
2. [AI] Select format/mechanism: checklist, template, calculator, guide, diagnostic, dataset, mini-course, toolkit, or other value-fit asset.
3. [HYBRID] Ensure the asset provides real value rather than merely previewing the sales pitch.
4. [AI] Design content/interaction and natural bridge to Offer based on unresolved next problem.
5. [DETERMINISTIC] Define lead capture/consent/tracking requirements and customer-journey handoff.
6. [DETERMINISTIC] Delegate production to Content where appropriate.
