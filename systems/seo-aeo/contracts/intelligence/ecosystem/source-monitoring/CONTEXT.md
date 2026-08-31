---
id: seo.intelligence.ecosystem.source-monitoring
type: playbook
version: 1.2.0
owner_system: seo-aeo
reads:
- type: Insight
  owner_system: industry-intelligence
- type: Learning
  owner_system: seo-aeo
writes:
- SourceRecord
- Observation
capabilities:
  required:
  - research.web.read
  optional:
  - search.observe
  - news.read
  - document.read
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
Run when the user/runtime invokes this monitoring work because its cadence intent is due, a priority source changes, or another material signal makes a fresh check useful. AURA may remember monitoring intent; the active harness/runtime owns actual scheduling and polling.

## Do Not Run When
Do not treat a publication, practitioner opinion, competitor behavior, or one business result as a validated tactic by itself. Do not use private cross-business evidence unless the applicable evidence-sharing rules actually permit it.

## Process
1. [AI] Maintain a source map grouped by official documentation/changelogs, primary research, replicated practitioner evidence, case studies, communities, and speculative commentary; record which fact types each source can credibly support.
2. [INTEGRATION] Using the active harness's available capabilities, retrieve new or changed items and record publication/change time separately from retrieval time when known.
3. [DETERMINISTIC] Deduplicate syndicated or repeated items, preserve the original source identity, and record a content/version hash when useful.
4. [AI] Classify each material item by affected SEO/AEO mechanism, surface, market applicability, materiality, and which existing Learnings or playbooks could be affected.
5. [HYBRID] Record direct factual statements as Observations with SourceRecord lineage; do not turn recommendations or speculative claims into facts.
6. [HYBRID] Route distinct material strategy claims to claim extraction, evidence assessment, and official-guidance contradiction checking before they influence stronger reusable guidance.

## Decisions / Routing
- Material source claims → `seo.intelligence.ecosystem.claim-extraction`.
- Material operational/platform issue → the relevant SEO incident or other appropriate organizational work.
- A potentially reusable process change → evidence-supported Learning first; broader playbook changes belong in the explicit AURA playbook-evolution path.

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
- No tactic is promoted, deprecated, or blocked for a reason that cannot be traced to evidence or an actual external constraint.
