---
id: competitor.research.baseline-snapshot
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- SourceRecord
- Observation
- Insight
writes:
- Observation
- Insight
context:
- Business
- Market
- AudienceSegment
- Offer
---
# Competitor Baseline Snapshot

## Purpose
Establish a dated, evidence-backed current-state baseline for a priority competitor.

## Business Outcome
Make future changes detectable without confusing old facts, copied claims, and current state.

## Run When
Run when a competitor becomes priority or lacks a sufficiently current baseline.

## Process
1. [DETERMINISTIC] Resolve the canonical Competitor and source map; identify required state dimensions.
2. [INTEGRATION] Capture current first-party evidence for products, packaging, price, offers, positioning, target audience, key funnel entry points, and releases where relevant.
3. [AI] Extract factual state separately from strategic interpretation.
4. [DETERMINISTIC] Store retrieval dates, source refs, versions/hashes/snapshots where useful for future comparison.
5. [AI] Note unknown/private dimensions explicitly instead of filling them from inference.
6. [AI] Compare with any prior state and surface material changes separately from the new baseline.
7. [HYBRID] Update the Competitor summary only from supported facts and linked Insights.
