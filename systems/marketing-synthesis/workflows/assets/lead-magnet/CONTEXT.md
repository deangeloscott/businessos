---
id: marketing.assets.lead-magnet
type: workflow
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
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Lead Magnet

## Purpose
Create an exchange-worthy asset that solves a bounded valuable problem and naturally relates to the next commercial step.

## Business Outcome
Increase the likelihood of the desired commercial action through an evidence-backed lead magnet that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a lead magnet is useful to remove a commercial persuasion gap or create the required conversion asset. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define audience problem/job, urgency, current alternatives, and what useful standalone outcome can be delivered.
2. [AI] Select format/mechanism: checklist, template, calculator, guide, diagnostic, dataset, mini-course, toolkit, or other value-fit asset.
3. [HYBRID] Ensure the asset provides real value rather than merely previewing the sales pitch.
4. [AI] Design content/interaction and natural bridge to Offer based on unresolved next problem.
5. [DETERMINISTIC] Define lead capture/consent/tracking requirements and the real customer-journey transition when relevant.
6. [HYBRID] Use relevant Content operating knowledge and the active harness's real production capabilities directly for the chosen format. Persist a WorkRequest only when a real organizational handoff must survive the current actor/session.
