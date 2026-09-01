---
id: customer.evidence-collection.communities
type: playbook
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes:
- SourceRecord
- Observation
- Insight
capabilities:
  required:
  - community.read
  optional:
  - crm.contact.read
  - analytics.read
context:
- AudienceSegment
- Market
- Offer
- ProductService
---
# Community & Social Listening

## Purpose
Discover emerging customer language, questions, alternatives, and concerns from public communities without treating unverified posters as representative customers.

## Business Outcome
Reduce uncertainty about customers through community & social listening, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current community & social listening and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [HYBRID] Define relevant communities/queries and inclusion rules tied to the active audience/category rather than broad vanity monitoring.
2. [INTEGRATION] Retrieve public posts/comments with date, context, thread relationship, and source reference.
3. [AI] Determine whether the speaker plausibly represents the target market; preserve uncertainty where identity/experience is unknown.
4. [AI] Extract recurring questions, pains, alternatives, desired outcomes, misconceptions, and native terminology.
5. [DETERMINISTIC] Cluster near-duplicate topics and measure recurrence/freshness without counting reposts as independent evidence.
6. [HYBRID] Treat community evidence as exploratory unless corroborated by stronger/direct customer evidence.
7. [HYBRID] Publish observations and candidate Insights; request validation when a theme could materially change strategy.
