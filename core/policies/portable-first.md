# Portable-First Requirement

**ViralTrac AURA (Agentic Understanding and Reinforcement Architecture)** is a portable, AI-native BusinessOS. This is a hard architectural invariant.

## Required invariant
A complete or standalone AURA/BusinessOS distribution must remain usable from its files without requiring a proprietary server, database, hosted control plane, UI, scheduler, vector store, version-control provider, second-brain application, or other optional infrastructure merely to understand and perform supported work.

The default operating model is:

```text
AURA product + active workspace + business instance + capable AI/agent + whatever real host capabilities the requested work needs
```

- With no special configuration, the AURA product root is also the active workspace. Download/unzip-and-use remains the zero-configuration default.
- An organization may instead configure a separate external workspace with the stable compatibility variable `BUSINESSOS_WORKSPACE` or the local untracked `.businessos/workspace.json` pointer created by `scripts/configure_workspace.py`.
- `instances/<business-id>/` is the logical portable store for durable business context and canonical AURA objects whether the workspace is inside or outside the product tree.
- `runtime/runs/<business-id>/<run-id>/` is an optional logical store for bounded work receipts and any receipt-local artifacts that are actually useful. Ordinary work does not require a Run.
- `knowledge/<business-id>/` is an optional human-readable Markdown view/notes area. It does not replace canonical JSON state and does not require Obsidian or any other editor.
- `attachments/` is an optional workspace-owned file area; large, high-volume, sensitive, or externally authoritative data may remain in the governing external system.
- External systems may remain systems of record for raw/large/sensitive data; preserve canonical references and permitted derived intelligence instead of copying everything into the workspace.
- External capabilities are needs of the requested work, not dependencies of AURA itself. The active model/harness/user chooses actual tools/providers and handles availability, credentials, retries, installation, or another real execution method. AURA does not run capability preflight, resolve providers, maintain bindings, or manufacture a manual-action fallback when the host lacks a tool.
- When a needed host capability is unavailable, use another valid host method when practical, ask the user only when a real choice/input is required, or preserve the limitation honestly. Do not make missing runtime machinery into AURA state unless the underlying limitation is itself durable organizational knowledge worth remembering.
- Git/GitHub/GitLab/Forgejo, Obsidian, hosted control planes, remote storage, schedulers, MCP servers, and custom UIs may improve scale, history, collaboration, retrieval, durability, or human experience, but they remain optional adapters around the same durable workspace semantics.

## Product/workspace separation
The AURA distribution owns `core/`, `systems/`, `scripts/`, schemas, tests, packaged templates, and distribution metadata. Organization/user state owns `instances/`, optional `runtime/` receipts, optional `knowledge/`, optional `attachments/`, and business-scoped extensions. Upgrading product source should not require an organization to fork or relocate its workspace merely to preserve state.

## Design test for future changes
Before adding a mandatory dependency, ask: **Can a recipient still copy/unzip ViralTrac AURA, initialize an organization, ask a capable AI for supported work, retrieve the relevant organizational knowledge, use whatever real host capabilities are available, and preserve useful durable results without installing an AURA-specific runtime?**

If no, the change violates portable-first unless it is explicitly an optional adapter whose absence does not weaken AURA's core memory/knowledge function.
