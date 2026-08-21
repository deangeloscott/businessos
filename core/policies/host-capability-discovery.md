# Host Capability Discovery

A fresh copy of ViralTrac's BusinessOS should use capabilities the current host already provides before concluding that a required capability is unavailable. Host discovery is part of startup and may also run when the environment changes.

## Startup behavior
1. Inspect the tools/functions/connectors/filesystem/code/browser/MCP or other interfaces exposed by the current AI/agent/harness.
2. Map a host tool to a provider-neutral BusinessOS capability only when the tool clearly satisfies the minimum ability needed by that capability. Capability IDs are interfaces, not a whitelist of allowed tools.
3. Prefer explicit tool descriptors, permissions, schemas, or successful non-mutating checks over guesses from a tool name. Do not test a write capability by causing a real external mutation.
4. Persist discovered non-secret tool metadata under `deployment/environments/<environment>/tool-inventory.json` and validated bindings under `capability-bindings.json` when filesystem writes are available. Never store credentials or secret material in the workspace.
5. If the host exposes capabilities that cannot be safely mapped automatically, keep them unbound and let the agent/human confirm the mapping when the workflow needs them.
6. After host-tool discovery, refresh machine-readable capability descriptors for already-authorized connected providers when the current job would benefit. Provider connection alone is not proof every provider capability is enabled. For ViralTrac, the host can retrieve a non-secret capability/descriptor response and run `python scripts/sync_viraltrac_capabilities.py <environment> --manifest <file>`.
7. If host/provider discovery is impossible, continue with declared bindings and the portable `local` fallback.

## Precedence
Capability preflight should treat a valid discovered host binding exactly like any other active binding. Only after host/existing capabilities are considered should a missing capability move to provider resolution or manual/assisted fallback.

## Environment bootstrap
An agent may write a small host-tool manifest and run `python scripts/bootstrap_environment.py <environment> --manifest <path>`. The helper validates declared capability IDs and compiles the non-secret inventory/bindings. The agent remains responsible for conservatively deciding which visible host tools genuinely satisfy which capabilities.

## Portability rule
Host discovery improves plug-and-play setup but is not a required proprietary service. A basic recipient can still configure bindings manually or operate through fallbacks.
