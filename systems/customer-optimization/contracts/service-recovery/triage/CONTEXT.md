---
id: customer-optimization.service-recovery.triage
type: playbook
owner_system: customer-optimization
reads:
- CustomerJourney
- Observation
- Insight
- Opportunity
- MetricObservation
- Experiment
writes:
- Observation
- Insight
- Opportunity
capabilities:
  required:
  - analytics.read
  optional:
  - product_analytics.read
  - crm.contact.read
  - crm.opportunity.read
  - checkout.read
  - billing.read
  - support.ticket.read
  - customer_success.read
  - scheduling.read
  - experiment.run
  - workflow.update
  - email.send
context:
- AudienceSegment
- Offer
- Objective
- EconomicContext
---
# Service Recovery Triage

## Purpose
Stabilize an active customer failure by understanding impact, urgency, ownership, and immediate next action.

## Business Outcome
Restore customer progress/trust quickly while preserving evidence for systemic prevention.

## Run When
Run when a customer experiences a material service/product/process failure, complaint, or incident affecting value.

## Process
1. [DETERMINISTIC] Capture customer/account, issue, first observed/time, affected outcome, severity, current state, prior attempts, and evidence without making customer repeat known information.
2. [AI] Classify immediate customer impact and whether safety/security/legal/financial/critical operational escalation applies.
3. [HYBRID] Assign the correct operational/human owner and prioritize containment/restoration before explanation or persuasion.
4. [AI] Define the immediate customer communication: acknowledgment, known facts, next action/owner, expected update—not unsupported cause or promise.
5. [DETERMINISTIC] Track containment/resolution actions, timestamps, commitments, and customer state.
6. [AI] After stabilization determine remediation/follow-up appropriate to harm and policy without inventing compensation authority.
7. [DETERMINISTIC] Create systemic root-cause/prevention work and link customer outcome.
