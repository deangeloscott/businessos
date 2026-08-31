# Process Extensions and Local Playbooks

AURA may retain business-scoped improvements to its operational knowledge without mutating the canonical AURA product. A `ProcessExtension` is optional durable knowledge, not a permission system or runtime wrapper.

## Purpose

Use an extension when evidence-supported Learning is reusable for a particular organization/team/role/operator and encoding that method would materially help future work. Do not create an extension merely to preserve one-off implementation detail.

Modes:
- `augment_contract` — add organization-scoped applicability, instructions, capability needs, and verification to an installed AURA playbook.
- `local_playbook` — define a reusable organization-scoped playbook when no suitable canonical playbook exists.

## Invariants

1. Extensions are operational knowledge. They do not own reasoning, tool/provider choice, orchestration, permissions, scheduling, concurrency, or runtime execution.
2. The active model/harness/user may use the extension, adapt it, combine it with another method, or choose a better method. If an AURA playbook plus extension is explicitly selected and completion is claimed, its essential quality/evidence requirements should be satisfied.
3. A capability declaration describes what the method may need; it is not proof the current runtime has that capability and never names/binds the provider that must satisfy it.
4. `augment_contract` may not introduce canonical write types the base playbook does not already declare. Use a local playbook or an explicit canonical product revision when a genuinely different durable output model is required.
5. Extensions may use canonical object types but may not invent alternative persistence semantics that undermine evidence/provenance, business isolation, or canonical state integrity.
6. Scope is organization-owned. A private extension never becomes another organization's knowledge automatically. Broader reuse requires appropriate evidence and an explicit product/community path.
7. Compatibility should describe AURA version applicability only; it must not encode host tools, providers, models, autonomy, risk tiers, or permission state.
8. Deactivating/retiring an extension preserves history and restores normal base-playbook resolution.
9. Canonical AURA product changes remain explicit product-development work and must pass the repository's integrity/quality validation before release.

## Scope precedence

When multiple active extensions apply, resolve lower to higher specificity:

`business -> team -> role -> operator`

Within the same scope, lower `priority` applies first. Equal-scope/equal-priority extensions may coexist only when their requirements are compatible; surface ambiguity instead of silently inventing precedence.

## Effective resolution

`scripts/resolve_effective_contract.py` and business-aware routing may surface applicable extensions/local playbooks. Resolution composes operational knowledge only. It does not perform capability preflight or create execution authority.
