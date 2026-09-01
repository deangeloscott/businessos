---
id: customer.analysis.decision-drivers
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
# Customer Decision Driver Analysis

## Purpose
Identify the factors and evidence-backed motivations that materially influence customer choice and how their importance varies by context.

## Business Outcome
Provide evidence-backed buying criteria, motivations, and tradeoffs that improve marketing, sales, product, and customer decisions without reducing customers to generic persuasion labels.

## Run When
Run when the business needs to understand why customers choose, reject, switch, delay, expand, stay, or leave.

## Process
1. [AI] Combine direct decision evidence from interviews, win/loss, sales/support conversations, reviews, public discussion, and behavior where relevant.
2. [AI] Separate stated preferences/language from factors demonstrably present in actual decisions and from analyst interpretation.
3. [AI] Identify triggers, must-haves, tradeoffs, proof requirements, alternatives, constraints, disqualifiers, and the customer progress/job at stake.
4. [DETERMINISTIC] Compare drivers across wins/losses, segments, awareness/knowledge states, journey/lifecycle stages, channels/situations, and deal/customer outcomes where evidence permits.
5. [AI] Test competing explanations such as price, timing, fit, trust, risk, implementation, status quo, desired gain, loss avoidance, certainty/control, speed, simplicity/effort, financial outcome, status/identity, autonomy, belonging, or convenience. Treat these as evidence-tested mechanisms, not a checklist that must be filled.
6. [HYBRID] Scope each driver/motivation to the population and evidence that support it; avoid universal ranking, personality profiling, or sensitive-trait inference.
7. [AI] Create/update Customer Insights with evidence links, confidence/contradictions, applicable decision context, and downstream relevance signals.
