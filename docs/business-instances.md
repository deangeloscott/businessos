# Business Instances

Each business is isolated under `instances/<business-id>/`. Canonical business context, intelligence, decisions, operations, Assets, measurement, and Learning remain inside that instance. Cross-business references fail by default.

`intelligence/proof/` stores canonical ProofRecords for reusable source-linked evidence such as testimonials, reviews, case results, demonstrations, metrics, and certifications. External systems such as a CRM remain their own systems of record; AURA should retain only the business-owned context, references, bounded evidence, and relationships that future work materially needs.

## Preferences and operator labels

Durable work/expression preferences belong under `instances/<business-id>/context/preferences/` as `PreferenceProfile` objects so they do not leak across businesses accidentally. A profile may target the business, a team, a role, or a stable operator label. Operator labels may be opaque and need not contain personal information.

Runs may record `operator_ref`, `team_ref`, and `role_ref` plus an effective preference snapshot for provenance. Those labels/snapshots do not grant authority.

## Cross-business boundary

Brand/company facts, customer evidence, private operational state, business-specific preferences, and `Learning` do not silently cross `business_id` boundaries. A Learning may be domain-scoped or business-scoped **inside its own organization**; neither scope makes it shared organizational memory for other businesses.

If reusable procedural knowledge should cross organization boundaries, share it deliberately through an InnovationPackage or make it deliberate canonical AURA product-development work. The receiving organization must evaluate imported knowledge against its own evidence and context rather than treating another organization's Learning as local truth.

AURA does not maintain a shared personal identity/permission profile that automatically supplies or authorizes external actions across businesses.
