---
id: core.intelligence.ecosystem.source-discovery
type: playbook
owner_system: core
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
Find current decision-relevant external signals through multiple discovery paths so AURA is neither trapped in a fixed watchlist nor reduced to generic keyword search.

## Business Outcome
Increase the chance of finding important new knowledge early while spending retrieval effort only where it can plausibly improve a business decision.

## Run When
Use inside an ecosystem radar, for a bounded external refresh, or when a newly discovered source/claim warrants deeper inspection.

## Process
1. [HYBRID] Start from relevant SourceProfiles, recently inspected SourceRecords, prior Learning/Insights, and current business context. Exact dates/checkpoints can be retrieved deterministically; the active model/user decides whether existing evidence is fresh and applicable enough for the current question. Optional imported exchange/index files may inform discovery but are support data rather than canonical organization truth.
2. [AI] Cover useful known sources and create context-specific mechanism/topic/entity searches from the actual question; do not depend on one generic query or literal keyword matching.
3. [AI] Perform semantic/open discovery for differently worded findings, new authors/researchers/communities, citation trails, related primary sources, adjacent mechanisms, and optional Innovation Exchange contributions when that discovery surface is relevant.
4. [AI] When a promising new source appears, judge real-world identity, originality versus repetition, relevant expertise/fact types, disclosed commercial context, and whether remembering it as a SourceProfile would help future work. Do not merge namesakes or semantically similar sources with deterministic text matching.
5. [HYBRID] Open/retrieve the underlying material with capabilities actually available to the host and preserve bounded SourceRecord/Observation evidence. Search results, snippets, previews, inaccessible URLs, and unverified community claims remain discovery-only rather than support-grade evidence.
6. [HYBRID] Use deterministic normalization/hashes/exact identifiers to collapse mechanically identical URLs/items/files/packages and known duplicates. Let the model/user judge semantic source identity, syndication/republication relationships, or differently presented content that may or may not be the same evidence lineage. Preserve publication/event time separately from retrieval time when it matters.
7. [AI] Stop expanding low-value branches when additional discovery is unlikely to change the decision, while keeping explicit coverage gaps for inaccessible high-value evidence.
8. [AI] Return candidate signals grouped in the way most useful to the decision, with source lineage, discovery path, freshness/limitations, and the next evidence question when one remains material rather than an unranked link dump.

## Verification
- Discovery is not limited to a fixed watchlist or literal keywords when broader semantic discovery materially improves the task.
- Query choice and semantic source identity are model/harness judgments; AURA provides reusable evidence-handling knowledge and exact persistence mechanics.
- Optional exchange/index data never substitutes for support-grade SourceRecord/Observation evidence.
- Popularity, repetition, or mechanically duplicated material is not counted as independent evidence.

## Completion Criteria
- The discovery set is provenance-aware, bounded by decision value, mechanically deduplicated where exact identity is known, and ready for evidence triangulation without deterministic AURA pretending to understand semantic freshness or identity.
