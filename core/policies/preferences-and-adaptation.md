# Preferences and Method Adaptation

AURA preserves durable organizational preferences without confusing them with business truth, decisions, current-task instructions, permissions, or measurements.

## Precedence

Apply established organizational truth and real task constraints before optional preferences:

1. Current supported business truth, provenance/reference integrity, organization isolation, and other AURA-owned state invariants.
2. Explicit business, legal/compliance, platform/account, task, and mandatory Brand requirements that actually apply.
3. Essential outcome/evidence/quality requirements from operating knowledge the model/user chooses to use.
4. Resolved durable preferences, from lower to higher precedence: business → team → role → operator.
5. Task-specific optional preferences.
6. AURA defaults where relevant.
7. Model/harness creative or implementation discretion.

A lower layer never overrides a higher-layer requirement. A preference conflict at the same effective precedence must be surfaced rather than resolved arbitrarily.

## PreferenceProfile

- Store durable business-scoped customization as canonical `PreferenceProfile` objects under `instances/<business-id>/context/preferences/`.
- Use `business`, `team`, `role`, or `operator` scope. Operator identifiers may be opaque workspace-local labels; do not require personal information merely to personalize work.
- `applies_to` can narrow relevance by operating-area/system label, Workflow, output type, or channel. These are applicability hints, not routing or execution authority. Missing/empty applicability means the profile is broadly applicable within its scope.
- Do not silently infer a durable PreferenceProfile from one prior output or behavior. Measured evidence about what works belongs in `Learning`; it may motivate an explicit preference change but is not automatically converted into preference truth.
- Brand/company truth remains in canonical Business Context. Visual identity, outward voice, established reference Assets, prohibited styles, and mandatory brand rules remain Brand concerns; PreferenceProfile expresses allowed working/expression choices within those boundaries.
- **Do not store authorization, approval, or permission state in `PreferenceProfile`.** “I prefer concise responses” is a preference. A current instruction such as “do not publish this” remains part of the current request/work context unless the organization explicitly chooses to preserve an appropriate durable instruction elsewhere.
- Durable organizational choices belong in `DecisionRecord` when future work benefits from knowing what was decided, by whom/what, when, and on what basis. A DecisionRecord is organizational memory, not a permission token.
- Historical Run-local preference snapshots are immutable provenance. They may show the preferences that existed when old work ran; do not treat that snapshot as current organizational truth.

## Effective resolution

Use `scripts/resolve_preferences.py` (or equivalent context retrieval) instead of asking the model to improvise preference precedence mechanically. The deterministic resolver deep-merges applicable profiles and records leaf-level provenance. Higher-priority profiles inside the same scope override lower-priority profiles. Equal-scope/equal-priority conflicting leaves fail resolution until clarified.

A bounded work receipt may record `operator_ref`, `team_ref`, and `role_ref` plus a work-local effective-preference snapshot. The snapshot is provenance, not canonical business truth.

During fresh-business onboarding, when the user explicitly asks AURA to remember reusable preferences, persist the applicable `PreferenceProfile` before later work that should rely on it. Otherwise the current session may appear personalized while future sessions/harnesses cannot reproduce the preference.

## Method adaptability

AURA operating knowledge should preserve the outcome, evidence, non-obvious expertise, and quality/constraint requirements that materially improve the work without freezing implementation technique.

A model/harness may choose a better, faster, easier method, provider, renderer, structure, tool, or external Skill when all of the following remain true:

- the chosen method still serves the requested business outcome;
- any genuinely essential truth/evidence/quality requirements for the job remain satisfied;
- real business, Brand, legal/compliance, platform/account, and task constraints remain satisfied;
- resolved preferences remain satisfied where they apply;
- no unsupported business fact, promise, outcome, or tool action is introduced.

Whether a host has the needed tools/resources is runtime reality for the active model/harness to handle. AURA does not require a provider/capability registry, preflight ceremony, or manufactured fallback state.

Changing a business's style, template, preference, or available runtime capability normally changes organizational or execution context, not AURA product code. Change AURA itself only when reusable operating knowledge, durable memory semantics, integrity, schemas, retrieval, measurement, or another genuinely AURA-owned responsibility is wrong or missing.
