---
id: customer.analysis.buying-criteria
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
# Buying Criteria & Trigger Analysis

## Purpose
Determine which criteria and events materially shape customer decisions.

## Business Outcome
Reduce uncertainty about customers through buying criteria & trigger analysis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current buying criteria & trigger analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] Extract explicit comparison criteria, must-haves, tradeoffs, approval criteria, and triggering events from qualified customer evidence.
2. [HYBRID] Distinguish screening criteria, differentiating criteria, veto criteria, and nice-to-have preferences.
3. [DETERMINISTIC] Compare occurrence and win/loss association by segment/offer where data volume permits.
4. [AI] Identify temporal triggers such as contract renewal, growth, failure event, regulation, leadership change, or budget cycle.
5. [HYBRID] Check whether criteria differ by buying role and stage; avoid assuming one respondent represents the buying committee.
6. [AI] Map alternatives customers use when the business is not selected.
7. [HYBRID] Create/update Customer Insights with scope/confidence and downstream relevance tags.
