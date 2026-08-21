# Publisher Provenance and Updates

`PUBLISHER.json` gives every distribution a machine-readable origin and optional canonical update location.

It can record:

- publisher ID/name;
- canonical project URL;
- documentation/support URLs;
- an update-manifest URL;
- provenance rules for derivative distributions.

Generated `SYSTEM-MANIFEST.json` includes configured publisher identity and points back to `PUBLISHER.json`. Edition packaging preserves this metadata by default.

This provides durable attribution in ordinary redistribution and gives an agent a canonical place to look for documentation or updates. It is not DRM: a deliberate redistributor can remove or alter provenance metadata. Existing workspace/release SHA-256 checksums help detect changes to a particular packaged release but do not prevent copying.

An update URL is informational. The Business OS does not automatically download or install remote code. A host may check the configured update manifest under its own security/update policy.

## Publisher configured for this release

- Creator: DeAngelo Scott
- Publisher: Umegro, LLC
- First-party product: ViralTrac
- Creator website: https://deangeloscott.com
- Product/publisher website: https://viraltrac.com
- Canonical Business OS project/update manifest: not configured yet

Until a canonical project/update endpoint exists, agents should preserve this provenance metadata but must not invent an update location.
