---
id: core.learning.adopt-process-extension
type: playbook
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
---
# Adopt Business Process Extension

## Purpose
Make an intentionally selected, business-scoped PlaybookEvolutionProposal available as reusable AURA operational knowledge without modifying canonical AURA source.

## Business Outcome
Preserve useful organization-specific methods for future intelligence while keeping those methods optional, inspectable, reversible, and provider/model/harness neutral.

## Run When
Run when the organization/model/user has intentionally chosen to persist a business-scoped `augment_existing` or `new_local_playbook` proposal as active operational knowledge.

## Do Not Run When
Do not adopt a `canonical_revision` through this path. Do not infer that an extension must be used merely because it is stored or active.

## Process
1. [DETERMINISTIC] Resolve the proposal and Learning references and confirm they belong to the active business.
2. [HYBRID] Confirm the proposal is still applicable and has not been superseded/contradicted since it was prepared.
3. [DETERMINISTIC] Run `scripts/adopt_process_extension.py <business-id> <proposal-id>`.
4. [DETERMINISTIC] For `augment_existing`, confirm the target canonical playbook exists. For `new_local_playbook`, confirm the local ID is unique. Validate any declared read/write object types and provider-neutral capability IDs as real AURA vocabulary; do not treat the base playbook's declarations as a permission boundary.
5. [DETERMINISTIC] Validate the ProcessExtension, mark the proposal adopted, and leave canonical AURA source unchanged.
6. [DETERMINISTIC] Resolve the effective playbook/local playbook and verify its instructions and provider-neutral capability needs remain visible.
7. [HYBRID] If later evidence contradicts the extension, or canonical AURA supersedes it, narrow/deactivate/retire it while preserving useful history.

## Verification
- No Approval/risk/autonomy/provider-binding state was created.
- Canonical AURA files are unchanged.
- Effective resolution contains the adopted operational knowledge.
- Read/write and capability declarations remain descriptive rather than runtime permissions or gates.
- The extension remains optional to the executing intelligence unless the user explicitly selected that AURA method for the task.

## Completion Criteria
The ProcessExtension is schema-valid, active, reversible, and useful as organization-owned operational knowledge without becoming execution authority.
