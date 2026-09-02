---
id: marketing.assets.ads
type: workflow
owner_system: marketing-synthesis
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
---
# Advertising Creative & Copy

## Purpose
Create persuasive ad concepts/copy/creative requirements matched to audience, awareness, funnel/journey role, channel/placement context, current field evidence where useful, and destination.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed advertising creative & copy that matches audience decision context, Offer, proof, acquisition source, and the destination experience.

## Run When
Run when the organization needs advertising creative/copy to remove a commercial persuasion gap or create the required conversion asset. An existing Opportunity or real WorkRequest may provide context but is not required.

## Process
1. Define channel placement/context, audience, awareness/knowledge state, funnel/journey role, evidence-backed motivations/objections, Offer, desired action, landing destination, and message continuity.
2. Reuse current Customer/Competitor/Marketing Insights, owned performance, and current-field evidence. When the creative field could materially change the hypothesis and current evidence is stale/absent, use bounded current research rather than inventing “best practices.”
3. When external creative evidence is used, compare multiple relevant examples/surfaces and extract transferable mechanisms such as hooks, angles, structures, proof, offers, visual/audio treatment, CTA, and landing continuity. Treat visible engagement, ad longevity, prevalence, or repeated exposure as calibrated proxies—not proof of profitability—and never copy protected expression.
4. Use relevant advertising operating knowledge—such as angle development, copy, creative planning, message match, variant design, or QA—only where it materially improves the requested result. Develop up to three genuinely distinct concept families when meaningful creative uncertainty exists, varying strategic mechanism/motivation/structure/visual system rather than cosmetic headlines. Use fewer when one route is clearly sufficient.
5. Check claims, policy/compliance, proof, Brand/Offer truth, and whether the creative promise is fulfilled by the destination.
6. Produce copy and creative/media requirements sized to placement and platform behavior. If media production is also part of the user's request and the active harness can do it, perform it directly using the relevant Content/creative capabilities; otherwise return the smallest precise production brief or create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
7. Define a test matrix isolating meaningful variables where useful and preserving downstream conversion/quality/business guardrails so a cheap click alone does not define the winner.
8. Preserve the resulting advertising Asset(s), evidence lineage, and useful test/measurement requirements when future work benefits from them. Media buying/targeting and publication remain host/external-system execution, not an AURA authorization or provider-control layer.

## Proportionate Scope
Use only the current-field research, concept breadth, variant count, production detail, and testing structure needed to resolve the actual creative uncertainty. Expand when stakes, spend, audience complexity, or uncertainty justify deeper evidence; do not manufacture variants or research volume for completeness theater.

## Verification
- Claims and Offer terms remain grounded in current organizational truth/evidence.
- Creative variants differ for a meaningful reason rather than cosmetic count-filling.
- Relevant Workflows are reusable operating knowledge, not required execution stages.
- Content/creative production is composed directly when the current model/harness can do it; WorkRequest is reserved for a real durable handoff.
- Visibility, prevalence, engagement, or longevity are not presented as proof of profitability.

## Completion Criteria
- The organization has decision-ready advertising creative/copy or the precise remaining real-world handoff needed to complete it, without an internal AURA request chain.
