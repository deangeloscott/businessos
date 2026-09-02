---
id: competitor.analysis.customer-sentiment
type: workflow
owner_system: competitor-intelligence
reads:
- Competitor
- type: Insight
  owner_system: customer-intelligence
- Observation
- SourceRecord
writes:
- Competitor
- Observation
- Insight
context:
- AudienceSegment
- Business
- Market
- Objective
- Offer
- ProductService
---
# Competitor Customer Sentiment

## Purpose
Understand what customers praise, dislike, expect, and compare about competitors.

## Business Outcome
Improve competitive decisions through evidence-backed competitor customer sentiment, without mistaking observed activity for proven effectiveness.

## Run When
Run when a decision requires current competitor customer sentiment and canonical competitor intelligence is missing, stale, contradictory, or insufficiently specific.

## Process
1. [INTEGRATION] Discover current reviews, public support/community discussions, and customer-alternative evidence, then inspect the underlying items used for material claims. Search snippets and unvisited URLs are discovery leads, not sufficient support. Do not label copied search text as directly inspected evidence; open/retrieve the underlying source when capability permits.
2. [INTEGRATION] Record the acquisition method, then preserve a bounded evidence packet for each material item: durable source reference, retrieval/date/product context, exact source text or bounded exact excerpt when permitted, and screenshot/snapshot when it adds value.
3. [DETERMINISTIC] Persist SourceRecords/Assets/Observations/Insights through `scripts/persist_research_bundle.py` with `acquisition_method` for each source or an equivalent supported provider path. Do not write a custom schema-specific persistence script during normal research.
4. [DETERMINISTIC] Deduplicate syndicated reviews and identify source/sample limitations.
5. [AI] Extract aspect-level strengths, weaknesses, complaints, desired outcomes, switching reasons, and exact comparison language. Keep direct evidence separate from interpretation.
6. [HYBRID] Separate high-frequency minor issues from lower-frequency severe decision drivers; label frequency claims according to the actual preserved sample rather than implying market-wide prevalence.
7. [AI] Compare across competitors and relevant customer segments where evidence permits.
8. [HYBRID] Publish competitor-specific Insights only when the preserved evidence chain supports them; otherwise keep them `candidate`. Contribute broader customer-market observations to Customer Intelligence without claiming our customers share them.
9. [DETERMINISTIC] Run research-evidence/business validation before calling the job complete. Candidate opportunities may follow from the evidence, but new active-business promises/services/guarantees require business-specific feasibility and authorization.
