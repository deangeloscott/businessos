---
id: customer.analysis.language
type: workflow
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
context:
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
---
# Customer Language & Terminology

## Purpose
Maintain how customers naturally describe problems, outcomes, products, alternatives, and category concepts.

## Business Outcome
Reduce uncertainty about customers through customer language & terminology, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current customer language & terminology and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Gather direct language from relevant customer sources and preserve verbatim source references.
2. [DETERMINISTIC] Normalize punctuation/case only for clustering while retaining raw wording.
3. [AI] Group synonyms, category terms, slang, technical/nontechnical phrasing, problem phrases, desired-outcome phrases, and objection language.
4. [HYBRID] Compare language by segment, awareness, role, market/language, and stage.
5. [AI] Detect terminology the business uses that customers rarely use or interpret differently.
6. [HYBRID] Distinguish prevalence from memorability and current usage from emerging usage.
7. [HYBRID] Publish Customer Insights/Business Context proposals where language should materially affect communication or positioning.
