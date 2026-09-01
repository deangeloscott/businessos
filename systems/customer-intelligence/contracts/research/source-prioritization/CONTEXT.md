---
id: customer.research.source-prioritization
type: playbook
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
- Insight
writes: []
capabilities:
  required:
  - none
  optional:
  - crm.opportunity.read
  - crm.activity.read
  - sales_call.read
  - support.ticket.read
  - survey.read
  - review.read
  - community.read
  - social.listen
  - analytics.read
  - research.web.read
context:
- AudienceSegment
- Objective
---
# Customer Evidence Source Prioritization

## Purpose
Choose the customer evidence sources most capable of answering a specific question before collecting more data.

## Business Outcome
Reduce redundant research while favoring direct, decision-relevant customer evidence.

## Run When
Run when several customer data sources are available or a research plan must choose what to inspect first.

## Process
1. [AI] Translate the research question into the type of evidence required: stated motive, behavior, outcome, language, friction, or preference.
2. [AI] Rank existing sources by directness, relevance, coverage, freshness, and known bias for that fact type.
3. [DETERMINISTIC] Check whether current canonical observations already satisfy the evidence requirement.
4. [AI] Prefer first-party direct evidence for customer-specific claims while using behavioral evidence to test stated claims.
5. [AI] Use public/community evidence to broaden discovery without assuming public posters represent the full customer base.
6. [HYBRID] Identify privacy, consent, access, or identity-linkage constraints before collection.
7. [AI] Return the smallest source set likely to resolve the decision and a fallback order if access fails.
