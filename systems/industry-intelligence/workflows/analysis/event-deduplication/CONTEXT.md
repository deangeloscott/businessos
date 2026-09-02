---
id: industry.analysis.event-deduplication
type: workflow
owner_system: industry-intelligence
reads:
- IndustryEvent
- Observation
- SourceRecord
- Insight
writes:
- IndustryEvent
- Observation
- Insight
context:
- Business
- Market
- Objective
- ProductService
---
# Event Deduplication & Clustering

## Purpose
Resolve many articles/updates into one coherent view of the same evolving real-world IndustryEvent when the evidence supports that interpretation.

## Business Outcome
Keep industry intelligence accurate and reusable by preventing duplicate coverage from becoming duplicate organizational events or inflated evidence.

## Run When
Run when multiple reports or observations may concern the same underlying external event and distinguishing duplicate coverage from genuinely separate events matters to current or future decisions.

## Process
1. [DETERMINISTIC] Normalize exact source URLs, hashes, timestamps, and mechanically identical/syndicated material so obvious duplicates can be identified cheaply.
2. [AI] Compare entities, event action, location/jurisdiction, dates, causal sequence, source claims, and material distinctions to judge whether remaining items refer to the same underlying real-world event.
3. [AI] Keep events separate when materially different actions, jurisdictions, dates, actors, or causal episodes would change organizational understanding or decisions.
4. [DETERMINISTIC] After the semantic event identity is resolved, consolidate exact references into the appropriate IndustryEvent without deleting contradictory Observations or useful historical evidence.
5. [AI] Update the durable event summary/status only to the extent supported by current evidence and preserve important chronology, uncertainty, and contradictions.
6. [DETERMINISTIC] Persist the selected IndustryEvent/Observation/Insight state and exact lineage. Do not emit runtime events, duplicate alerts, or manufacture a WorkRequest merely because evidence was deduplicated.

## Verification
- Same-event versus separate-event identity is a model/user semantic judgment, not lexical matching alone.
- Duplicate/syndicated coverage does not inflate independent evidence.
- Contradictory evidence remains inspectable after consolidation.
- No runtime event, alert, or internal handoff is created by deduplication itself.

## Completion Criteria
- Future work sees a coherent evidence-backed event record without duplicate coverage, lost contradictions, or internal orchestration artifacts.
