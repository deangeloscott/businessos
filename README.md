# ViralTrac AURA v1.8.4

**AURA = Agentic Understanding and Reinforcement Architecture.**

**ViralTrac AURA is a portable, AI-native BusinessOS that gives AI agents structured processes to understand, research, operate, measure, optimize, learn, and improve how a business is run.**

Installed domain modules: **Competitor Intelligence, Content Synthesis, Customer Intelligence, Customer Optimization, Industry Intelligence, Marketing Synthesis, SEO/AEO**. Core is always included.

This distribution is **source-available, not open source**. Internal/commercial business use, customization, and agency/consulting use for clients are permitted under `LICENSE.md`; white-label resale or repackaging it as someone else's standalone BusinessOS product is not.

AURA remains model/provider/vendor/harness agnostic. Each customer can keep a separate copy or, optionally, a separate organization-owned workspace; business-specific context, intelligence, assets, preferences, Learning, extensions, and human knowledge stay inside that workspace unless deliberately integrated elsewhere. AURA is portable-first: no proprietary AURA server/database/UI, ViralTrac account, cloud runtime, Git provider, or second-brain application is required for local operation.

## Start

**AI/agent:** read root `CONTEXT.md` and `core/policies/agent-execution.md` before the first business write. Contract IDs are not executable paths; durable Business Context must use validated canonical objects.

- Automatic first-run message: `WELCOME.md`
- Human: `START-HERE.md`
- Deployment/storage/versioning/Obsidian: `DEPLOYMENT.md`
- Public naming rules: `BRANDING.md`
- Browse what AURA can do: `PLAYBOOKS.md`
- AI/agent: `CONTEXT.md`
- License: `LICENSE.md`
- Public distribution/security boundary: `PUBLIC-DISTRIBUTION.md`, `SECURITY.md`
- Installed modules/dependencies: `INSTALLATION.json` and `distribution/ACTIVE-DEPENDENCIES.json`
- Tasks: `TASK-NAVIGATOR.md`
- Publisher/origin: `PUBLISHER.json`
- Provider defaults: `distribution/provider-defaults.json`

Optional modules are enrichments, not hidden hard dependencies. When one is absent, use `core/policies/module-independence.md`.

## Three deployment experiences
AURA has one operating architecture with three deployment experiences, not three separate products:

1. **Simple — Download and Use.** The product folder is also the workspace. No Git, hosted service, or Obsidian is required.
2. **Power User — Private Versioned Workspace.** Optionally separate organization state from product source, use private Git for history/rollback/multi-device use, and open the human knowledge layer in Obsidian or another Markdown tool.
3. **Organization — Shared Organization Workspace.** Keep a private team-owned workspace with controlled Git/organization infrastructure while the canonical AURA product can be upgraded separately.

Configure a new/empty external workspace with:

```bash
python3 scripts/configure_workspace.py <path> --profile power_user|organization
python3 scripts/workspace_status.py
```

If the current workspace already contains business state, migrate it safely instead:

```bash
python3 scripts/migrate_workspace.py <path> --profile power_user|organization
python3 scripts/workspace_status.py
```

Migration is non-destructive and hash-verified; the old workspace remains intact. `BUSINESSOS_WORKSPACE=<path>` can select the workspace without a local pointer. The `BUSINESSOS_*` namespace is intentionally retained as a technical compatibility identifier after the AURA rebrand.

Refresh the human-readable knowledge layer with:

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

Canonical BusinessOS JSON remains authoritative. `knowledge/<business-id>/_generated/` is a replaceable Markdown view; `knowledge/<business-id>/notes/` is for human working notes and is noncanonical until deliberately incorporated through normal evidence/context governance. A human note can be registered as provenance-backed source material with `scripts/register_human_note.py` without automatically making its statements true.

See `DEPLOYMENT.md` and `core/policies/workspace-and-human-knowledge.md`.

## ViralTrac native companion
When ViralTrac is connected, AURA can dynamically discover its current machine-facing capabilities and use its governed semantic data, measurement, tracking, supported action/receipt surfaces, and event/reactive plane without making ViralTrac a required runtime. The public AURA package contains only integration-facing metadata needed by authorized clients; it does not include ViralTrac's proprietary hosted-application source code or private infrastructure. See `core/policies/viraltrac-native-companion.md`.

## Customization and multi-operator use
AURA separates reusable operating invariants from business/Brand configuration, team/operator preferences, and implementation technique. Durable preferences live as business-scoped `PreferenceProfile` objects and resolve deterministically as business → team → role → operator → one-task preference, always below mandatory AURA/business/Brand/contract/approval requirements. Runs may carry opaque `operator_ref`/`team_ref`/`role_ref` labels and snapshot the effective preferences for reproducibility. See `core/policies/preferences-and-adaptation.md`.

Different models/harnesses may sequentially resume the same durable workspace; WorkRequests can be executed in the same session or by harness-managed workers. AURA does not itself spawn agents or guarantee arbitrary simultaneous writes to the same canonical object are conflict-safe. See `core/policies/shared-workspace-coordination.md`.

## Fresh-business onboarding
For a new business, `scripts/bootstrap_explicit_context.py` can ground setup facts across multiple original user-supplied files with repeated `--source-file` arguments; it preserves each source member reference/hash instead of requiring a manually merged source file. Explicit organization Brand instructions should be persisted as first-class Brand state during the same handoff, preferably with `--brand-profile-file runtime/<brand>.json` (the grounded facts `brand` field remains supported); reusable business/team/role/operator preferences can be persisted before residual work with `--preference-profile-file`. This keeps the first downstream Run portable and preference-aware rather than depending on transient chat context.

For outward Content/Marketing work, intended audience and publication state are separate. A local unpublished homepage, landing page, email, ad, proposal, webinar, or similar draft remains customer-facing and must use the appropriate customer-facing production root, claim governance, required subcontract evidence, and Run provenance. Work created during the current execution is never `imported`/`preexisting` merely because it has not been published.

## Updates
Update checks use official GitHub Releases, are disabled by default, metadata-only, and never auto-install. For a one-time check: `python scripts/check_for_updates.py --force`.

## Attention and changing platforms
AURA keeps portable semantic state for material unresolved attention and versioned external platform changes; it does not require a proprietary notification/scheduler service. Compatible harnesses can query current attention with `python scripts/list_attention.py <business-id> --json` and current platform state with `python scripts/list_platform_state.py <business-id> --json`, then use whatever delivery/scheduling capabilities they provide. Repeated unchanged checks update existing state instead of creating duplicate files.

### Authorization is not a preference
Reusable style/work-method choices belong in `PreferenceProfile`. Current-task permissions and restrictions (for example, do not publish, do not spend, ask before contacting customers, or approval required before deployment) do **not** belong in PreferenceProfile and must not be carried into later sessions as personal preferences. Keep them in the current request/Run/action context; persist formal approvals through the governed `Approval` lifecycle when applicable.

If upgrading a workspace created before this separation was enforced, inspect legacy profiles with `python3 scripts/migrate_preference_profiles.py <business-id>`. After reviewing the dry-run output, apply with `--apply`, then run `python3 scripts/validate_business.py <business-id> --require-context`. The migration removes invalid preference-held authority only; it does not create or infer an Approval.

## Naming compatibility
The official public product name is **ViralTrac AURA**. “BusinessOS” remains the descriptor/category and is retained in stable technical identifiers such as the `businessos` repository name, `BUSINESSOS_*` environment variables, existing contract/object conventions, and other compatibility-sensitive interfaces. See `BRANDING.md`.
