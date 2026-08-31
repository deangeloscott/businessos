---
id: customer.research.plan
type: playbook
version: 1.3.0
owner_system: customer-intelligence
reads:
- Insight
- SourceRecord
- Observation
writes:
- WorkRequest
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
# Customer Research Plan

## Purpose
Turn a business decision, uncertainty, or customer hypothesis into a bounded evidence plan.

## Business Outcome
Collect the minimum sufficient customer evidence needed to make the target decision with known confidence and coverage limits.

## Run When
Run before material customer research when the question, population, evidence needs, or stopping rule is not already explicit.

## Process
1. [AI] State the decision to support, the exact customer question, current hypothesis, and what would change the decision.
2. [AI] Define the relevant population, segments, journey stage, geography, time window, and exclusions.
3. [AI] List the evidence types that can directly answer the question and distinguish first-party, behavioral, and public evidence.
4. [HYBRID] Identify likely biases, missing perspectives, privacy constraints, and evidence that could contradict the working hypothesis.
5. [AI] Select collection methods and sequence them from highest-value existing evidence to new research only where needed.
6. [DETERMINISTIC] Define coverage targets, evidence-quality checks, stopping conditions, freshness requirements, and outputs.
7. [AI] Create bounded WorkRequests or collection tasks only for unresolved evidence needs; reuse current canonical evidence first.
