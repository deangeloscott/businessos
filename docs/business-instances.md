# Business Instances

Each business is isolated under `instances/<business-id>/`. Canonical business context, intelligence, decisions, operations, Assets, measurement, and Learning remain inside that instance. Cross-business references fail by default.

`intelligence/proof/` stores canonical ProofRecords for reusable source-linked evidence such as testimonials, reviews, case results, demonstrations, metrics, and certifications. External systems such as a CRM remain their own systems of record; AURA should retain only the business-owned context, references, bounded evidence, and relationships that future work materially needs.

## Preferences and operator labels

Durable work/expression preferences belong under `instances/<business-id>/context/preferences/` as `PreferenceProfile` objects so they do not leak across businesses accidentally. A profile may target the business, a team, a role, or a stable operator label. Operator labels may be opaque and need not contain personal information.

Runs may record `operator_ref`, `team_ref`, and `role_ref` plus an effective preference snapshot for provenance. Those labels/snapshots do not grant authority.

## Cross-business boundary

Brand/company facts, customer evidence, private operational state, and business-specific preferences do not silently cross `business_id` boundaries. Reuse across businesses requires an explicit object/policy designed for broader eligibility, such as carefully supported system-level Learning or product operational knowledge.

AURA does not maintain a shared personal identity/permission profile that automatically supplies or authorizes external actions across businesses.
