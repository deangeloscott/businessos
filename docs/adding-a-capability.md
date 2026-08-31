# Declaring SOP capability needs

AURA playbooks may describe **provider-neutral capability needs** so a model, harness, or human can understand what kind of work a method expects.

Capability IDs live in `core/capabilities/catalog.json` and are descriptive operational knowledge. They are not permissions, runtime inventory, provider bindings, or execution gates.

Example:

```yaml
capabilities:
  required:
    - research.web.read
    - webpage.fetch
  optional:
    - creative.image.generate
```

This means the SOP expects web research/fetch and may benefit from image generation. It does **not** mean AURA chooses a browser, provider, account, connector, model, or API, and it does not prove the current runtime has those capabilities.

## Host/runtime responsibility

The active model/harness/user decides how to satisfy a capability need using the tools actually available. AURA does not inventory host tools, rank providers, install software, store credentials, bind executable paths, sign up for accounts, or block reasoning because a binding record is missing.

If a required capability cannot be satisfied, adapt the method when that can preserve quality, use another valid method, or surface the real limitation. Never fabricate that a tool/action occurred.

## Adding a capability ID

Add a new semantic ID only when the need is reusable across playbooks and cannot be expressed clearly by an existing ID. Keep names provider-neutral and describe the business/technical ability, not a vendor implementation.

Good: `research.web.read`, `webpage.fetch`, `creative.image.generate`, `document.read`.

Prefer an existing semantic capability over adding a synonym. Do not add aliases merely to mirror a provider, product, or tool's native name.

Avoid: provider-specific route names, credential scopes, executable paths, plan tiers, or temporary host state.

## Deliberate non-goals

The capability catalog is not a provider registry, host inventory, permission system, compatibility matrix, or runtime resolver. AURA describes what a method may need; the active model/harness/user decides how to accomplish it with the capabilities actually available.
