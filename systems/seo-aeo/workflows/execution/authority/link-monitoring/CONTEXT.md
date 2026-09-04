---
id: seo.execution.authority.link-monitoring
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Link and Mention Monitoring

## Purpose
Detect meaningful new, changed, lost, redirected, or harmful external references and decide whether they warrant attention.

## Business Outcome
Preserve useful authority and awareness of material external-reference changes without treating every provider fluctuation or low-value link as an operational event.

## Use When
Use when changes in external links or mentions could materially affect authority, referral value, reputation, relationships, important assets, or a current business decision.

## Process
1. Compare current link and mention observations with the prior meaningful state, preserving source and observation timing where it affects interpretation.
2. Verify live status, destination, context, redirects, and the surrounding mention before concluding that a gain, loss, or change is real. Distinguish source/provider noise from an actual external change.
3. Classify the material meaning: valuable acquisition, natural loss, recoverable loss, destination change, correction need, spam/noise, reputational issue, or another relevant condition.
4. Decide whether action has plausible value. Continue directly into the appropriate recovery, correction, outreach, reputation, or diagnostic work when useful; create an Opportunity or AttentionItem only when durable coordination or future awareness earns it.
5. Preserve important resulting state, attribution to prior outreach/PR where evidence supports it, and any reusable Learning. Do not force every observation into canonical state.
6. If repeated observation matters, record the monitoring intent and what would count as a material change. The host/runtime owns any actual schedule, polling, or notification delivery.

## Proportional Scope
Monitor the sources, assets, markets, and changes whose loss or gain could materially matter. Avoid exhaustive reaction to low-value link churn simply because a provider can report it.
