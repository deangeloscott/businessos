---
id: marketing.intelligence.ecosystem-radar
type: workflow
owner_system: marketing-synthesis
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
- Asset
writes:
- Observation
- Insight
context:
- Business
- Brand
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
workflows:
  conditional:
  - id: core.intelligence.ecosystem.source-discovery
    when: Relevant marketing evidence still needs discovery, inspection, or conversion from leads into support-grade source material.
  - id: core.intelligence.ecosystem.evidence-triangulation
    when: A material marketing mechanism or performance claim benefits from explicit independence, contradiction, freshness, methodology, or uncertainty analysis.
  - id: marketing.experimentation.message-test
    when: A promising uncertain marketing mechanism is testable and a bounded experiment would materially improve the decision.
---
# Marketing Ecosystem Tactic Radar

## Purpose
Discover and evaluate emerging positioning, messaging, offer-presentation, creative, advertising, funnel, landing-page, email, webinar, VSL, and campaign mechanisms before using them in marketing work.

## Business Outcome
Improve persuasion faster from credible external learning while avoiding copycat marketing, anecdotal best practices, and tactics that do not fit the active audience/offer/channel.

## Run When
Use on demand for marketing refresh or when a material new persuasion/channel tactic or measured result could affect the business.

## Process
1. [HYBRID] Reuse current Marketing Learning, customer/competitor evidence, owned performance, prior experiments, Assets, and SourceProfiles before external expansion.
2. [AI] Discover mechanism claims across practitioners, primary experiments, case studies, research, competitors, communities, platform changes, and adjacent categories only to the depth relevant to the current marketing decision. Draw on Core source-discovery knowledge when it materially improves coverage or provenance.
3. [HYBRID] Preserve underlying evidence and use Core triangulation when useful to separate original measurements, independent replications, repeated retellings, practitioner inference, commercial promotion, and counterevidence. Do not require ceremonial triangulation when the evidence needed for the decision is already sufficient.
4. [AI] Identify the persuasion mechanism and conditions: audience awareness/segment, Offer, proof, channel, creative format, traffic/source context, journey stage, and outcome measured.
5. [AI] Determine whether the reported metric is a leading signal, a downstream commercial result, or something in between, and consider confounders such as media mix, targeting, Offer changes, seasonality, or funnel changes before inferring effect. Attention, response, click, conversion, and revenue signals can all matter; keep the observed stage of the pathway explicit rather than either dismissing upstream signals or promoting them into unobserved downstream outcomes.
6. [AI] Decide what the evidence warrants next: ignore, watch, investigate, test, adapt into current work, revise Learning, or do nothing. `marketing.experimentation.message-test` and other Marketing Playbooks/Workflows are optional methods, not automatic routes.
7. [AI] Where owned outcomes exist, use them to assess support/contradiction/inconclusive status without generalizing one winning creative/offer across audiences or channels.
8. [DETERMINISTIC] Persist only material Observation/Insight evidence and exact references selected by the model/user. Reusable Marketing Learning updates require the appropriate evidence and semantic judgment rather than automatic lifecycle progression.

## Verification
- External tactics do not become active-business facts, offers, promises, or permissions.
- Claimed lift is not treated as causal without evidence/design that supports causality.
- No Opportunity, WorkRequest, experiment, or Learning update is created merely because the radar observed a tactic.

## Completion Criteria
- Material marketing mechanisms are evidence-calibrated and scoped to their applicability, with any suggested next method left to capable model/user judgment.
