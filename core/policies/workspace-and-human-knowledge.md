# AURA Workspace and Human Knowledge Layer

ViralTrac AURA separates **product source**, **organization-owned operating state**, **human knowledge views**, and **external authoritative data**. This separation improves deployment, upgrades, collaboration, and human usability without changing the meaning of canonical BusinessOS objects.

## 1. Product source vs organization workspace
- `core/`, `systems/`, `scripts/`, schemas, tests, distribution metadata, and packaged templates belong to the AURA product distribution.
- Durable active-business state belongs to the active AURA workspace.
- With no workspace configuration, the product root is also the workspace root; this preserves download/unzip-and-use behavior.
- An external workspace may be selected with the compatibility variable `BUSINESSOS_WORKSPACE` or the local untracked `.businessos/workspace.json` pointer created by `scripts/configure_workspace.py`.
- Configuring an external workspace must not copy or fork canonical AURA product source into that workspace merely to make state portable.
- If the current workspace contains business state that is absent from a new target, do not silently switch roots. Use `scripts/migrate_workspace.py` or an explicitly authorized intentional state switch.

## 2. Active workspace namespaces
The active workspace owns these logical namespaces:
- `instances/<business-id>/` — canonical durable business state.
- `runtime/runs/<business-id>/<run-id>/` — bounded execution/recovery state.
- `knowledge/<business-id>/` — human-facing derived views and clearly labeled human notes.
- `attachments/` — optional workspace-owned files that are appropriate to keep locally; large/sensitive/system-owned data may remain external.

Logical refs remain workspace-relative (`instances/...`, `runtime/...`) even when the physical workspace is elsewhere on disk. Do not persist absolute host paths when a portable workspace-relative ref is available.

## 3. Workspace migration
A workspace move is state migration, not a product fork.
- Preflight the target for non-identical conflicts before copying.
- Migrate organization-owned namespaces, not product source or `instances/_template/`.
- Copy non-destructively; source state remains intact.
- Verify every migrated file by content hash before activating the target workspace.
- Re-running migration over identical content must be safe/idempotent.
- If a host-level `BUSINESSOS_WORKSPACE` environment variable overrides local pointers, report the required host change rather than claiming to have changed the parent process.
- Do not delete the old workspace as part of migration. Retirement/deletion is a separate explicit human/administrator decision after the target has been validated.

## 4. Human knowledge is a view, not parallel truth
- Canonical JSON objects remain authoritative for AURA/BusinessOS state.
- `knowledge/<business-id>/_generated/` is generated from canonical objects and may be regenerated at any time.
- `knowledge/<business-id>/notes/` is for human-authored working notes. Notes are non-canonical until evidence/truth governance explicitly incorporates their contents into canonical objects.
- Registering a human note creates provenance-backed source material; it does not automatically promote the note's statements to Business, Observation, Insight, Learning, or other canonical truth.
- A generated Markdown summary, Obsidian page, dashboard, or future UI must not silently become an independent competing truth store.
- Generated pages should preserve canonical IDs/source refs so humans and agents can trace the underlying state.

## 5. Obsidian and other second-brain tools
Obsidian, VS Code, file browsers, Markdown editors, and future interfaces may open the knowledge directory directly because it contains ordinary portable Markdown. No editor-specific format is required. Editor metadata/configuration may exist locally but must not become an AURA dependency.

## 6. Git/version-control boundary
Git is recommended but optional for users who need history, rollback, multi-device synchronization, or team collaboration.
- A private GitHub/GitLab/Forgejo/self-hosted repository may contain an organization workspace.
- Do not require Git for Simple deployments.
- Do not commit credentials, API keys, tokens, private keys, or raw secret files.
- Large, high-volume, sensitive, or externally authoritative data should usually remain in the governing external system; store permitted references, provenance, bounded snapshots, or derived intelligence instead.
- Runtime logs and ephemeral files need not be versioned merely because the workspace itself is versioned.

## 7. Deployment profiles
AURA exposes three human-facing deployment concepts in `distribution/deployment-profiles.json`:
1. `simple` — download/unzip and use locally.
2. `power_user` — separate organization workspace, optional private Git/versioning, optional second-brain interface.
3. `organization` — separate private team workspace, controlled collaboration/versioning, optional human knowledge interface.

These are deployment experiences, not separate editions with different operating semantics.

## 8. Upgrade rule
Upgrading AURA product source must not require moving or rewriting organization state merely because product files changed. Business-scoped `ProcessExtension` objects and other organization state remain in the workspace. Product migrations may be required when schemas intentionally change, but the workspace remains organization-owned and separately recoverable.

The public product name is ViralTrac AURA; “BusinessOS” remains a descriptor and compatibility namespace where needed. See `BRANDING.md`.
