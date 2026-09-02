---
id: seo.execution.aeo.ai-referral-measurement
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- conversion CRM revenue best available proxy
---
# AI Referral and Assisted Conversion Measurement

## Purpose
Measure observable visits and business outcomes associated with answer surfaces without treating unobservable influence as zero or overstating attribution.

## Business Outcome
Understand the measurable business contribution of AI/answer discovery using the strongest available first-party evidence while keeping direct referral, assisted influence, and visibility proxies distinct.

## Run When
Use when a current AEO/business decision needs to understand whether answer surfaces are producing observable traffic, qualified actions, revenue, or credible assisted influence and relevant measurement evidence exists.

## Process
1. Identify recognizable answer-surface referral/source patterns and the actual tracking detail available from analytics, CRM, surveys, customer-reported source data, or other first-party evidence.
2. Normalize observable sessions, users, events, leads, conversions, revenue, or other business outcomes associated with recognizable AI/answer referrals while preserving the attribution model and material data limitations.
3. Separate direct referral from assisted or self-reported influence. Do not collapse them into one metric or assume missing observable referral data means zero influence.
4. Relate referral/business evidence to prompt, citation, mention, or source observations only when the linkage is defensible. Temporal proximity or shared landing pages alone do not establish causal attribution.
5. Compare conversion quality, value, landing assets, new/returning behavior, downstream outcomes, or other decision-relevant dimensions only where the available sample makes the comparison useful.
6. Use visibility, mention, recommendation, or citation metrics as proxies only when direct business value cannot be observed, and label them explicitly as proxies rather than equivalent outcomes.

## Proportionate Scope
Measure only the channels, segments, landing assets, attribution windows, and downstream outcomes capable of changing the decision. Expand when material value may be hidden by aggregation or attribution uncertainty; do not build elaborate attribution models when the available evidence cannot support them.

## Verification
- Direct referral, assisted influence, self-reported influence, visibility, and business outcomes remain distinguishable.
- Attribution method and known blind spots are visible.
- Temporal association is not presented as causal proof.
- Unobservable influence is reported as unknown rather than automatically zero.
