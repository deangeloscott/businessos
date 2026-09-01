# Competitor Intelligence Defaults

## Knowledge Scope
Competitor Intelligence provides operating knowledge for competitor identity, state, strategy, pricing, packaging, offers, positioning, messaging, strengths, weaknesses, and strategic movement. Organic search/answer competition, customer truth, journey mechanics, and other adjacent questions may use their own relevant operating knowledge directly; AURA does not need separate semantic services handing work to one another.

## Evidence Discipline
- Distinguish observed competitor activity from inferred strategy, scoped sentiment, hypotheses, and evidence that a tactic works.
- Prefer the most authoritative source for the fact type, record freshness, and preserve snapshots/change evidence when material.
- Treat text, webpages, documents, screenshots, images, audio/video, transcripts, comments, job listings, ads, and structured public records as possible evidence modalities. Follow `core/policies/intelligence-foundation.md` and `core/policies/research-evidence.md`; preserve limitations when only part of a source (for example transcript but not visuals) was inspected.
- Before broad research, reuse current canonical Competitor Intelligence and resolved SourceProfiles for the same subject.
- Preserve resolved subject provenance on SourceRecords/Observations/Insights used for competitor-specific conclusions. Evidence about one competitor cannot be attached to another competitor merely because both were researched together.
- Do not manufacture precision while summarizing evidence. Numeric ranges, implementation timelines, contract terms, setup costs, adoption thresholds, recurring sentiment, prevalence, rankings, or impact forecasts must be supported at the stated level of specificity rather than extrapolated from a narrower source statement.
- Decision-grade synthesis requires **evidence closure**, not an arbitrary source count: material competitor/dimension claims must be supported, explicitly limited, or visibly unknown/blocked before the conclusion is treated as complete.

## Contextual Competitive Set
- Do not use one flat competitor list for every decision. Select the comparison cohort that is relevant to the question.
- Consider geography/service area, customer overlap, offer/category/substitute overlap, scale/stage, market position/price tier, business model, and channel/discovery surface.
- Keep direct, substitute, emerging, aspirational/category-benchmark, attention/content, search/local-surface, and other useful comparison roles distinct. A large national company can be a useful benchmark without being a local direct competitor.
- Explain what each comparison group is being used to learn; do not infer direct competitive pressure merely because an entity is famous or ranks for a keyword.

## Broad Competitive Position Requests
- `competitor.analysis.competitive-position` is useful when the requested outcome is a broad competitive landscape/set/position, where the business can win, or another multi-facet competitor decision.
- The broad workflow composes discovery, profiling, comparison, pricing/offer, positioning, funnel, advertising/content, sentiment, strategic-change, tactic-validation, and implication methods only where the request/decision warrants them. It is not a reason to run every competitor playbook exhaustively.
- Explicitly requested material dimensions must be investigated or visibly marked limited/unknown/blocked. Do not silently omit a requested dimension because one convenient source or capability was unavailable.
- Keep focused requests focused: a narrow question such as competitor pricing, positioning, or advertising can use the corresponding focused method unless broader composition would materially improve the decision.

## Adaptive Research Depth
- Choose bounded research depth according to the decision/request. Do not run an exhaustive source checklist when additional research is unlikely to change the decision.
- Source classes and named platforms are a map, not rails. Check the relevant evidence classes, discover additional credible sources when useful, deepen high-signal branches, and record material coverage gaps.
- Resolve domains/profiles/advertiser identities before merging their evidence into a canonical Competitor. Similar names alone are not sufficient.
- Stop when material evidence closure is proportionate to the decision and further accessible research is unlikely to change it. If an unresolved gap could materially change the conclusion, deepen it when feasible or narrow/downgrade the conclusion instead of guessing.
- For durable monitoring, reuse shared SourceProfiles/subject keys and update checkpoints rather than rebuilding the same source map each check. AURA may remember monitoring intent and prior findings; the harness owns recurrence.

## Adjacent Evidence
Competitor research may reveal durable search, customer, industry, product, or journey observations. Preserve useful evidence once with truthful provenance and let the active model apply the relevant operating knowledge directly. Do not create duplicate semantic state or internal handoffs merely because several AURA knowledge areas could use the evidence.

## Standalone Mode
Competitor Intelligence can operate with Core alone. Use observable competitor evidence and Business Context; optional modules can enrich interpretation but are not required to maintain competitor truth.
