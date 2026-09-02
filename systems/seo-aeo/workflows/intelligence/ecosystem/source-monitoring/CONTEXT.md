---
id: seo.intelligence.ecosystem.source-monitoring
type: workflow
owner_system: seo-aeo
reads:
- type: Insight
  owner_system: industry-intelligence
- type: Learning
  owner_system: seo-aeo
writes:
- SourceRecord
- Observation
evidence_inputs:
- SEO ecosystem source map
- Official search answer engine guidance
---
# SEO Ecosystem Source Monitoring

## Purpose
Capture material official search/answer-engine changes and credible SEO/AEO research as reusable sources and observations without automatically changing operating guidance.

## Business Outcome
Keep SEO/AEO strategy current, evidence-linked, and connected to measurable organic and business outcomes without turning AURA into a scheduler or creating a parallel strategy-evidence store.

## Run When
Use when a fresh check of important SEO/AEO sources is useful because the user asks, a runtime invokes the work, a known source changed, or another material signal warrants review. AURA may remember monitoring intent; the active harness/runtime owns actual scheduling and polling.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless the applicable evidence-sharing rules actually permit it.

## Process
1. [AI] Maintain or use a source map grouped by official documentation/changelogs, primary research, replicated practitioner evidence, case studies, communities, and speculative commentary; record which fact types each source can credibly support when that distinction matters.
2. [INTEGRATION] Using the active harness's available capabilities, retrieve new or changed items and record publication/change time separately from retrieval time when known.
3. [HYBRID] Deduplicate syndicated or repeated items, preserve the original source identity, and record a content/version hash when useful.
4. [AI] Classify each material item by affected SEO/AEO mechanism, surface, market applicability, materiality, and which existing Learning or operating knowledge could be affected.
5. [HYBRID] Record direct factual statements as Observations with SourceRecord lineage; do not turn recommendations or speculative claims into facts.
6. [AI] For material strategy claims, use claim extraction, evidence assessment, official-guidance checking, experimentation, or another sound method only when it materially improves the decision. Do not create an internal routing chain merely because those Workflows exist.
7. [AI] Preserve a material operational concern, unresolved question, Insight, Learning change, or other durable state only when future organizational work benefits from remembering it.

## Related operating knowledge
Useful methods may include:
- `seo.intelligence.ecosystem.claim-extraction`
- `seo.intelligence.ecosystem.evidence-grading`
- `seo.intelligence.ecosystem.official-contradiction-check`
- `seo.learning.strategy-experiment-design`

These are optional expert methods selected by the model/user, not runtime routes.

## Verification
- Validate written AURA objects and preserve SourceRecord/Observation lineage.
- Keep evidence strength, conclusion confidence, applicability, uncertainty, and external platform/policy status distinct.
- Do not fabricate a runtime Event merely because monitoring found something important.

## Measurement
- Strategy claims become stronger only through relevant observations, experiments, OutcomeEvaluations, replication, or authoritative guidance; popularity and confidence language are not outcome evidence.

## Learning
- Maintain SEO-specific strategy knowledge as SEO Domain Learning only when the accumulated evidence materially supports durable organizational learning.

## Failure / Fallback
- If a source cannot be retrieved with the current harness, use another authoritative source when that still answers the question. Otherwise preserve the evidence gap or unresolved work honestly; do not invent the missing evidence or a fake runtime action.
- If evidence remains contradictory or insufficient, preserve uncertainty and keep the claim at the narrowest justified maturity.

## Completion Criteria
- Material new evidence is captured through current SourceRecord/Observation semantics when useful.
- Provenance, contradictory evidence, applicability, confidence, and external guidance status remain inspectable.
- No tactic is promoted, deprecated, blocked, or handed off merely because a monitoring Workflow observed it.
