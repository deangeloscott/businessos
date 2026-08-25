---
id: industry.intelligence.ecosystem-radar
type: playbook
version: 1.0.0
owner_system: industry-intelligence
risk: low
autonomy_ceiling: 4
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - regulatory.read
  - research.paper.read
  - market_data.read
  - rss.read
  - community.read
  - social.listen
context:
- Business
- Market
- Objective
- ProductService
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  - id: industry.source-mapping.priority-sources
  conditional:
  - id: industry.analysis.event-verification
    when: A material event or change needs factual verification.
  - id: industry.analysis.materiality
    when: A verified event may affect an active business decision.
  - id: industry.analysis.business-impact
    when: A material event requires business-specific impact analysis.
  - id: industry.learning.domain-learning
    when: Outcomes or repeated corrections justify reusable Industry Intelligence learning.
---
# Industry Ecosystem Radar

## Purpose
Discover and verify important external industry changes, research, regulation, technology, market shifts, and emerging practices before routing them into Industry Intelligence decisions.

## Business Outcome
Give the business timely external awareness without confusing attention, forecasts, or repeated reporting with verified material change.

## Run When
Run from the Core ecosystem radar, on demand for an industry refresh, or when an external event could materially affect the business.

## Process
1. [HYBRID] Reuse the Industry Source Map, current Industry Insights/Learnings, and recent monitoring before expanding the search.
2. [AI] Define decision-relevant event classes across regulation/standards, technology/platforms, research/science, market structure, supply/demand, distribution, category behavior, macro inputs, and adjacent threats/opportunities.
3. [HYBRID] Use Core discovery to cover priority sources plus open/semantic discovery, then preserve evidence and triangulate material claims with original provenance, independent corroboration, contradiction, freshness, and novelty.
4. [AI] Distinguish an observed event, a forecast, a sustained trend, a practitioner tactic, and an interpretation; do not force all external developments into tactic language.
5. [HYBRID] Route factual event candidates through existing event verification and materiality contracts, then assess scoped impact on this business rather than assuming an industry development applies equally to every company.
6. [HYBRID] Route uncertain practice/tactic claims to the domain that owns the mechanism, create a bounded Industry WorkRequest when more external evidence is needed, and escalate urgent policy/operational risk through existing pathways.
7. [DETERMINISTIC] Preserve event/Insight lineage and update Industry Learning only after repeated evidence, OutcomeEvaluations, or corrections justify reusable guidance.
8. [AI] Return the few developments that could change a decision, what is verified versus uncertain, and the next monitoring/research/action checkpoint.

## Verification
- Primary/authoritative evidence is favored for facts it can establish; other evidence remains eligible for mechanisms/outcomes it can actually support.
- Repeated news coverage of one event is not treated as independent corroboration.

## Completion Criteria
- Material industry findings have verified facts, applicability/materiality status, and an owned next route.
