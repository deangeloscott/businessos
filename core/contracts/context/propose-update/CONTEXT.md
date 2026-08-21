---
id: core.context.propose-update
type: playbook
version: 1.1.0
owner_system: core
risk: medium
autonomy_ceiling: 2
reads:
- Observation
- Insight
- Learning
writes:
- ContextUpdateProposal
- Approval
capabilities:
  required:
  - none
  optional:
  - none
context:
- AudienceSegment
- Brand
- Business
- EconomicContext
- Market
- Objective
- Offer
- ProductService
---
# Propose Canonical Context Update

## Purpose
Convert evidence that conflicts with or materially extends canonical Business Context into a controlled proposed change.

## Business Outcome
Keep canonical Business Context accurate without allowing downstream systems to silently overwrite business facts, terms, positioning, or policy.
## Run When
When a specialized system finds credible evidence that a Business, Brand, Offer, Audience, Market, Objective, Economics, or Constraint fact should change.

## Process
1. [AI] Identify the exact context field/object, current value, proposed value, and why the distinction matters operationally.
2. [HYBRID] Link evidence and separate confirmed fact, inference, preference, and learned performance behavior.
3. [HYBRID] Determine whether the proposed change is factual synchronization, business decision, brand decision, commercial term, or policy/compliance change.
4. [DETERMINISTIC] Apply authorization policy; business decisions/terms/policy changes require the appropriate authority rather than automated overwrite.
5. [AI] Identify downstream objects/contracts materially dependent on the current value.
6. [DETERMINISTIC] Persist a ContextUpdateProposal with status and Approval requirement. Apply no canonical context change until the required authority approves it; notify dependents only after the approved change is applied.
