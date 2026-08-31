---
id: marketing.assets.ads
type: playbook
version: 1.4.0
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
- ProofRecord
writes:
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - advertising.observe
  - research.web.read
  - webpage.snapshot
  - social.observe
  - marketing.performance.read
  - conversion.read
  - analytics.read
  - email.send
  - social.ad.publish
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
- Objective
subcontracts:
  required:
  - marketing.intake.persuasion-brief
  - marketing.ads.angle-matrix
  - marketing.ads.copy
  - marketing.ads.creative-brief
  - marketing.ads.message-match
  - marketing.ads.variant-plan
  - marketing.ads.qa
  conditional:
  - id: marketing.intelligence.ecosystem-radar
    when: Current field/competitor creative evidence is stale or absent and could materially change the campaign hypothesis.
---
# Advertising Creative & Copy

## Purpose
Create persuasive ad concepts/copy/creative requirements matched to audience, awareness, funnel/journey role, channel/placement context, current field evidence where useful, and destination.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed advertising creative & copy that matches audience decision context, Offer, proof, acquisition source, and the destination experience.

## Run When
Run when an Opportunity or WorkRequest requires advertising creative & copy to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define channel placement/context, audience, awareness/knowledge state, funnel/journey role, evidence-backed motivations/objections, Offer, desired action, landing destination, and message continuity.
2. [HYBRID] Reuse current Customer/Competitor/Marketing Insights, owned performance, and current-field evidence. When the creative field could materially change the hypothesis and current evidence is stale/absent, run the bounded conditional Marketing ecosystem research rather than inventing “best practices.”
3. [AI] When external creative evidence is used, compare multiple relevant examples/surfaces and extract transferable mechanisms such as hooks, angles, structures, proof, offers, visual/audio treatment, CTA, and landing continuity. Treat visible engagement, ad longevity, prevalence, or repeated exposure as calibrated proxies—not proof of profitability—and never copy protected expression.
4. [AI] Generate up to three genuinely distinct concept families when meaningful creative uncertainty exists, varying strategic mechanism/motivation/structure/visual system rather than cosmetic headlines. Use fewer when one route is clearly sufficient.
5. [HYBRID] Check claims, policy/compliance, proof, Brand/Offer truth, and whether the creative promise is fulfilled by the destination.
6. [AI] Write copy/creative brief variants sized to placement and platform behavior; specify visual/audio requirements and the role each variant plays in the customer decision context.
7. [HYBRID] Design a test matrix isolating meaningful variables where possible and preserving downstream conversion/quality/business guardrails so a cheap click alone does not define the winner.
8. [DETERMINISTIC] Create WorkRequests to Content for media production and package tracking/measurement requirements. Media buying/targeting execution remains outside Marketing Synthesis unless a separate authorized provider surface is explicitly governed elsewhere.
