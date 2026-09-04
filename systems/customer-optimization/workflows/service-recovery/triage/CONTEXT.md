---
id: customer-optimization.service-recovery.triage
type: workflow
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
3. [HYBRID] Assign the correct real operational/human owner and prioritize containment/restoration before explanation or persuasion.
4. [AI] Define the immediate customer communication: acknowledgment, known facts, next action/owner, expected update—not unsupported cause or promise.
5. [DETERMINISTIC] Track containment/resolution actions, timestamps, commitments, and customer state in the real service/operational system where that work lives.
6. [AI] After stabilization determine remediation/follow-up appropriate to harm and policy without inventing compensation authority.
7. [HYBRID] Preserve the systemic question/evidence and use root-cause/prevention operating knowledge directly when follow-up is useful. Create a WorkRequest only when a real durable handoff to another actor must survive the current interaction.
