---
id: customer-optimization.intervention.sales-handoff
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- MetricObservation
writes:
- Asset
- ChangeEvent
capabilities:
  required:
  - none
  optional:
  - analytics.read
  - product_analytics.read
  - crm.contact.read
  - crm.contact.update
  - crm.opportunity.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - email.send
  - workflow.update
context:
- EconomicContext
- Offer
---
# Sales Handoff Optimization

## Purpose
Reduce delay, context loss, ownership ambiguity, duplicate outreach, and customer effort when a real qualified lead/customer moves between sales people or operational systems.

## Business Outcome
Improve customer progression and sales continuity through a clearer real-world handoff process without confusing AURA's organizational memory with the CRM/workflow runtime that performs assignment and notification.

## Run When
Use when evidence shows a sales handoff is materially harming a defined journey transition or when the organization wants to design/improve that real operational handoff. An existing Opportunity may provide context but is not required.

## Process
1. [HYBRID] Map the actual business handoff: triggering condition, source/receiving role or system, assignment logic, required context, customer expectation, acceptance/reassignment, first-contact target, and failure/recovery path.
2. [HYBRID] Measure or inspect latency, unassigned/reassigned cases, missing context, duplicate outreach, customer wait/repetition, and downstream outcomes using the strongest available operational evidence.
3. [AI] Use sales/customer evidence to identify where handoff confusion, expectation mismatch, poor qualification, missing data, process design, capacity, or salesperson behavior is the likely mechanism.
4. [AI] Distinguish problems that should be solved in the handoff design from training, staffing, offer, customer-understanding, or other business issues. Do not turn every sales problem into routing logic.
5. [AI] Define the smallest useful handoff design: ownership rule, minimum context, customer-facing expectation, service target where justified, fallback/escalation owner, and what should happen on acceptance/failure. Avoid unnecessary rules that make the process brittle.
6. [HYBRID] Preserve the design as an internal `Asset` when future operators/models benefit from it. If the user wants the real process changed and the active harness has the required CRM/workflow capabilities and real permissions, make those external changes directly; AURA does not create a generic approval gate or internal WorkRequest first.
7. [HYBRID] When a material operational change is actually made, preserve a `ChangeEvent` only if later evaluation/continuity benefits from knowing what changed, when, and why. Do not create a ChangeEvent for a draft recommendation.
8. [AI] Define what later evidence would show whether the handoff improved customer/sales outcomes. Use separate measurement/evaluation work when that evidence becomes available rather than manufacturing an Experiment or OutcomeEvaluation during design.

## Verification
- This playbook concerns a real business handoff, not model/subagent/domain routing inside AURA.
- Customer context transfer is limited to what the receiving actor actually needs and respects real privacy/contractual constraints.
- Proposed service/routing rules are justified by business/customer evidence rather than needless process complexity.
- Recommendations, external changes actually executed, and later outcomes remain separate facts.

## Completion Criteria
- The organization has either a clear evidence-backed handoff design or an implemented real-world handoff improvement, with enough durable context to understand the change later and no AURA-owned assignment/notification runtime.
