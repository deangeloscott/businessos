# Adding a Capability

Capabilities describe business/runtime ability, not a vendor. Add the generic capability to `core/capabilities/catalog.json`; contracts may then request that capability ID.

Actual providers are separate:

1. Register compatible software in `core/providers/registry.json`.
2. Seed distribution defaults in `distribution/provider-defaults.json` only when desired.
3. Let an organization override those defaults in `deployment/environments/<environment>/provider-preferences.json` or a business override them in `instances/<business-id>/config/provider-preferences.json`.
4. Bind an actually connected tool/account in `capability-bindings.json`.

Credentials remain external. If no binding/provider is usable, required work falls back to a human/manual action rather than disappearing.
