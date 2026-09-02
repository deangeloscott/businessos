---
id: customer.evidence-collection.surveys
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
- Offer
- ProductService
workflows:
  required:
  - customer.research.plan
  - customer.research.sample-design
  - customer.evidence-collection.survey-design
  - customer.evidence-collection.survey-fielding
---
# Survey Intelligence

## Purpose
Analyze structured and open-ended surveys while accounting for sampling and question-design limitations.

## Business Outcome
Reduce uncertainty about customers through survey intelligence, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current survey intelligence and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [HYBRID] Confirm the survey objective, target population, collection method, question wording, sample size, and response-rate limitations.
2. [DETERMINISTIC] Clean invalid/duplicate responses without altering legitimate outliers; preserve respondent segment where permitted.
3. [DETERMINISTIC] Calculate structured response distributions and segment comparisons using appropriate denominators.
4. [AI] Code open-ended responses into themes while retaining verbatim examples and multi-label responses.
5. [HYBRID] Check leading-question, self-selection, nonresponse, and recency bias before interpreting results.
6. [AI] Compare stated attitudes with behavioral/transactional evidence when available.
7. [HYBRID] Update Customer Insights only to the scope the sampling supports and preserve uncertainty.
