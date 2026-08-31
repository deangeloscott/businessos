---
id: customer.research.sample-design
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- SourceRecord
- Observation
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
# Customer Research Sample Design

## Purpose
Select research participants or records that represent the decision population and useful contrast cases.

## Business Outcome
Produce customer research samples that support valid comparisons rather than convenient anecdotes.

## Run When
Run when interviews, surveys, win/loss, churn, adoption, or other customer research requires selecting cases.

## Process
1. [AI] Define the population and the attributes that could materially change the answer.
2. [DETERMINISTIC] Build the available sampling frame and identify known coverage gaps.
3. [AI] Select required contrast groups such as wins/losses, retained/churned, successful/unsuccessful, new/mature, or segment differences.
4. [HYBRID] Choose purposive, stratified, random, census, or mixed sampling based on the decision rather than default convenience.
5. [AI] Identify likely selection and survivorship biases and add cases that can expose them.
6. [DETERMINISTIC] Define target coverage and stopping logic using information sufficiency, not a universal sample-size rule.
7. [AI] Document who is included/excluded and what the resulting sample cannot support.
