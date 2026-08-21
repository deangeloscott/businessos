# Deployment

Contracts request generic capabilities. Environment bindings map them to actual connected tools and accounts. Provider preferences can resolve a missing capability to a compatible or preferred provider without coupling business contracts to vendors. Credentials remain outside the workspace. Manual mode is always a valid fallback.

Business OS is portable-first: deployment configuration enhances a workflow; it is not a prerequisite for opening/understanding the workspace. `deployment/environments/local/` is the built-in no-integration default so a fresh recipient can run deterministic capability preflight immediately.

Key files per environment:
- `tool-inventory.json` — what the harness/environment exposes;
- `capability-bindings.json` — enabled capability → provider action/connection mappings;
- `provider-preferences.json` — environment-level preferred/allowed/blocked providers;
- `scheduler-bindings.json` — optional schedule/runtime mappings.

Use `python scripts/preflight_capabilities.py <business-id> <contract-id>` before an atomic job. It defaults to `local`. Use `python scripts/resolve_capability.py <environment> <capability> --business <business-id>` when inspecting one capability directly.
