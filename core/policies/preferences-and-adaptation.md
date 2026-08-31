# Preferences and Method Adaptation

AURA preserves durable organizational preferences without confusing them with business truth, decisions, current-task instructions, permissions, or measurements.

## Precedence

Apply organizational truth and explicit task constraints before preferences:

1. AURA truth, provenance, ownership, lifecycle, and validation invariants.
2. Explicit business/compliance requirements and mandatory Brand rules that are actually applicable.
3. Selected SOP requirements and task-specific mandatory requirements.
4. Resolved durable preferences, from lower to higher precedence: business → team → role → operator.
5. Task-specific optional preferences.
6. AURA defaults.
7. Model/harness creative or implementation discretion.

A lower layer never overrides a higher-layer requirement. A preference conflict at the same effective precedence must be surfaced rather than resolved arbitrarily.

## PreferenceProfile

- Store durable business-scoped customization as canonical `PreferenceProfile` objects under `instances/<business-id>/context/preferences/`.
- Use `business`, `team`, `role`, or `operator` scope. Operator identifiers may be opaque workspace-local labels; do not require personal information merely to personalize work.
- `applies_to` can narrow a profile by system, contract/SOP, output type, or channel. Missing/empty applicability means the profile is broadly applicable within its scope.
- Do not silently infer a durable PreferenceProfile from one prior output or behavior. Measured evidence about what works belongs in `Learning`; it may motivate an explicit preference change but is not automatically converted into preference truth.
- Brand/company truth remains in canonical Business Context. Visual identity, outward voice, established reference Assets, prohibited styles, and mandatory brand rules remain Brand concerns; PreferenceProfile expresses allowed working/expression choices within those boundaries.
- **Do not store authorization, approval, or permission state in `PreferenceProfile`.** “I prefer concise responses” is a preference. A current instruction such as “do not publish this” remains part of the current request/work context unless the organization explicitly chooses to preserve it as a durable instruction elsewhere.
- Durable organizational choices belong in `DecisionRecord` when future work benefits from knowing what was decided, by whom, when, and on what basis. A DecisionRecord is organizational memory, not a permission token.
- Historical Run-local preference snapshots are immutable provenance. They may show the preferences that existed when old work ran; do not treat that snapshot as current organizational truth.

## Effective resolution

Use `scripts/resolve_preferences.py` (or the equivalent context retrieval integration) instead of asking the model to improvise precedence. The deterministic resolver deep-merges applicable profiles and records leaf-level provenance. Higher-priority profiles inside the same scope override lower-priority profiles. Equal-scope/equal-priority conflicting leaves fail resolution until clarified.

A bounded work receipt may record `operator_ref`, `team_ref`, and `role_ref` plus a work-local effective-preference snapshot. The snapshot is provenance, not canonical business truth.

During fresh-business onboarding, when the user explicitly asks AURA to remember reusable preferences, persist the applicable `PreferenceProfile` before downstream work that should rely on it. Otherwise the current session may appear personalized while later sessions/harnesses cannot reproduce the preference.

## Method adaptability

SOPs should govern required outcomes, evidence, essential process/quality invariants, and relevant constraints without freezing implementation technique. A model/harness may choose a better, faster, easier method, provider, renderer, structure, or tool when all of the following remain true:

- the chosen method satisfies the required business outcome and any selected SOP's essential requirements;
- evidence, claim, ownership, privacy, and task-specific requirements remain satisfied;
- the needed execution capability is actually available in the current harness or a valid fallback is used;
- business/Brand/task requirements and resolved preferences remain satisfied;
- no unsupported business fact, promise, outcome, or tool action is introduced.

Changing a business's style, template, preference, or runtime capability normally changes organizational or execution state, not AURA product code. Change AURA itself only when reusable operational knowledge, durable memory semantics, integrity, schemas, lifecycle, retrieval, measurement, or shared organization-owned mechanisms are wrong or missing.
