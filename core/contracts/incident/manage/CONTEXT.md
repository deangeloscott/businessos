---
id: core.incident.manage
type: playbook
version: 2.0.0
owner_system: core
reads:
- Incident
- Observation
- DecisionRecord
- ChangeEvent
- VerificationRecord
writes:
- Incident
- WorkRequest
- AttentionItem
- ChangeEvent
- VerificationRecord
- DecisionRecord
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
Coordinate material incident understanding, containment, correction, verification, communication, and learning while the relevant domain/harness owns technical execution.

## Business Outcome
Resolve important incidents quickly without losing organizational truth, ownership, evidence, decisions, or post-incident Learning.

## Run When
When a condition creates material customer, operational, financial, reputational, legal, security, or other business impact that warrants incident-level coordination.

## Process
1. [HYBRID] Establish the incident scope, affected subjects, current impact, confidence, evidence, and responsible domain/owner.
2. [AI] Prioritize the smallest effective containment or information-gathering action that can materially reduce harm or uncertainty.
3. [AI] Route specialized diagnosis/correction to the appropriate real owner. Use a durable WorkRequest only when the handoff itself should survive the current session.
4. [HYBRID] Preserve material changes, verification evidence, and real organizational decisions when future continuity benefits from them. Do not create records merely to mirror tool calls.
5. [HYBRID] Keep stakeholders informed according to actual organizational needs and constraints; use AttentionItem only for a material unresolved condition worth future awareness.
6. [HYBRID] Close the Incident when the organization has sufficient evidence that the incident is resolved or accepted at its current state, with material residual uncertainty explicit.
7. [HYBRID] Produce evidence-supported postmortem/root-cause Learning and prevention recommendations without blame-oriented speculation.

## Verification
- Incident status and claimed resolution are supported by appropriate evidence for the actual consequence.
- Independent verification is used when needed to establish restoration or another important post-state; it is not required as generic ceremony for every intermediate tool action.

## Completion Criteria
- The incident's material facts, actions/results, decisions, residual uncertainty, and Learning are understandable from organization-owned state without requiring an internal authority lifecycle.
