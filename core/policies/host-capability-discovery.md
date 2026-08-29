# Host Capability Discovery

A fresh copy of **ViralTrac AURA** should use capabilities the current host already provides before concluding that a required capability is unavailable. Host discovery is part of startup and may also run when the environment changes.

## Startup behavior
1. Inspect the tools/functions/connectors/filesystem/code/browser/MCP or other interfaces exposed by the current AI/agent/harness.
2. Map a host tool to a provider-neutral BusinessOS capability only when the tool clearly satisfies the minimum ability needed by that capability. Capability IDs are interfaces, not a whitelist of allowed tools.
3. Prefer explicit tool descriptors, permissions, schemas, or successful non-mutating checks over guesses from a tool name. Do not test a write capability by causing a real external mutation.
4. Persist discovered non-secret tool metadata in the **active workspace environment overlay** under `.businessos/environments/<environment>/tool-inventory.json` and validated bindings under the sibling `capability-bindings.json` when filesystem writes are available. Shipped `deployment/environments/<environment>/` files are immutable defaults and must not be rewritten during ordinary business operation. Never store credentials or secret material in the workspace.
5. If the host exposes capabilities that cannot be safely mapped automatically, keep them unbound and let the agent/human confirm the mapping when the workflow needs them.
6. After host-tool discovery, refresh machine-readable capability descriptors for already-authorized connected providers when the current job would benefit. Provider connection alone is not proof every provider capability is enabled. For ViralTrac, the host can retrieve a non-secret capability/descriptor response and run `python scripts/sync_viraltrac_capabilities.py <environment> --manifest <file>`; provider snapshots/bindings also persist through the workspace environment overlay.
7. For a still-missing capability, inspect **trusted optional local capability packs** before concluding that a local deterministic path is unavailable. Use `python3 scripts/manage_local_capabilities.py status --pack <id>`; bind a healthy existing tool without reinstalling it. Installing/upgrading/repairing system software requires explicit user authorization and must use the fixed pack recipe, never an arbitrary installer discovered at runtime. See `core/policies/local-capability-packs.md`.
8. If host/provider/local-pack discovery is impossible, continue with declared shipped bindings and the portable `local` fallback.

## Precedence
Capability preflight should treat a valid discovered workspace binding exactly like any other active binding. Effective resolution is: workspace environment overlay first, then shipped environment defaults, then explicit provider preference, then trusted local-pack inspection where applicable, then compatible provider/manual fallback.

## Environment bootstrap
An agent may provide a small host-tool manifest and run `python scripts/bootstrap_environment.py <environment> --manifest <path>`. Workspace-relative state refs such as `runtime/host-tools.json` resolve through the active workspace; `--manifest -` may be used for stdin. The helper validates declared capability IDs and compiles the non-secret inventory/bindings into the workspace environment overlay. Do not create or patch host-discovery files under shipped `deployment/environments/`.

Local capability packs merge into the same overlay through `scripts/manage_local_capabilities.py bind --pack <id>` and must preserve unrelated host/provider bindings.

## Portability rule
Host discovery and local capability packs improve AURA's plug-and-play setup but are not required proprietary services. A basic recipient can still configure bindings manually or operate through fallbacks. Host-specific overlay state is intentionally regenerable rather than part of product source or canonical business truth.
