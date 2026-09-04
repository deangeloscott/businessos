---
id: competitor.research.adaptive-source-coverage
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
context:
- Business
- Market
- AudienceSegment
- Offer
references:
- systems/competitor-intelligence/references/source-coverage.json
---
# Adaptive Competitive Source Coverage

## Purpose
Achieve decision-appropriate competitive evidence coverage without forcing every research run through the same fixed list of websites or allowing shallow model discretion to declare research complete too early.

## Business Outcome
Make competitive conclusions more complete, reproducible, and efficient while preserving the agent's ability to discover useful sources and signals not anticipated by AURA.

## Run When
Run as part of substantial competitor research, comprehensive audits, priority competitor onboarding, or whenever current evidence coverage is unclear.

## Process
1. [AI] Select/inherit depth: **Rapid**, **Standard**, **Comprehensive**, or **Continuous**. Tie depth to the business decision, time sensitivity, risk, requested thoroughness, and what additional evidence could realistically change the action.
2. [AI] Resolve the material subjects and dimensions for this decision before treating source count as coverage. A broad comparison may require different evidence classes for pricing, capabilities, positioning, funnels, sentiment, advertising/content patterns, or strategic change; a narrow question may need only one or two dimensions.
3. [AI] Evaluate the relevant evidence classes in the source-coverage reference. Treat named platforms/sites as examples, not an exhaustive whitelist; add credible sources discovered during research when they have material decision value.
4. [HYBRID] For each relevant class, choose the strongest accessible sources by authority, directness, freshness, identity confidence, subject relevance, and expected information gain. Mark irrelevant/unavailable/blocked sources instead of fabricating completeness.
5. [INTEGRATION] Collect evidence from the selected sources using the narrowest appropriate host capability. When a high-signal source reveals a material theme, campaign, funnel, complaint, release, or strategic change, deepen that branch rather than mechanically exhausting low-value sources. Preserve resolved subject scope on evidence used for subject-specific conclusions.
6. [AI] Continuously test coverage for contrary evidence, snapshot bias, platform bias, regional gaps, stale data, subject/evidence mismatches, and competing explanations. Use relevant SEO/AEO or other specialist operating knowledge directly when deep specialist analysis materially improves the work rather than duplicating that expertise or its durable organizational evidence.
7. [DETERMINISTIC] Maintain a coverage Observation recording material subject/dimension or evidence class, specific sources checked, status (`supported`, `limited`, `unknown`, `not_material`, `unavailable`, `blocked`, or `deferred` as appropriate), freshness, strongest evidence refs, important gaps, and why deeper research was or was not warranted. This coverage state supports evidence closure; it is not a fixed matrix that every run must fill exhaustively.
8. [AI] Stop when required depth and material evidence closure are satisfied and additional accessible evidence is unlikely to change the decision enough to justify its cost/time. If an unresolved material gap could plausibly reverse or materially weaken the decision, deepen that area when feasible or preserve the gap and narrow the conclusion. For Comprehensive work, explicitly report material uncovered gaps; for Continuous work, reuse the baseline and focus on changed/high-value areas.

## Verification
The resulting decision can show what subjects/dimensions/evidence classes were materially considered, which were supported or limited, where coverage is unknown/incomplete, which evidence supports the covered areas, and why research stopped, without pretending the source examples define the universe of possible evidence.
