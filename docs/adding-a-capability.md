# Declaring SOP capability needs

AURA playbooks may describe **provider-neutral capability needs** so a model, harness, or human can understand what kind of work a method expects.

Capability IDs live in `core/capabilities/catalog.json` and are descriptive operational knowledge. They are not permissions, runtime inventory, provider bindings, or execution gates.

Example:

```yaml
capabilities:
  required:
    - web.search
    - web.fetch
  optional:
    - media.image_generate
```

This means the SOP expects web search/fetch and may benefit from image generation. It does **not** mean AURA chooses a browser, provider, account, connector, model, or API, and it does not prove the current runtime has those capabilities.

## Runtime responsibility

The active model/harness/user decides how to satisfy a capability need using the tools actually available. AURA does not inventory host tools, rank providers, install software, store credentials, bind executable paths, sign up for accounts, or block reasoning because a binding record is missing.

If a required capability cannot be satisfied, adapt the method when that can preserve quality, use another valid method, or surface the real limitation. Never fabricate that a tool/action occurred.

## Adding a capability ID

Add a new semantic ID only when the need is reusable across playbooks and cannot be expressed clearly by an existing ID. Keep names provider-neutral and describe the business/technical ability, not a vendor implementation.

Good: `web.search`, `document.read`, `media.image_generate`.

Avoid: provider-specific route names, credential scopes, executable paths, plan tiers, or temporary host state.
