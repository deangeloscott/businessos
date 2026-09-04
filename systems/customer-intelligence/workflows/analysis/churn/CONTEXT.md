---
id: customer.analysis.churn
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
# Churn Reason Analysis

## Purpose
Understand customer-stated and evidenced reasons for leaving without conflating correlation with customer motivation.

## Business Outcome
Reduce uncertainty about customers through churn reason analysis, so downstream decisions reflect current customer evidence rather than assumption.

## Run When
Use when a decision requires current churn reason analysis and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [DETERMINISTIC] Define churn event/cohort, voluntary vs involuntary where relevant, segment, tenure, product/offer, and analysis window.
2. [INTEGRATION] Gather cancellation reasons, exit interviews, support history, success notes, usage summaries, billing events, and renewal communications. Draw on evidence-coverage operating knowledge when it materially improves source completeness.
3. [AI] Extract customer-stated reasons, unmet outcomes, expectation gaps, alternatives, triggers, and language. Theme-coding and decision-driver methods may be useful when the evidence volume/decision warrants them; they are not required stages.
4. [HYBRID] Separate stated reasons from behavioral predictors and operational/lifecycle evidence.
5. [DETERMINISTIC] Compare churn reasons across tenure/segment/cohort while reporting missing exit-feedback coverage.
6. [AI] Identify multi-cause patterns and contradictions between stated reasons and preceding experience.
7. [HYBRID] Preserve Customer Insights and any lifecycle-friction evidence that future work will materially benefit from. Customer Optimization operating knowledge may use the same organizational evidence directly when relevant; do not create an internal AURA handoff merely to cross domains.
