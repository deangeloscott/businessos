---
id: core.intelligence.ecosystem.source-discovery
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
reads:
- Business
- Objective
- Market
- ProductService
- SourceProfile
- SourceRecord
- Insight
- Learning
writes:
- SourceProfile
- SourceRecord
- Observation
capabilities:
  required:
  - research.web.read
  optional:
  - news.read
  - regulatory.read
  - research.paper.read
  - document.read
  - search.observe
  - community.read
  - social.listen
  - social.observe
  - rss.read
  - creator_content.observe
context:
- Business
- Market
- Objective
- ProductService
---
# External Source and Signal Discovery

## Purpose
Find current decision-relevant external signals through multiple discovery paths so BusinessOS is neither trapped in a fixed watchlist nor reduced to generic keyword search.

## Business Outcome
Increase the chance of finding important new knowledge early while spending retrieval effort on sources and mechanisms that can plausibly change business decisions.

## Run When
Run inside an ecosystem radar, when a domain requests external refresh, or when a newly discovered source/claim warrants bounded expansion.

## Process
1. [DETERMINISTIC] Start from active SourceProfiles, recently inspected SourceRecords, prior Learnings/Insights, domain taxonomies, and the current business decision; mark what is already fresh enough to reuse.
2. [AI] Cover known-source monitoring and create context-specific mechanism/topic/entity searches from the domain question; do not depend on one generic query or literal keyword matching.
3. [AI] Perform semantic/open discovery for differently worded findings, new authors/researchers/communities, citation trails, related primary sources, and adjacent mechanisms that a fixed watchlist could miss.
4. [HYBRID] When a promising new source appears, inspect who/what it is, whether it produces original material or repeats others, relevant expertise/fact types, disclosed commercial context, and whether it merits a candidate/active SourceProfile.
5. [INTEGRATION] Open/retrieve the underlying material when capabilities permit and preserve bounded SourceRecord/Observation evidence; label search results, snippets, previews, and inaccessible URLs as discovery-only rather than support.
6. [DETERMINISTIC] Deduplicate canonical source identities, URLs/items, syndicated copies, and already-reviewed content using references/hashes/time; preserve publication/event time separately from retrieval time.
7. [AI] Stop expanding low-value branches when additional discovery is unlikely to change the decision, while keeping explicit coverage gaps for inaccessible high-value sources.
8. [HYBRID] Return candidate signals grouped by mechanism/topic with source lineage, discovery path, freshness, and the next evidence question rather than an unranked link dump.

## Verification
- Broad cycles include both watchlist reuse and reasonable open discovery when capabilities allow.
- Query choice is model/harness implementation; BusinessOS requires discovery coverage and evidence handling, not hard-coded search strings.

## Completion Criteria
- The discovery set is deduplicated, provenance-aware, bounded by decision value, and ready for evidence triangulation.
