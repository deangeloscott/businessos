# Object Model

See `core/schemas/` and `core/references/lifecycles.md`. Canonical objects use opaque IDs and references rather than filesystem paths. Status/maturity fields describe semantic state; they are not mandatory execution lifecycles.

## Proof
`ProofRecord` is reusable evidence for a specific claim, result, transformation, demonstration, certification, or customer experience. It is not persuasive copy. It preserves source, supported claim, before/after where directly evidenced, evidence strength, freshness, permission status, usage constraints, and related Assets.

A ProofRecord may be discovered through Customer Intelligence or another operating area and reused wherever that evidence is relevant without duplicating the original evidence.

## PreferenceProfile
`PreferenceProfile` is canonical business-scoped customization, not factual business truth or permission. It may apply at business, team, role, or operator scope. Optional `applies_to` hints may narrow relevance by operating area/system label, Workflow, output type, or channel; those hints help retrieval/application and do not route work or constrain model judgment.

The deterministic resolver combines applicable profiles and preserves leaf-level provenance; equal-precedence conflicting leaves are surfaced instead of silently choosing one. Brand visual identity/voice/mandatory expression rules remain Brand concerns, reusable outward claims and claim constraints remain `BusinessClaim` concerns, while measured evidence about what performs better remains `Learning`.
