---
id: core.incident.manage
type: playbook
version: 1.1.0
owner_system: core
risk: high
autonomy_ceiling: 2
reads:
- Incident
- Observation
- ActionPacket
writes:
- Incident
- ActionPacket
- ChangeEvent
- VerificationRecord
- Learning
capabilities:
  required:
  - none
  optional:
  - none
evidence_inputs:
- Business Constraints
---
# Manage Incident

## Purpose
Coordinate detection, containment, correction, verification, communication, and postmortem for material incidents while the domain owns technical diagnosis.

## Business Outcome
Contain and resolve urgent business incidents without losing ownership, evidence, escalation, verification, or post-incident Learning.
## Run When
When a condition meets domain severity thresholds or creates urgent customer/business risk.

## Process
1. [HYBRID] Confirm incident scope/severity, affected subjects, current impact, confidence, and domain owner.
2. [HUMAN] Establish accountable incident authority for severe/high-risk events when policy requires it.
3. [HYBRID] Prioritize containment that limits harm before optimization/root-cause work.
4. [AI] Route domain diagnosis/correction to the owning specialized contract and maintain timeline/evidence.
5. [DETERMINISTIC] Track actions/approvals/changes/verification and incident state.
6. [HYBRID] Confirm restoration/guardrails, communicate status to required stakeholders, and close only when residual risk is explicit.
7. [HYBRID] Produce postmortem/root-cause Learning and prevention Actions without blame-oriented speculation.
