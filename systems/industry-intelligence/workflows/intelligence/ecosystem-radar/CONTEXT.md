---
id: industry.intelligence.ecosystem-radar
type: workflow
owner_system: industry-intelligence
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- Insight
context:
- Business
- Market
- Objective
- ProductService
---
# Industry Ecosystem Radar

## Purpose
Discover and verify important external industry changes, research, regulation, technology, market shifts, and emerging practices without converting every finding into a routed action.

## Business Outcome
Give the business timely external awareness while keeping verified events, forecasts, interpretations, and business-specific implications distinct.

## Run When
Use on demand for an industry refresh or when an external development could materially affect the business.

## Process
1. [HYBRID] Reuse the Industry Source Map, current Industry Insights/Learnings, SourceProfiles, and recent evidence when they are relevant before expanding the search.
2. [AI] Define the event/mechanism classes actually relevant to the decision: regulation/standards, technology/platforms, research/science, market structure, supply/demand, distribution, category behavior, macro inputs, or adjacent threats/opportunities.
3. [HYBRID] Discover relevant priority and open sources using the best available research approach. Draw on Core source-discovery, evidence-triangulation, and the established priority-source method when they materially improve the work. Preserve support-grade evidence for material claims and distinguish original provenance, independent corroboration, contradiction, freshness, and novelty where those distinctions matter.
4. [AI] Distinguish an observed event, forecast, sustained trend, practitioner tactic, and interpretation; do not force all external developments into one lifecycle or tactic category.
5. [AI] Use event verification, materiality, or business-impact Workflows when those methods can materially improve the answer. The active model/user decides applicability and sequencing rather than AURA routing events through a fixed chain.
6. [AI] For uncertain practice/tactic claims, identify the mechanism and uncertainty and use whatever relevant method the active model/harness can perform. Create a durable handoff only when a real human/owner handoff needs to survive the current runtime; do not manufacture an Industry WorkRequest.
7. [DETERMINISTIC] Persist only material Industry Insight/evidence meaning and exact references selected by the model/user. Reusable Industry Learning changes only when evidence supports that broader guidance.
8. [AI] Return the few developments that could change a decision, what is verified versus uncertain, applicable business implications, and any suggested next check/method without encoding a mandatory next route.

## Verification
- Primary/authoritative evidence is favored for facts it can establish; other evidence remains eligible for mechanisms/outcomes it can actually support.
- Repeated news coverage of one event is not treated as independent corroboration.
- Industry relevance/materiality is a reasoned judgment, not a deterministic route or score.

## Completion Criteria
- Material industry findings have traceable evidence, calibrated uncertainty, and appropriately scoped business relevance without requiring an AURA-owned next-route state.
