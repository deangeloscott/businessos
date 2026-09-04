---
id: seo.intelligence.organic-competition.page-analysis
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- Observation
- OrganicCompetitorState
- Competitor
writes:
- OrganicCompetitorState
- MetricObservation
- Observation
- Competitor
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Competitor Page Analysis

## Purpose
Compare a specific competing page or asset against the owned or missing asset for a defined intent and determine what, if anything, is materially better about the competing experience.

## Business Outcome
Learn from assets that repeatedly earn valuable search/answer attention without copying their text, mistaking surface similarity for causality, or turning every difference into a new task.

## Run When
Use when a specific competing asset is materially visible for important demand or answer prompts and page-level comparison could explain a useful gap or improvement opportunity.

## Process
1. [HYBRID] Retrieve the competing asset and inspect the dimensions that matter to the intent: asset type, audience, freshness, structure, entities, evidence, media, usability, CTA/next step, internal/external references, and visible structured information.
2. [HYBRID] Preserve the query, prompt, result, citation, or other context that makes the page competitively relevant. A page should not be analyzed merely because it belongs to a known competitor.
3. [HYBRID] Compare it with the owned target or missing owned experience on usefulness, distinct information, evidence, format, accessibility, conversion alignment, authority/context, freshness, and other factors that can plausibly affect the user or discovery surface.
4. [AI] Identify the few material differences that may explain why the competing asset earns attention. Avoid superficial proxies such as raw word count or copying visible page structure without understanding the mechanism.
5. [AI] Classify useful gaps by their real mechanism—content, evidence, format, technical delivery, internal linking, authority, reputation, local relevance, Offer/brand fit, or another supported cause—and distinguish observation from causal inference.
6. [AI] Decide whether the organization should improve an existing asset, create something genuinely missing, use another specialist method, or do nothing. Competitor performance is evidence to learn from, not a required template.
7. [HYBRID] Preserve page-level evidence and conclusions when they will improve current or future work. Create an Opportunity only when the unresolved possibility itself is worth remembering.

## Verification
- Comparison is tied to a defined user/search/answer intent.
- Competitor strengths are inferred from evidence, not assumed from rank alone.
- Strong visibility is treated as a meaningful signal of exposure and possible user/discovery preference while remaining distinct from proven causality or competitor revenue.
- Recommendations preserve owned differentiation and business truth rather than copying the competitor.
