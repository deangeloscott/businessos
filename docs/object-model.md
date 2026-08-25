# Object Model

See `core/schemas/` and `core/references/lifecycles.md`. Canonical objects use opaque IDs and references rather than filesystem paths.

## Proof
`ProofRecord` is reusable evidence for a specific claim, result, transformation, demonstration, certification, or customer experience. It is not persuasive copy. It preserves source, supported claim, before/after where directly evidenced, confidence, freshness, permission status, usage constraints, and related Assets.

A ProofRecord may be discovered by Customer Intelligence or another system and reused by Content, Marketing, SEO/AEO, Customer Optimization, and future systems without duplicating the original evidence.

## PreferenceProfile
`PreferenceProfile` is canonical business-scoped customization, not factual business truth or permission. It may apply at business, team, role, or operator scope and may be narrowed by system/contract/output/channel. The deterministic resolver combines applicable profiles and preserves leaf-level provenance; equal-precedence conflicts are surfaced instead of silently choosing one. Brand visual identity/voice/mandatory rules remain Brand concerns, while measured evidence about what performs better remains `Learning`.
