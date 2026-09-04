---
id: seo.execution.aeo.question-universe
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
---
# Question / Prompt Universe

## Purpose
Build and refresh the high-value questions and conversational prompts through which buyers may discover, compare, or evaluate the brand, Offer, category, or problem.

## Business Outcome
Give AEO work a decision-relevant demand universe grounded in customer language and business value rather than an unbounded list of generated prompts.

## Run When
Use when the organization needs to establish or materially refresh the questions/prompts worth observing or serving for a current AEO/search decision.

## Process
1. Start from current Brand/Offer/Audience/Market context, awareness stages, customer objections, support/sales language, existing organic demand, and relevant competitor/category evidence.
2. Generate natural conversational forms that reflect real discovery and decision behavior: broad discovery, problem diagnosis, comparisons, recommendations, constraints, local needs, follow-ups, and brand-specific verification where relevant.
3. Incorporate observed first-party queries, on-site search, sales/support questions, AI grounding/query evidence, and useful third-party demand evidence when available.
4. Consolidate semantic duplicates while preserving materially different constraints, audience, geography, stage, intent, or answer requirement.
5. Map the meaningful prompt clusters to business value, likely answer need, relevant owned/earned assets or entities, and answer surfaces only where that mapping helps action.
6. Refresh or rerank the universe when new evidence, product/market change, competitor movement, or observed answers make the existing set materially stale. Recurring wakeups belong to the active runtime, not AURA itself.

## Proportionate Scope
Cover enough prompt diversity to represent the important customer decision space. Stop expanding when additional prompts are mainly paraphrases or unlikely to change prioritization; broaden when new audiences, markets, Offers, or answer behaviors materially change the universe.

## Verification
- Prompt volume is not treated as business value.
- Material customer constraints and intents are preserved through clustering.
- Generated prompts are distinguished from observed demand evidence.
- A refresh intention does not imply that AURA schedules or runs background checks.
