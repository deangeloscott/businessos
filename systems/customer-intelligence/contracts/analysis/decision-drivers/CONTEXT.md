---
id: customer.analysis.decision-drivers
type: playbook
version: 1.3.0
owner_system: customer-intelligence
risk: low
autonomy_ceiling: 2
reads:
- Observation
- Insight
writes:
- Insight
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
# Customer Decision Driver Analysis

## Purpose
Identify the factors that materially influence customer choice and how their importance varies by context.

## Business Outcome
Provide evidence-backed buying criteria and tradeoffs that improve marketing, sales, product, and customer decisions.

## Run When
Run when the business needs to understand why customers choose, reject, switch, or delay.

## Process
1. [AI] Combine direct decision evidence from interviews, win/loss, sales conversations, reviews, and behavior where relevant.
2. [AI] Separate stated preferences from factors demonstrably present in actual decisions.
3. [AI] Identify triggers, must-haves, tradeoffs, proof requirements, alternatives, constraints, and disqualifiers.
4. [DETERMINISTIC] Compare drivers across wins/losses, segments, journey stages, and deal/customer outcomes.
5. [AI] Test competing explanations such as price, timing, fit, trust, risk, implementation, and status quo.
6. [HYBRID] Scope each driver to the population/evidence that supports it and avoid universal ranking without evidence.
7. [AI] Create/update Customer Insights with evidence links and downstream relevance signals.
