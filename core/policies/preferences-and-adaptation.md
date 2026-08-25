# Preferences and Method Adaptation

BusinessOS standardizes durable business invariants and quality/authorization boundaries without freezing every implementation choice. Preferences customize valid choices; they are not business truth, permissions, promises, or measurements.

## Precedence

Apply constraints before preferences:

1. BusinessOS safety, truth, provenance, ownership, lifecycle, and validation invariants.
2. Explicit business/compliance/approval requirements and mandatory Brand rules.
3. Contract requirements and task-specific mandatory requirements.
4. Resolved durable preferences, from lower to higher precedence: business → team → role → operator.
5. Task-specific optional preferences.
6. BusinessOS defaults.
7. Model/harness creative or implementation discretion.

A lower layer never overrides a higher-layer requirement. A preference conflict at the same effective precedence must be surfaced rather than resolved arbitrarily.

## PreferenceProfile

- Store durable business-scoped customization as canonical `PreferenceProfile` objects under `instances/<business-id>/context/preferences/`.
- Use `business`, `team`, `role`, or `operator` scope. Operator identifiers may be opaque workspace-local labels; do not require personal information merely to personalize work.
- `applies_to` can narrow a profile by system, contract, output type, or channel. Missing/empty applicability means the profile is broadly applicable within its scope.
- Do not silently infer a durable PreferenceProfile from one prior output or behavior. Measured evidence about what works belongs in `Learning`; it may motivate an explicit preference/configuration change but is not automatically converted into preference truth.
- Brand/company truth remains in canonical Business Context. Visual identity, outward voice, approved reference Assets, prohibited styles, and mandatory brand rules remain Brand concerns; PreferenceProfile expresses allowed working/expression choices within those boundaries.
- **Do not store authorization, approval, permission, or action-boundary state in `PreferenceProfile`.** “I prefer concise responses” is a preference; “do not publish without asking,” “may spend up to X,” “contact customers only with approval,” and similar statements are action/authorization requirements. Keep current-task boundaries in the user request and bounded Run context. When a formal approval must persist, use the governed `Approval` lifecycle under `operations/approvals/` according to `core/policies/approval.md`. A PreferenceProfile can neither grant nor revoke action authority.
- An old task restriction does not become an eternal operator preference merely because it was conservative. A later session must resolve current authorization from the current request, BusinessOS policies, applicable Approval records, and action state—not from style/work-method preferences.
- **Legacy upgrade rule:** if an older BusinessOS workspace already contains authorization/approval semantics inside `PreferenceProfile`, do not manually reinterpret them as standing authority. Run `scripts/migrate_preference_profiles.py <business-id>` to inspect the proposed cleanup, then `--apply` to remove only values the current PreferenceProfile semantic guard rejects. The migration preserves legitimate preferences, records removal paths/fingerprints for auditability, creates no Approval, and is idempotent.
- Historical Run-local preference snapshots are immutable execution provenance. A legacy snapshot may therefore still show the effective preferences that existed when that old Run executed; do not rewrite it during migration and do not use it as current authorization. New resolution must use the migrated active PreferenceProfile plus current task/policy/Approval state.

## Effective resolution

Use `scripts/resolve_preferences.py` (or the equivalent context-plan/run integration) instead of asking the model to improvise precedence. The deterministic resolver deep-merges applicable profiles and records leaf-level provenance. Higher-priority profiles inside the same scope override lower-priority profiles. Equal-scope/equal-priority conflicting leaves fail resolution until clarified.

A bounded Run may record `operator_ref`, `team_ref`, and `role_ref` plus a run-local effective-preference snapshot. The snapshot is execution context/provenance, not canonical business truth.

During fresh-business onboarding, when the user explicitly asks BusinessOS to remember reusable preferences, persist the applicable `PreferenceProfile` **before creating the first downstream Run**. `bootstrap_explicit_context.py --preference-profile-file ...` exists for this handoff. Otherwise the current chat may appear personalized while the Run snapshot remains empty and the preference will not be reproducibly portable to a later session/harness.

## Method adaptability

Contracts should govern required outcomes, evidence, constraints, capabilities, risk, authorization, and validation—not unnecessarily freeze implementation technique. A model/harness may choose a better/faster/easier method, provider, renderer, structure, or tool when all of the following remain true:

- the selected method satisfies the contract's required business outcome and outputs;
- evidence, claim, ownership, privacy, approval, and verification rules remain satisfied;
- the capability is actually available/authorized or a valid fallback is used;
- business/Brand/task requirements and resolved preferences remain satisfied;
- no unsupported business fact, promise, outcome, or permission is introduced.

Changing a business's style, template, preference, or capability binding normally changes business/deployment state, not BusinessOS product code. Change BusinessOS itself only when the reusable operating invariant, schema, lifecycle, validation, or shared mechanism is wrong or missing.
