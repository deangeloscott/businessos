---
id: industry.monitoring.news
type: workflow
owner_system: industry-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- IndustryEvent
- Insight
context:
- Business
- Market
- Objective
- ProductService
---
# News Monitoring

## Purpose
Find materially relevant current industry developments while suppressing duplicate/low-value coverage and keeping real-world events distinct from AURA runtime events.

## Business Outcome
Improve awareness of external change through timely, evidence-backed news monitoring.

## Run When
When a business decision or monitoring intent needs current industry news and existing evidence is missing, stale, or unresolved.

## Process
1. [INTEGRATION] Retrieve relevant new material with publication/event dates and source references using the active harness's available capabilities.
2. [HYBRID] Use exact URLs/hashes/references for mechanical deduplication and model judgment to identify syndication, rewrites, or separate reports about the same underlying real-world event. Do not collapse distinct events from lexical similarity alone.
3. [AI] Extract the actual event claims, entities, dates, affected market, and what is confirmed versus reported/speculative.
4. [AI] Judge materiality against active markets, products/services, Objectives, and existing IndustryEvents at the depth needed for the current decision.
5. [HYBRID] Verify high-consequence claims with authoritative or meaningfully independent sources before relying on them.
6. [HYBRID] Create/update a durable IndustryEvent only when the model/user judges the evidence to concern the same real-world event and preserving that event has future value. Preserve direct Observations; create an Insight only when durable interpretation is warranted.
7. [DETERMINISTIC] Persist the selected evidence/state and validate references. Do not emit an AURA runtime event merely because an IndustryEvent changed.

## Verification
- Real-world event identity and materiality are evidence-backed semantic judgments.
- Syndicated/repeated reporting does not inflate independent evidence.
- IndustryEvent state remains organizational intelligence, not runtime messaging.

## Completion Criteria
- Important current developments are represented with enough evidence, uncertainty, and event identity for future work to reuse without an internal event bus.
