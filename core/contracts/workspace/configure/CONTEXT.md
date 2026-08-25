---
id: core.workspace.configure
type: service
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 3
reads: []
writes: []
capabilities:
  required:
  - none
  optional:
  - none
---
# Configure BusinessOS Workspace

## Purpose
Configure where organization-owned BusinessOS state lives and which deployment experience is being used without changing the operating semantics of BusinessOS or making Git, Obsidian, or hosted infrastructure mandatory.

## Business Outcome
Give individuals and organizations a clean upgradeable place for durable state, versioning, collaboration, and human knowledge while preserving zero-configuration download/unzip use.

## Run When
Run during deployment/onboarding, when moving state out of the product folder, when setting up a private versioned/team workspace, or when the user asks how BusinessOS should be stored across devices or collaborators.

## Process
1. [AI] Determine whether the requested deployment is `simple`, `power_user`, or `organization`; do not force an external workspace when the user only wants local download/unzip use.
2. [HYBRID] Select the workspace location and knowledge preference. Treat private Git/GitHub/GitLab/Forgejo, Obsidian, and hosted services as optional adapters rather than BusinessOS dependencies.
3. [DETERMINISTIC] Run `scripts/configure_workspace.py <workspace-path> --profile <profile>` or use `BUSINESSOS_WORKSPACE` when the host should control the path without a local pointer.
4. [DETERMINISTIC] Inspect `scripts/workspace_status.py` and confirm `instances/`, `runtime/`, `knowledge/`, and `attachments/` resolve to the intended workspace while product contracts/schemas remain under the BusinessOS distribution.
5. [HYBRID] If Git/versioning is desired, keep the workspace repository private/appropriately permissioned, exclude credentials/secrets and ephemeral logs, and leave large/sensitive authoritative data in its governing system when appropriate.
6. [HYBRID] If human knowledge browsing is desired, refresh the human layer through `core.knowledge.refresh-human-layer`; Obsidian may open the resulting ordinary Markdown but is not required.
7. [DETERMINISTIC] Verify a business initialization and bounded Run write to the active workspace rather than silently falling back to product-local state.

## Verification
- Zero-config mode still resolves the product root as the workspace.
- External mode stores active business/run state outside product source.
- Product contracts, schemas, scripts, and packaged templates remain product-owned.
- The workspace can be copied/versioned independently of the product distribution.
- No provider/editor/version-control tool became mandatory.

## Completion Criteria
- The active workspace path/profile is explicit and inspectable, state writes resolve there consistently, and the chosen deployment remains portable and reversible.
