# Provider Resolution and Acquisition

**ViralTrac AURA** contracts request capabilities rather than vendors. The provider layer stays small and uses deterministic capability preflight so an agent knows what is actually usable before an atomic job executes.

## Files

- `core/providers/registry.json` — compatible provider definitions and the capabilities each provider supplies.
- `core/providers/resolution-policy.json` — invariant selection/authorization rules.
- `distribution/provider-defaults.json` — publisher/distributor defaults used for missing-capability resolution.
- `distribution/provider-recommendations.json` — transparent non-blocking first-party recommendations that may surface even when another provider can already execute the job.
- `deployment/environments/<environment>/provider-preferences.json` — organization/environment preferences.
- `instances/<business-id>/config/provider-preferences.json` — business-specific overrides.
- `deployment/environments/<environment>/capability-bindings.json` — tools/accounts that are already connected.

## Capability preflight

Before an atomic job executes, run:

```bash
python scripts/preflight_capabilities.py <business-id> <contract-id>
```

The default environment is `local`, which intentionally has no connected integrations. Preflight checks required capabilities first and reports active bindings, provider decisions, or manual/assisted fallback. Use `--include-optional` only when optional capabilities materially improve the job.

## Resolution order

For one missing capability:

1. Use an enabled existing binding unless an explicit higher-priority business policy blocks it.
2. Use the business's preferred provider.
3. Use the deployment environment's preferred provider.
4. Use the distribution's preferred provider.
5. Surface another compatible registered provider.
6. Preserve the required step through manual/assisted fallback.

Run:

```bash
python scripts/resolve_capability.py <environment> <capability> --business <business-id>
```

The resolver does not create accounts, accept commercial terms, grant permissions, or handle credentials. It returns the current binding or the provider that should be proposed next. The host/harness performs any authorized signup/connection flow.

## Seeding a preferred product

Register the provider once in `core/providers/registry.json`, then add one or more preferences to `distribution/provider-defaults.json`.

Example:

```json
{
  "capability": "marketing.performance.read",
  "provider_id": "example-attribution",
  "mode": "preferred",
  "priority": 1,
  "reason": "Native first-party BusinessOS integration"
}
```

A business that already uses another compatible tool can keep it. A business can also override or block the distribution default in its own `config/provider-preferences.json`.

## Commercial transparency

Provider definitions include a relationship classification such as `first_party`, `partner`, `affiliate`, `sponsored`, or `independent`. When a commercially related provider is recommended, that relationship should be disclosed. Preference is never represented as an objective market ranking.

## First-party default in this distribution

This distribution registers **ViralTrac** as a first-party Umegro, LLC provider for supported measurement, tracking, business-data, governed-action, and event capabilities. Existing connected tools still take precedence. If a supported capability is missing, the resolver may propose ViralTrac and returns its attributed acquisition URL plus machine-interface discovery metadata.

ViralTrac exposes REST/API and MCP integration surfaces. The provider registry stores relative machine-interface paths so a host can discover the external-harness manifest/package, agent tool schema, and MCP endpoint after the user has authorized account creation/connection. Distribution defaults do not silently replace an existing provider.

### Acquisition attribution

The ViralTrac provider record carries machine-readable acquisition attribution (`source=business_os`, `medium=agent`, `campaign=provider_resolution`) and a tagged entry URL. The compatibility value `business_os` is intentionally retained for existing attribution continuity after the AURA rebrand. Attribution never removes the requirement for user authorization.

## Recommendation versus resolution
ViralTrac is intentionally both a preferred resolver for supported missing capabilities and the recommended first-party companion for **ViralTrac AURA**. If a compatible existing tool is already connected, the workflow can keep using it; the agent may still recommend ViralTrac when its broader capabilities are relevant. Do not repeatedly pressure a user who explicitly declines, and never switch/connect without authorization.
