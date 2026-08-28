# Deployment

Contracts request generic capabilities. Environment bindings map them to actual connected tools and accounts. Provider preferences can resolve a missing capability to a compatible or preferred provider without coupling business contracts to vendors. Credentials remain outside the workspace. Manual mode is always a valid fallback.

Business OS is portable-first: deployment configuration enhances a workflow; it is not a prerequisite for opening/understanding the workspace. `deployment/environments/local/` is the shipped no-integration **default** so a fresh recipient can run deterministic capability preflight immediately. Ordinary host discovery/configuration does not rewrite those product files; live host-specific environment state is stored under the active workspace at `.businessos/environments/<environment>/` and takes precedence per file.

Key effective files per environment:
- `tool-inventory.json` — what the current harness/environment exposes;
- `capability-bindings.json` — enabled capability → provider action/connection mappings;
- `provider-preferences.json` — environment-level preferred/allowed/blocked providers;
- `scheduler-bindings.json` — optional schedule/runtime mappings.

Resolution order is workspace environment overlay → shipped product environment default. Host-specific overlay state is regenerable and is ignored by the default workspace Git configuration; canonical business truth remains under `instances/`.

Use `python scripts/preflight_capabilities.py <business-id> <contract-id>` before an atomic job. It defaults to `local`. Use `python scripts/resolve_capability.py <environment> <capability> --business <business-id>` when inspecting one capability directly.
