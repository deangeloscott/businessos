---
id: core.action-control.authorize-action
type: playbook
version: 1.8.1
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
Resolve whether a proposed material action is inside the authority actually granted by the user, organization, account/platform, law/compliance requirements, and the current request, while preserving uncertainty rather than inventing permission or a new AURA-owned approval regime.

## Business Outcome
Let authorized work proceed without unnecessary approval ceremony while preventing consequential actions from exceeding real governing boundaries.

## Run When
Before a material external mutation or sensitive customer/business action when authority is not already mechanically clear from the current request and recorded governing state.

## Process
1. [DETERMINISTIC] Resolve the requested Action, mutation scope, required capability/write scope, current-request boundary, and any explicit Approval, prohibition, spending limit, account/platform constraint, legal/compliance requirement, or other recorded governing rule that applies.
2. [AI] Interpret contextual consequence, scale/blast radius, reversibility/rollback, evidence strength, customer/financial/compliance impact, and other business risk relevant to deciding how the authorized action should be carried out. Preserve material uncertainty; do not turn a generic risk label into a permission rule by itself.
3. [DETERMINISTIC + AI] Compare the proposed execution with the real authority sources. Capability is not permission. Preferences/risk tolerance are not permission. When multiple governing authority sources actually apply, honor the most restrictive applicable boundary. Do not invent an additional ceiling merely because AURA would make a more conservative business choice.
4. [HYBRID] Determine the valid current mode: observe/recommend, prepare, execute inside existing authority, or wait for a required approval. A provider preview may supply exact eligibility/constraint evidence but cannot create authority that the user/organization/platform has not granted.
5. [DETERMINISTIC] Create or update Approval only when a real governing rule, selected SOP requirement, or unresolved request boundary requires it. If otherwise useful work is waiting on user approval, input, credential, or capability, create/update one deduplicated AttentionItem when durable attention materially helps; do not manufacture an approval or alert merely for bookkeeping.
6. [DETERMINISTIC] Record the resolved authority state on the Action/Approval without rewriting the underlying Opportunity rationale. Resolve related AttentionItems when the blocker is verified cleared or the action is no longer relevant.

## Verification
- The authorization result cites an actual authority source or explicitly states what authority remains unknown.
- Risk/evidence/reversibility informed the business judgment without silently becoming an AURA-invented permission boundary.
- Capability availability was not treated as authorization.
- Preferences were not treated as authorization.
- No required real approval was bypassed, and no approval was created solely because a generic risk label demanded ceremony.

## Failure / Fallback
- If the governing authority is genuinely ambiguous and the proposed external mutation would exceed clearly granted scope, preserve the Action as prepared/proposed and request only the smallest approval needed to resolve the boundary.
- If useful analysis, drafting, simulation, or other non-mutating work remains inside existing authority, continue that work rather than treating the unresolved external action as a global blocker.
