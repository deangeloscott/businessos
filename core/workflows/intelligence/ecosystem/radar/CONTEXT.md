---
id: core.intelligence.ecosystem-radar
type: workflow
owner_system: core
reads:
- Business
- Objective
- Market
- ProductService
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- Observation
- Insight
workflows:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
---
# External Ecosystem Intelligence Radar

## Purpose
Run one evidence-grounded external-intelligence cycle that discovers meaningful outside developments and determines what the evidence actually supports.

## Business Outcome
Keep organizational understanding current without chasing noise, duplicating domain intelligence, or allowing internet popularity to rewrite operating guidance.

## Run When
Use on demand, when durable monitoring intent indicates another review would be useful, after a material external change, or when stale external assumptions could affect an active business decision.

## Do Not Run When
Do not use this playbook as an always-on daemon. AURA may remember monitoring/cadence intent; the active harness/runtime owns actual scheduling, wake-up, polling, retries, and notification delivery.

## Process
1. [HYBRID] Reuse relevant Business Context, Objectives, current evidence/Learning, prior radar findings, and SourceProfiles before fetching the same material again. Freshness/applicability are model judgments informed by dates and evidence, not deterministic owner routing.
2. [AI] Define the smallest decision-relevant discovery envelope, including the mechanisms/events that could materially change the current decision and enough open discovery to avoid a fixed-watchlist blind spot.
3. [HYBRID] Use `core.intelligence.ecosystem.source-discovery` to find/inspect relevant material and preserve support-grade SourceRecords/Observations; snippets/unvisited results remain discovery leads only.
4. [HYBRID] Group potentially related claims with model judgment, then use `core.intelligence.ecosystem.evidence-triangulation` for material candidates so provenance, independence, contradictions, freshness, novelty, methodology, and uncertainty are explicit.
5. [AI] Determine what each finding means for the active organization, if anything. Domain-specific AURA playbooks may be useful operating knowledge when the finding concerns competitors, customers, industry, SEO/AEO, content, marketing, or customer progression, but AURA Core does not automatically invoke or route through them.
6. [AI] Choose the narrowest justified disposition in ordinary reasoning: ignore, remember, watch, investigate, test, act, revise an existing hypothesis/Learning, or do nothing. The choice depends on evidence, applicability, decision value, reversibility, and actual constraints—not a Core routing service or permission lifecycle.
7. [DETERMINISTIC] Persist only material Observation/Insight meaning and exact evidence/source references chosen by the model/user. Update SourceProfile/checkpoint state through its specialized helper when useful. Do not manufacture WorkRequests, Opportunities, or next-route objects solely because a radar cycle occurred.
8. [AI] Return a compact prioritized result: important verified changes, promising hypotheses, material unknowns/contradictions, items worth watching, and the evidence/reason behind each conclusion or suggested next method.

## Verification
- Every material factual conclusion has inspectable provenance and distinguishes independent evidence from echo/republication.
- Domain-specific meaning remains a capable-model judgment; Core does not become a semantic owner/router for every domain.
- Ongoing monitoring intent may be preserved without claiming that a background schedule exists.

## Completion Criteria
- Decision-relevant external evidence has been inspected to the level justified by the question, material conclusions are calibrated to that evidence, and any suggested next method remains a recommendation rather than AURA-owned routing state.
