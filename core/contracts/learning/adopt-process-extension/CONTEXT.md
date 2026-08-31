---
id: core.learning.adopt-process-extension
type: service
version: 1.0.0
owner_system: core
reads:
- PlaybookEvolutionProposal
- Learning
writes:
- ProcessExtension
capabilities:
  required:
  - none
  optional:
  - none
events:
  consumes:
  - none
  emits:
  - core.object.created
  - core.object.updated
---
# Adopt Business Process Extension

## Purpose
Apply an explicitly approved business-scoped PlaybookEvolutionProposal as a reversible ProcessExtension without modifying the canonical BusinessOS source tree.

## Business Outcome
Make proven business-specific methods durable and automatically reusable while preserving upgradeability and provider/model agnosticism.

## Run When
Run only after the user explicitly approves a proposal whose change kind is `augment_existing` or `new_local_playbook`.

## Do Not Run When
Do not auto-adopt a `canonical_revision`; do not treat a stored sharing/configuration preference as approval.

## Process
1. [DETERMINISTIC] Resolve the proposal and its Learning references and confirm they belong to the active business.
2. [HYBRID] Confirm the proposal is still applicable and has not been superseded/contradicted since it was prepared.
3. [DETERMINISTIC] Run `scripts/adopt_process_extension.py <business-id> <proposal-id> --approve`.
4. [DETERMINISTIC] For `augment_existing`, confirm the target canonical contract exists. For `new_local_playbook`, confirm the local contract ID is unique in this business.
5. [DETERMINISTIC] Validate the ProcessExtension, mark the proposal adopted, and leave the canonical base unchanged.
6. [DETERMINISTIC] Resolve the effective contract/local playbook and verify its extension requirements are visible to capability preflight.
7. [HYBRID] If the extension later becomes incompatible, contradicted, or superseded by canonical BusinessOS, deactivate/retire it rather than deleting history.

## Verification
- Explicit `--approve` was used for adoption.
- Canonical BusinessOS files are unchanged.
- Effective resolution contains the adopted instructions.
- Base risk/approval/evidence controls remain authoritative.
- Required extension capabilities appear in preflight.

## Completion Criteria
- The ProcessExtension is schema-valid, active, reversible, and resolvable for the intended business/scope.
