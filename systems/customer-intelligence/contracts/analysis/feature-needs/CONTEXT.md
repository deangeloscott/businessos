---
id: customer.analysis.feature-needs
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
# Customer Feature Need Analysis

## Purpose
Interpret feature requests as evidence of underlying customer needs, workflows, and desired outcomes.

## Business Outcome
Help the business understand what problem customers are trying to solve before treating requests as roadmap instructions.

## Run When
Run when feature requests or capability complaints accumulate or materially affect buying/retention.

## Process
1. [AI] Group feature requests by requested capability, user context, underlying problem, workaround, and desired outcome.
2. [AI] Separate direct request frequency from business/customer impact and from request-vocality bias.
3. [AI] Identify different requested solutions that appear to solve the same underlying job.
4. [DETERMINISTIC] Compare evidence across segments, lost deals, churn, support burden, usage, and successful workarounds where available.
5. [AI] Test whether the need can be addressed through product, service, process, education, integration, or expectation setting.
6. [HYBRID] Keep Product/roadmap decisions outside Customer Intelligence; publish evidence and downstream proposals only.
7. [AI] Create/update need Insights with source/evidence scope and affected audience/product references.
