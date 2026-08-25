# Portable-First Requirement

ViralTrac's BusinessOS is a portable ICM-style operating workspace. This is a hard architectural invariant.

## Required invariant
A complete or standalone Business OS distribution must remain usable from its files without requiring a proprietary Business OS server, database, hosted control plane, UI, scheduler, vector store, version-control provider, second-brain application, or other optional infrastructure merely to understand and perform supported work.

The default operating model is:

```text
BusinessOS product + active workspace + business instance + capable AI/agent + workflow-required capabilities
```

- With no special configuration, the BusinessOS product root is also the active workspace. Download/unzip-and-use remains the zero-configuration default.
- An organization may instead configure a separate external workspace with `BUSINESSOS_WORKSPACE` or the local untracked `.businessos/workspace.json` pointer created by `scripts/configure_workspace.py`.
- `instances/<business-id>/` is the logical portable store for durable business context and canonical BusinessOS objects whether the workspace is inside or outside the product tree.
- `runtime/runs/<business-id>/<run-id>/` is the logical portable store for bounded run state and working artifacts.
- `knowledge/<business-id>/` is an optional human-readable Markdown view/notes area. It does not replace canonical JSON state and does not require Obsidian or any other editor.
- `attachments/` is an optional workspace-owned file area; large, high-volume, sensitive, or externally authoritative data may remain in the governing external system.
- External systems may remain systems of record for raw/large/sensitive data; preserve canonical references and permitted derived intelligence instead of copying everything into the workspace.
- External capabilities are workflow dependencies, not dependencies of the BusinessOS architecture itself. If a requested activity intrinsically needs a capability the current host does not have, use capability preflight and the allowed provider/manual fallback rather than making the workspace unusable.
- Git/GitHub/GitLab/Forgejo, Obsidian, hosted control planes, remote storage, schedulers, and custom UIs may improve scale, history, collaboration, retrieval, durability, or human experience, but they must remain adapters/enhancements around the same contracts and workspace semantics.

## Product/workspace separation
The BusinessOS distribution owns `core/`, `systems/`, `scripts/`, schemas, tests, packaged templates, and distribution metadata. Organization/user state owns `instances/`, `runtime/`, optional `knowledge/`, optional `attachments/`, and business-scoped extensions. Upgrading product source should not require an organization to fork or relocate its workspace merely to preserve state.

## Design test for future changes
Before adding a mandatory dependency, ask: **Can a recipient still copy/unzip BusinessOS, initialize a business, route a supported task, follow the process, persist work in the default local workspace, and produce a usable result when the workflow's intrinsic capabilities are available or handled by fallback?**

If no, the change violates portable-first unless it is explicitly an optional adapter.
