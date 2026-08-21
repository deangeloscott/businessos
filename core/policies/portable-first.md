# Portable-First Requirement

ViralTrac's BusinessOS is a portable ICM-style operating workspace. This is a hard architectural invariant.

## Required invariant
A complete or standalone Business OS distribution must remain usable from its files without requiring a proprietary Business OS server, database, hosted control plane, UI, scheduler, vector store, or other optional infrastructure merely to understand and perform supported work.

The default operating model is:

```text
workspace + active business instance + capable AI/agent + workflow-required capabilities
```

- The workspace defines how work should be performed.
- `instances/<business-id>/` is the default portable store for durable business context and canonical Business OS objects.
- `runtime/runs/<business-id>/<run-id>/` is the default portable store for bounded run state and working artifacts.
- External systems may remain systems of record for raw/large/sensitive data; preserve canonical references and permitted derived intelligence instead of copying everything into the workspace.
- External capabilities are workflow dependencies, not dependencies of the Business OS architecture itself. If a requested activity intrinsically needs a capability the current host does not have, use capability preflight and the allowed provider/manual fallback rather than making the workspace unusable.
- Optional infrastructure may improve scale, automation, retrieval, durability, or human experience, but it must be an adapter/enhancement around the same contracts and business-instance semantics, not a prerequisite that changes their meaning.

## Design test for future changes
Before adding a mandatory dependency, ask: **Can a recipient still copy/unzip this workspace, initialize a business, route a supported task, follow the process, persist the work locally, and produce a usable result when the workflow's intrinsic capabilities are available or handled by fallback?**

If no, the change violates portable-first unless it is explicitly an optional adapter.
