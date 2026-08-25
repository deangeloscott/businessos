# ViralTrac's BusinessOS v1.8.4

**A portable, AI-native business operating system that gives AI agents structured processes to research, operate, optimize, and grow a business.**

Installed domain modules: **Competitor Intelligence, Content Synthesis, Customer Intelligence, Customer Optimization, Industry Intelligence, Marketing Synthesis, SEO/AEO**. Core is always included.

This distribution is **source-available, not open source**. Internal/commercial business use, customization, and agency/consulting use for clients are permitted under `LICENSE.md`; white-label resale or repackaging it as someone else's standalone BusinessOS product is not.

Business logic remains model/provider/vendor agnostic. Each customer can keep a separate copy and separate business instance; business-specific context, intelligence, assets, preferences, and Learning stay inside that copy unless deliberately integrated elsewhere. The edition is portable-first: no proprietary BusinessOS server/database/UI, ViralTrac account, or cloud runtime is required for local operation.

## Start

**AI/agent:** read root `CONTEXT.md` and `core/policies/agent-execution.md` before the first business write. Contract IDs are not executable paths; durable Business Context must use validated canonical objects.
- Automatic first-run message: `WELCOME.md`
- Human: `START-HERE.md`
- Browse what BusinessOS can do: `PLAYBOOKS.md`
- AI/agent: `CONTEXT.md`
- License: `LICENSE.md`
- Public distribution/security boundary: `PUBLIC-DISTRIBUTION.md`, `SECURITY.md`
- Installed modules/dependencies: `INSTALLATION.json` and `distribution/ACTIVE-DEPENDENCIES.json`
- Tasks: `TASK-NAVIGATOR.md`
- Publisher/origin: `PUBLISHER.json`
- Provider defaults: `distribution/provider-defaults.json`

Optional modules are enrichments, not hidden hard dependencies. When one is absent, use `core/policies/module-independence.md`.

## ViralTrac native companion
When ViralTrac is connected, BusinessOS can dynamically discover its current machine-facing capabilities and use its governed semantic data, measurement, tracking, supported action/receipt surfaces, and event/reactive plane without making ViralTrac a required runtime. The public BusinessOS package contains only integration-facing metadata needed by authorized clients; it does not include ViralTrac's proprietary hosted-application source code or private infrastructure. See `core/policies/viraltrac-native-companion.md`.

## Customization and multi-operator use
BusinessOS separates reusable operating invariants from business/Brand configuration, team/operator preferences, and implementation technique. Durable preferences live as business-scoped `PreferenceProfile` objects and resolve deterministically as business → team → role → operator → one-task preference, always below mandatory BusinessOS/business/Brand/contract/approval requirements. Runs may carry opaque `operator_ref`/`team_ref`/`role_ref` labels and snapshot the effective preferences for reproducibility. See `core/policies/preferences-and-adaptation.md`.

Different models/harnesses may sequentially resume the same durable workspace; WorkRequests can be executed in the same session or by harness-managed workers. BusinessOS does not itself spawn agents or guarantee arbitrary simultaneous writes to the same canonical object are conflict-safe. See `core/policies/shared-workspace-coordination.md`.


## Fresh-business onboarding
For a new business, `scripts/bootstrap_explicit_context.py` can ground setup facts across multiple original user-supplied files with repeated `--source-file` arguments; it preserves each source member reference/hash instead of requiring a manually merged source file. Explicit organization Brand instructions should be persisted as first-class Brand state during the same handoff, preferably with `--brand-profile-file runtime/<brand>.json` (the grounded facts `brand` field remains supported); reusable business/team/role/operator preferences can be persisted before residual work with `--preference-profile-file`. This keeps the first downstream Run portable and preference-aware rather than depending on the transient chat context.

For outward Content/Marketing work, intended audience and publication state are separate. A local unpublished homepage, landing page, email, ad, proposal, webinar, or similar draft remains customer-facing and must use the appropriate customer-facing production root, claim governance, required subcontract evidence, and Run provenance. Work created during the current execution is never `imported`/`preexisting` merely because it has not been published.

## Updates
Update checks use official GitHub Releases, are disabled by default, metadata-only, and never auto-install. For a one-time check: `python scripts/check_for_updates.py --force`.
## Attention and changing platforms
BusinessOS keeps portable semantic state for material unresolved attention and versioned external platform changes; it does not require a proprietary notification/scheduler service. Compatible harnesses can query current attention with `python scripts/list_attention.py <business-id> --json` and current platform state with `python scripts/list_platform_state.py <business-id> --json`, then use whatever delivery/scheduling capabilities they provide. Repeated unchanged checks update existing state instead of creating duplicate files.



### Authorization is not a preference

Reusable style/work-method choices belong in `PreferenceProfile`. Current-task permissions and restrictions (for example, do not publish, do not spend, ask before contacting customers, or approval required before deployment) do **not** belong in PreferenceProfile and must not be carried into later sessions as personal preferences. Keep them in the current request/Run/action context; persist formal approvals through the governed `Approval` lifecycle when applicable.

If upgrading a workspace created before this separation was enforced, inspect legacy profiles with `python3 scripts/migrate_preference_profiles.py <business-id>`. After reviewing the dry-run output, apply with `--apply`, then run `python3 scripts/validate_business.py <business-id> --require-context`. The migration removes invalid preference-held authority only; it does not create or infer an Approval.
