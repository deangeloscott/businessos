---
id: marketing.assets.ads
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
- ProofRecord
writes:
- Asset
context:
- AudienceSegment
- Brand
- Offer
- Objective
workflows:
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
Run when the organization needs advertising creative/copy to remove a commercial persuasion gap or create the required conversion asset. An existing Opportunity or real WorkRequest may provide context but is not required.

## Process
1. [AI] Define channel placement/context, audience, awareness/knowledge state, funnel/journey role, evidence-backed motivations/objections, Offer, desired action, landing destination, and message continuity.
2. [HYBRID] Reuse current Customer/Competitor/Marketing Insights, owned performance, and current-field evidence. When the creative field could materially change the hypothesis and current evidence is stale/absent, use the bounded conditional Marketing ecosystem research rather than inventing “best practices.”
3. [AI] When external creative evidence is used, compare multiple relevant examples/surfaces and extract transferable mechanisms such as hooks, angles, structures, proof, offers, visual/audio treatment, CTA, and landing continuity. Treat visible engagement, ad longevity, prevalence, or repeated exposure as calibrated proxies—not proof of profitability—and never copy protected expression.
4. [AI] Use the authored advertising submethods as relevant operating knowledge to develop up to three genuinely distinct concept families when meaningful creative uncertainty exists, varying strategic mechanism/motivation/structure/visual system rather than cosmetic headlines. Use fewer when one route is clearly sufficient.
5. [HYBRID] Check claims, policy/compliance, proof, Brand/Offer truth, and whether the creative promise is fulfilled by the destination.
6. [AI] Produce copy and creative/media requirements sized to placement and platform behavior. If media production is also part of the user's request and the active harness can do it, perform it directly using the relevant Content/creative capabilities; otherwise return the smallest precise production brief or create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
7. [AI] Define a test matrix isolating meaningful variables where useful and preserving downstream conversion/quality/business guardrails so a cheap click alone does not define the winner.
8. [AI] Preserve the resulting advertising Asset(s), evidence lineage, and useful test/measurement requirements when future work benefits from them. Media buying/targeting and publication remain host/external-system execution, not an AURA authorization or provider-control layer.

## Verification
- Claims and Offer terms remain grounded in current organizational truth/evidence.
- Creative variants differ for a meaningful reason rather than cosmetic count-filling.
- Content/creative production is composed directly when the current model/harness can do it; WorkRequest is reserved for a real durable handoff.
- Visibility, prevalence, engagement, or longevity are not presented as proof of profitability.

## Completion Criteria
- The organization has decision-ready advertising creative/copy or the precise remaining real-world handoff needed to complete it, without an internal AURA request chain.
