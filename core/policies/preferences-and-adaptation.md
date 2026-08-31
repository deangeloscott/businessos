# Preferences and Method Adaptation

AURA standardizes durable business truth, provenance, process-quality invariants, and organizational continuity without freezing every implementation choice. Preferences customize valid choices; they are not business truth, permissions, promises, measurements, or decisions.

## Precedence

Apply actual requirements before preferences:

1. AURA truth, provenance, ownership, lifecycle, and integrity invariants.
2. Explicit organization, legal, compliance, Brand, and current-task requirements.
3. Essential requirements of the selected AURA SOP, when an AURA SOP is actually being used or claimed.
4. Resolved durable preferences, from lower to higher precedence: business → team → role → operator.
5. Task-specific optional preferences.
6. AURA defaults.
7. Model/harness creative or implementation discretion.

A lower layer never overrides a higher-layer requirement. A preference conflict at the same effective precedence must be surfaced rather than resolved arbitrarily.

## PreferenceProfile

- Store durable business-scoped customization as canonical `PreferenceProfile` objects under `instances/<business-id>/context/preferences/`.
- Use `business`, `team`, `role`, or `operator` scope. Operator identifiers may be opaque workspace-local labels; do not require personal information merely to personalize work.
- `applies_to` can narrow a profile by system, contract, output type, or channel. Missing/empty applicability means the profile is broadly applicable within its scope.
- Do not silently infer a durable PreferenceProfile from one prior output or behavior. Measured evidence about what works belongs in `Learning`; it may motivate an explicit preference/configuration change but is not automatically converted into preference truth.
- Brand/company truth remains in canonical Business Context. Visual identity, outward voice, established reference Assets, prohibited styles, and mandatory brand rules remain Brand concerns; PreferenceProfile expresses allowed working/expression choices within those boundaries.
- **Do not store authorization, permission, approval state, or one-time task boundaries in `PreferenceProfile`.** “I prefer concise responses” is a preference. “Do not publish this,” “do not spend money on this task,” or “contact these customers only after I review the draft” is a current instruction or task constraint and stays with the relevant request/work context unless the organization explicitly establishes it as a durable operating instruction.
- A material organizational choice that should be remembered is a `DecisionRecord`, not a PreferenceProfile. `DecisionRecord` records that a decision was made; it is not a standing permission token and does not make future action automatically allowed or forbidden.
- An old task restriction does not become an eternal operator preference merely because it was conservative. A later model/harness resolves the current action boundary from the current request, current organization instructions/context, current external permissions, and any actually applicable law/platform constraints.
- **Legacy upgrade rule:** if an older workspace already contains authorization/approval semantics inside `PreferenceProfile`, do not reinterpret those fields as standing authority. `scripts/migrate_preference_profiles.py <business-id>` may be used to remove values the current PreferenceProfile semantic guard rejects while preserving legitimate preferences and audit fingerprints. Historical Run-local snapshots remain immutable provenance and do not govern current work.

## Effective resolution

Use `scripts/resolve_preferences.py` (or the equivalent context-plan/run integration) instead of asking the model to improvise preference precedence. The deterministic resolver deep-merges applicable profiles and records leaf-level provenance. Higher-priority profiles inside the same scope override lower-priority profiles. Equal-scope/equal-priority conflicting leaves fail resolution until clarified.

A bounded Run may record `operator_ref`, `team_ref`, and `role_ref` plus a run-local effective-preference snapshot. The snapshot is execution context/provenance, not canonical business truth or authority.

During fresh-business onboarding, when the user explicitly asks AURA to remember reusable preferences, persist the applicable `PreferenceProfile` before the first downstream work that should use it. Otherwise the current session may appear personalized while later sessions/harnesses cannot reproduce the preference.

## Method adaptability

AURA SOPs should govern the essential outcome, evidence, process, and quality invariants that make the SOP valuable—not unnecessarily freeze implementation technique or current execution mechanics. A model/harness may choose a better/faster/easier method, provider, renderer, structure, or tool when all of the following remain true:

- if an AURA SOP was selected, the method still satisfies its essential business outcome and required process/quality invariants;
- truth, evidence, provenance, ownership, and applicable customer-facing claim rules remain satisfied;
- the actual current environment can perform the chosen method, or the model/harness selects a truthful fallback;
- business/Brand/task requirements and resolved preferences remain satisfied;
- no unsupported business fact, promise, outcome, or execution claim is introduced.

Changing a business's style, template, preference, or current tool normally changes organization/runtime state, not AURA product code. Change AURA itself only when the reusable organizational-memory, operating-knowledge, continuity, truth, measurement/Learning, or product-integrity mechanism is wrong or missing.
