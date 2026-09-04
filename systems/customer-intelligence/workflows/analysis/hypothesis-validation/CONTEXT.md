---
id: customer.analysis.hypothesis-validation
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
# Customer Hypothesis Validation

## Purpose
Test a strategically important belief about customers before future decisions or work build on it.

## Business Outcome
Reduce uncertainty about customers through customer hypothesis validation, so future decisions reflect current customer evidence rather than assumption.

## Run When
Run when a decision requires current customer hypothesis validation and existing Customer Insights are missing, stale, too broad, or insufficiently supported.

## Process
1. [AI] State the hypothesis precisely with scope, predicted observable evidence, and what would contradict it.
2. [HYBRID] Inventory existing direct and indirect evidence and grade its relevance/source quality.
3. [AI] Identify the minimum additional evidence needed to discriminate among plausible explanations.
4. [HYBRID] Select method: interview, survey, win/loss, behavior, support/review mining, experiment result, or mixed evidence.
5. [HYBRID] Collect/analyze the evidence without changing the hypothesis after seeing results.
6. [AI] Compare observed evidence with predictions and alternative explanations.
7. [HYBRID] Confirm, narrow, weaken, contradict, or leave unresolved; update the relevant Insight and confidence.
