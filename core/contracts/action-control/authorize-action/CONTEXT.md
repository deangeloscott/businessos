---
id: core.action-control.authorize-action
type: playbook
version: 1.8.0
owner_system: core
risk: medium
autonomy_ceiling: 2
reads:
- ActionPacket
- Approval
- CapabilityBinding
writes:
- Approval
- ActionPacket
- AttentionItem
capabilities:
  required:
  - none
  optional:
  - business.action.governed.preview
evidence_inputs:
- Business Constraints
---
# Authorize Action

## Purpose
Calculate effective action authorization from capability, autonomy, risk, permissions, evidence, compliance, scale, reversibility, and approval requirements.

## Business Outcome
Allow material actions only when capability, permission, risk, reversibility, autonomy, and required approval permit them.
## Run When
Before any material external mutation or sensitive customer/business action.

## Process
1. [DETERMINISTIC] Resolve requested Action, required capability, business/domain permissions, and capability write scope.
2. [HYBRID] Evaluate risk, scale/blast radius, reversibility/rollback, confidence/evidence, customer/financial/compliance impact.
3. [DETERMINISTIC] Apply the most restrictive autonomy ceiling across Core, business, domain, Action, capability, and approval policy.
4. [HYBRID] Determine authorized executor/mode: observe, recommend, prepare, execute with approval, or autonomous execution. A provider preview may supply eligibility/constraint evidence, but it cannot raise the BusinessOS autonomy ceiling or replace required business/user approval.
5. [DETERMINISTIC] Require/create Approval when policy demands it and block execution until conditions are satisfied. If an otherwise ready material action is waiting on user approval, input, credential, or capability, create/update one deduplicated AttentionItem rather than silently stopping or repeatedly alerting.
6. [DETERMINISTIC] Record authorization decision on the Action/Approval without modifying the underlying Opportunity rationale. Resolve the related AttentionItem when the blocker is verified cleared or the action is no longer relevant.
