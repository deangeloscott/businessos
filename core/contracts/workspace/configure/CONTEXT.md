---
id: core.workspace.configure
type: service
version: 1.1.0
owner_system: core
reads: []
writes: []
capabilities:
  required:
  - none
  optional:
  - none
---
# Configure AURA Workspace

## Purpose
Configure where organization-owned ViralTrac AURA state lives and which deployment experience is being used without changing AURA's operating semantics or making Git, Obsidian, or hosted infrastructure mandatory.

## Business Outcome
Give individuals and organizations a clean, upgradeable place for durable state, versioning, collaboration, and human knowledge while preserving zero-configuration download/unzip use.

## Run When
Run during deployment/onboarding, when moving state out of the product folder, when setting up a private versioned/team workspace, or when the user asks how AURA/BusinessOS should be stored across devices or collaborators.

## Process
1. [AI] Determine whether the requested deployment is `simple`, `power_user`, or `organization`; do not force an external workspace when the user only wants local download/unzip use.
2. [HYBRID] Inspect `scripts/workspace_status.py` and determine whether the current workspace already contains durable business state before selecting a different root.
3. [HYBRID] Select the target workspace location and knowledge preference. Treat private Git/GitHub/GitLab/Forgejo, Obsidian, and hosted services as optional adapters rather than AURA dependencies.
4. [DETERMINISTIC] If moving a populated workspace, run `scripts/migrate_workspace.py <target> --profile <profile>` so `instances/`, `runtime/`, `knowledge/`, and `attachments/` are conflict-checked, copied, hash-verified, and retained at the source. Do not replace this with a partial/manual state move.
5. [DETERMINISTIC] If configuring a new/empty workspace, run `scripts/configure_workspace.py <workspace-path> --profile <profile>` or use `BUSINESSOS_WORKSPACE` when the host should control the path without a local pointer.
6. [DETERMINISTIC] Re-run `scripts/workspace_status.py` and confirm `instances/`, `runtime/`, `knowledge/`, and `attachments/` resolve to the intended workspace while product contracts/schemas remain under the AURA distribution.
7. [HYBRID] If Git/versioning is desired, keep the workspace repository private/appropriately permissioned, exclude credentials/secrets and ephemeral logs, and leave large/sensitive authoritative data in its governing system when appropriate.
8. [HYBRID] If human knowledge browsing is desired, refresh the human layer through `core.knowledge.refresh-human-layer`; Obsidian may open the resulting ordinary Markdown but is not required.
9. [DETERMINISTIC] Verify a business initialization or bounded Run write to the active workspace rather than silently falling back to product-local state.

## Verification
- Zero-config mode still resolves the product root as the workspace.
- External mode stores active business/run state outside product source.
- A populated workspace cannot be silently switched to an empty target without explicit override or verified migration.
- Workspace migration preserves the old source, rejects different target conflicts, and verifies copied files by content hash before activation.
- Product contracts, schemas, scripts, and packaged templates remain product-owned.
- The workspace can be copied/versioned independently of the product distribution.
- No provider/editor/version-control tool became mandatory.

## Completion Criteria
- The active workspace path/profile is explicit and inspectable, any existing state was migrated safely when required, state writes resolve consistently, and the chosen deployment remains portable and reversible.
