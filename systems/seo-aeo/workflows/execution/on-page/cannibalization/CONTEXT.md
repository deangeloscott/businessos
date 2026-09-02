---
id: seo.execution.on-page.cannibalization
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
writes:
- SEOAssetState
- ChangeEvent
- Asset
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- records topic intent evidence
---
# Cannibalization & Intent Ownership

## Purpose
Determine whether multiple owned assets create harmful search/answer intent ambiguity and resolve it only when consolidation, differentiation, or signal alignment is likely to improve the combined outcome.

## Business Outcome
Clarify useful intent ownership without destroying legitimate multi-page coverage, valuable links, differentiated customer journeys, or historical performance merely because several owned URLs appear for similar demand.

## Run When
Use when multiple owned URLs appear to compete for materially similar queries/topics/prompts, switch visibility unexpectedly, dilute click/conversion performance, or otherwise create a plausible ownership problem.

## Process
1. [AI] Identify the materially relevant query/topic/prompt clusters and owned URLs with overlapping visibility, targeting, citations, or intended demand. Similar keywords alone are not enough to establish a problem.
2. [HYBRID] Compare actual user/search intent, audience, page type, Offer/conversion role, content overlap/distinct value, backlinks, internal links, canonical state, historical performance, and meaningful URL-switching behavior.
3. [AI] Distinguish legitimate multiple-result coverage or distinct sub-intents from harmful duplication, conflicting targeting, unstable ownership, or signal ambiguity. Preserve an unknown/no-change conclusion when evidence does not support intervention.
4. [AI] If harmful overlap is supported, choose the smallest coherent remedy: differentiate or retarget content, clarify internal-link architecture, consolidate content, redirect a superseded URL, align canonicals, or another method justified by the actual mechanism. Do not choose consolidation simply to reduce page count.
5. [HYBRID] Before consequential changes, preserve valuable content, backlinks, navigation, conversion paths, and historical meaning that should survive. Follow customer-facing truth guardrails for any visible content changes.
6. [HYBRID] Execute through the host/site controls actually available under the user's request and verify URL, redirect, canonical, internal-link, and content behavior after the change.
7. [HYBRID] Evaluate subsequent performance at the combined topic/cluster level as well as individual URLs, because moving value from one owned URL to another is not necessarily a business improvement. Allow enough time for the affected search/index mechanism to respond.
8. [AI] Preserve an Opportunity only when a materially valuable unresolved problem remains; preserve material diagnosis/change history when future work benefits from understanding why the assets were differentiated, consolidated, or left alone.

## Verification
- Query/topic similarity alone does not establish harmful cannibalization.
- Distinct useful intents and customer journeys are not collapsed for cosmetic simplification.
- Redirect/canonical/consolidation choices preserve the most valuable legitimate signals and user paths where practical.
- Success is judged on the combined demand/business outcome, not solely the ranking of one surviving URL.
