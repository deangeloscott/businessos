# Process Extensions and Local Playbooks

AURA may retain organization-scoped improvements to operating knowledge without mutating the canonical AURA product. A `ProcessExtension` is optional durable knowledge, not a permission system, runtime wrapper, or automatic self-modification mechanism.

## Purpose

Use an extension when reusable organization-authored process knowledge or evidence-supported Learning would materially help future work. Do not create one merely to preserve one-off implementation detail.

Modes:
- `augment_contract` — add organization-scoped applicability, instructions, capability needs, durable input/output metadata, and verification to an installed AURA playbook.
- `local_playbook` — define a reusable organization-scoped playbook when no suitable canonical playbook exists.

## Invariants

1. Extensions are operating knowledge. They do not own reasoning, tool/provider choice, orchestration, permissions, scheduling, concurrency, or runtime execution.
2. The active model/harness/user may use an extension, adapt it, combine it with another method, or choose a better method. Its instructions and verification matter only when that method is actually being used.
3. Capability declarations describe provider-neutral method needs. They are not proof that the current runtime has those capabilities and never bind a provider.
4. `reads` and `writes` describe possible durable organizational inputs/outputs. The base playbook's lists are not a permission boundary, and an extension must not manufacture objects merely because a type is declared.
5. Extensions use valid canonical object/capability vocabulary but may not invent alternative persistence semantics that undermine evidence/provenance, organization isolation, or canonical state integrity.
6. Scope is organization-owned. A private extension never becomes another organization's knowledge automatically. Broader reuse requires an explicit sharing/product-development path with appropriate evidence and privacy handling.
7. Compatibility describes AURA-version applicability only; it must not encode host tools, providers, models, autonomy, risk tiers, or permission state.
8. Deactivating or retiring an extension preserves the historical object while removing it from normal effective-method retrieval.
9. Canonical AURA product changes remain explicit product-development work and must pass repository integrity/quality validation before release.

## Scope and conflicts

`business`, `team`, `role`, and `operator` scope describe **where knowledge is relevant**, not which instruction has deterministic authority. When several active extensions apply, AURA may present them in a stable broad-to-specific order for readability, but the model/user resolves semantic applicability or conflicts from actual organization context. A numeric priority or hidden precedence rule is not needed.

## Effective resolution

`scripts/resolve_effective_contract.py` and business-aware candidate retrieval may surface applicable extensions/local playbooks. Resolution composes operating knowledge only. It does not perform capability preflight, choose the method semantically, or create execution authority.
