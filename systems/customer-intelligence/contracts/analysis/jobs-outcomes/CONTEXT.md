---
id: customer.analysis.jobs-outcomes
type: playbook
owner_system: customer-intelligence
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
# Customer Job and Desired Outcome Analysis

## Purpose
Identify the progress customers are trying to make and the outcomes they use to judge success.

## Business Outcome
Give downstream systems a customer-grounded understanding of desired progress rather than a feature-centric interpretation.

## Run When
Run when customer needs, desired outcomes, alternatives, or product/service value must be understood.

## Process
1. [AI] Extract situations that trigger action, desired progress, current workaround/alternative, and successful end state from direct evidence.
2. [AI] Separate functional, emotional, social, risk-reduction, and effort/time outcomes only when evidence supports the distinction.
3. [AI] Link requested features or solutions back to the underlying job/outcome they are intended to achieve.
4. [DETERMINISTIC] Compare jobs/outcomes by segment, context, journey stage, and success/failure cases.
5. [AI] Identify constraints and tradeoffs customers accept or reject while pursuing the outcome.
6. [HYBRID] Test whether the job is stable or only an artifact of the current product/category framing.
7. [AI] Publish scoped Customer Insights and exact customer language supporting the outcome.
