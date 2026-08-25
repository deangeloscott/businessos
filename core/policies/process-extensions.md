# Process Extensions and Local Playbooks

BusinessOS may adapt a business's operating process without mutating the canonical BusinessOS product. The preferred mechanism is a business-scoped `ProcessExtension`.

## Why overlays come first

Canonical contracts remain the portable upgrade base. A `ProcessExtension` can augment an installed contract or define a local business playbook while preserving the original contract, its provenance, and its upgrade path. Successful local practice does not become a universal BusinessOS rule merely because it worked once.

## Modes

- `augment_contract`: adds business-scoped applicability, method instructions, provider-neutral capability requirements, and verification to an installed canonical contract.
- `local_playbook`: defines a new business-scoped playbook with its own local contract ID, purpose, route terms, declared reads/writes, capabilities, instructions, and verification.

## Invariants

1. Higher-level BusinessOS safety, truth, approval, evidence, lifecycle, privacy, and validation policies always win.
2. An extension may not lower a canonical contract's risk, autonomy ceiling, approval, evidence, claim, or verification requirements.
3. Augmenting a contract never deletes the canonical instructions. Effective resolution is base contract plus applicable active extensions.
4. An `augment_contract` extension may not introduce canonical write types the base contract does not already declare; use a new local playbook or explicit canonical revision when a genuinely new lifecycle/output is needed.
5. Local playbooks may use canonical object types and provider-neutral capabilities, but they may not invent replacement persistence rules or bypass deterministic helpers.
6. Capability requirements describe what the job needs, not which vendor/model must provide it. Provider preferences and bindings remain separate.
7. Business-scoped extensions never become another business's private state. Cross-business/system reuse requires explicit eligible evidence and normal Core learning governance.
8. BusinessOS version compatibility must be checked before applying an extension. Incompatible extensions remain inspectable but inactive.
9. Retiring/deactivating an extension must leave the canonical contract intact and restore normal base behavior.
10. Canonical BusinessOS product changes remain explicit BusinessOS development work and require the normal repository regression/release path.

## Scope precedence

When several active extensions apply to the same contract, resolve lower to higher precedence:

`business -> team -> role -> operator`

Within the same scope, lower `priority` applies first and higher `priority` later. Equal-scope/equal-priority extensions may coexist only when they do not declare contradictory requirements; ambiguous conflicts must be surfaced.

## Effective resolution

Use `scripts/resolve_effective_contract.py` or `scripts/resolve_contract.py --business-id ...` when an active business may have extensions. `scripts/route_and_resolve.py --business-id ...` also considers active local playbooks before falling back to canonical routing.

## Capability preflight

`preflight_capabilities.py` includes the required/optional provider-neutral capabilities declared by applicable extensions. A missing provider changes execution/fallback; it does not silently remove the extension's required business step.
