---
id: customer.intelligence.ecosystem-radar
type: playbook
version: 1.0.0
owner_system: customer-intelligence
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
writes:
- Observation
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - customer_feedback.read
  - crm.opportunity.read
  - crm.activity.read
  - sales_call.read
  - support.ticket.read
  - survey.read
  - review.read
  - community.read
  - social.listen
context:
- Business
- AudienceSegment
- Market
- Objective
- ProductService
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: customer.analysis.insight-refresh
    when: New evidence may strengthen, narrow, contradict, or supersede an existing Customer Insight.
  - id: customer.learning.domain-learning
    when: Repeated evidence/outcomes justify reusable guidance about customer research methods or evidence reliability.
---
# Customer Signal Ecosystem Radar

## Purpose
Detect changing customer needs, language, objections, expectations, desired outcomes, category behaviors, and use cases from external and first-party evidence without mistaking market conversation for active-customer truth.

## Business Outcome
Keep customer understanding current enough to improve product, marketing, sales, and customer decisions while preserving segment, source, and evidence boundaries.

## Run When
Run from the Core ecosystem radar, on demand for customer-signal refresh, or when external/first-party evidence suggests customer behavior or expectations may be changing.

## Process
1. [HYBRID] Reuse current Customer Insights, evidence coverage, segments, source profiles, and recent first-party/public observations before launching new retrieval.
2. [AI] Discover signals across reviews, communities, social discussion, research, category conversations, sales/support/survey evidence when available, and adjacent emerging use cases using semantic as well as known-source discovery.
3. [HYBRID] Preserve direct statements as Observations and use Core triangulation to distinguish independent customer evidence from reposted narratives, influencer interpretation, survey/report repetition, and speculation.
4. [AI] Separate expressed customer language/behavior from inferred motivation, and test whether apparent change is actually segment, market, journey-stage, time, channel, or method composition.
5. [HYBRID] Compare external-market signals with active-business first-party evidence when the decision requires applicability; external prevalence does not establish that the business's customers share the same pattern.
6. [HYBRID] Refresh existing Customer Insights when evidence strengthens/narrows/contradicts them; create a bounded research WorkRequest when interviews, surveys, or deeper evidence are needed.
7. [AI] Route implications to Product/Marketing/Content/Customer Optimization through cross-system relevance rather than embedding downstream recommendations as customer facts.
8. [DETERMINISTIC] Preserve contradiction/history and update customer domain Learning only for reusable research/evidence guidance supported by repeated outcomes or corrections.

## Verification
- Customer observation, interpretation, and business applicability are distinct.
- Frequency claims remain scoped to measured or sampled populations.

## Completion Criteria
- Material customer changes are evidence-backed, segment-scoped, freshness-aware, and routed to the correct owner.
