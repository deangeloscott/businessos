# ViralTrac AURA — Operator Guide

This guide is for **power users, operators, developers, and agent harnesses** that want direct control over AURA's workspace, deterministic helpers, providers, validation, and deployment mechanics.

Normal users do **not** need to operate these commands manually. The preferred experience is still: give a capable agent the AURA folder, describe the business and desired outcome, and let the agent use AURA's supported mechanics internally.

## 1. Product and workspace

AURA can run directly from one local folder. That is the default **Simple** experience.

For a new external workspace:

```bash
python3 scripts/configure_workspace.py /path/to/workspace --profile power_user
python3 scripts/workspace_status.py
```

For an existing populated workspace that must move:

```bash
python3 scripts/migrate_workspace.py /path/to/workspace --profile organization
python3 scripts/workspace_status.py
```

Migration is non-destructive and hash-verified. `BUSINESSOS_WORKSPACE=/path/to/workspace` can select an external workspace without changing product source.

AURA supports the same architecture across:

- **Simple** — product folder is also the workspace;
- **Power User** — optional separate private/versioned workspace;
- **Organization** — shared organization-owned workspace with controlled infrastructure.

Git, GitHub, GitLab, Forgejo, Obsidian, remote servers, and cloud storage are optional adapters, not requirements.

## 2. Agent startup

Before the first business write, an AI/agent should read:

- `CONTEXT.md`
- `INSTALLATION.json`
- `core/policies/agent-execution.md`
- `core/policies/operating-scope.md`

`WELCOME.md` is the first-run human message.

Contract IDs are playbook identifiers, not executable commands or paths.

## 3. Initialize a business manually

If an agent is not doing this automatically:

```bash
python3 scripts/init_business.py <business-id> --name "Business Name"
```

Explicit user-supplied setup facts should be grounded through the supported deterministic bootstrap rather than written ad hoc:

```bash
python3 scripts/bootstrap_explicit_context.py <business-id> \
  --facts-file runtime/business-facts.json \
  --source-file /path/to/original-source
```

For multiple original sources, repeat `--source-file` instead of creating a synthetic merged source solely for grounding.

Useful bootstrap options include:

- `--brand-profile-file` for explicit organization Brand guidance;
- `--preference-profile-file` for reusable working preferences;
- `--residual-request` when setup is only the first part of a broader user request;
- `--initialization-only` only when setup itself is the entire request.

Explicit reusable outward promises/claims or claim constraints should use the helper's approved-claim / claim-constraint support so they become grounded `BusinessClaim` state.

Unknowns remain unknown. Do not fabricate plausible prices, margins, KPIs, audiences, offers, geography, targets, results, or business facts.

## 4. Natural-language routing

Normal work starts from the user's request, not an internal contract ID.

```bash
python3 scripts/route_and_resolve.py "<natural-language request>" --business-id <business-id> --show
```

If you already know a contract ID for inspection:

```bash
python3 scripts/resolve_contract.py <contract-id> --show
```

Composite jobs may expand through:

```bash
python3 scripts/process_plan.py ...
```

Minimal context for executable jobs is produced through `scripts/context_plan.py`.

After setup, preserve and continue the unresolved original outcome automatically. A user should not have to choose a module simply because bootstrap completed first.

## 5. Capability preflight and tools

Before atomic execution, use AURA's capability layer to identify what the current environment can actually do:

```bash
python3 scripts/preflight_capabilities.py ...
```

AURA describes required capabilities independently of providers. Existing visible tools should be discovered first; provider recommendations/fallbacks come afterward.

New account signup, connection, credential use, spending, publishing, contacting customers, or other consequential external actions still require appropriate authorization.

Do not replace a failed deterministic AURA helper with a custom canonical-state writer merely to get around the failure.

## 6. Durable state and Runs

Canonical organization state lives under logical paths such as:

`instances/<business-id>/`

Resumable execution state lives under:

`runtime/runs/<business-id>/<run-id>/`

AURA distinguishes lifecycle states such as drafted, approved, executed, verified, and measured. A local draft is not a production execution merely because the artifact exists.

Preserve prior state and Runs unless deletion/replacement is explicitly authorized. Different models/harnesses can sequentially resume the same durable workspace.

## 7. Customer-facing work and claims

Customer-facing Content/Marketing work should use the appropriate customer-facing production root and preserve its actual Run/evidence lifecycle.

An unpublished homepage, landing page, email, ad, proposal, webinar, or similar outward draft is still customer-facing by intended use.

Use:

- `core/policies/context-provenance-and-claims.md`
- `core/policies/completion-evidence.md`
- `scripts/record_contract_completion.py`
- `scripts/complete_run.py`

AURA should remain flexible about creative expression but strict about factual/outward claims. Do not claim a scan, render, publication, media master, experiment, measurement, or production change that did not occur.

## 8. Preferences vs. authorization

Reusable work/style choices belong in `PreferenceProfile`.

Examples:

- concise reports;
- sparse slides;
- detailed speaker notes;
- preferred output formats.

Current-task permissions and restrictions do **not** belong in preferences.

Examples:

- do not publish;
- do not spend;
- ask before contacting customers;
- approval required before deployment.

Those belong to current request/Run/action context or the formal governed `Approval` lifecycle.

Useful helpers:

```bash
python3 scripts/upsert_preference_profile.py ...
python3 scripts/resolve_preferences.py ...
```

For legacy workspaces:

```bash
python3 scripts/migrate_preference_profiles.py <business-id>
python3 scripts/migrate_preference_profiles.py <business-id> --apply
```

Review the dry run before applying.

## 9. Human knowledge layer

Generate a readable Markdown view of canonical organization knowledge with:

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

Open `knowledge/` in Obsidian or any Markdown tool if desired.

Generated pages are derived/noncanonical views. Human notes remain noncanonical until deliberately incorporated through the evidence/context process.

Register a human note as source material with:

```bash
python3 scripts/register_human_note.py <business-id> <note>
```

Registration preserves provenance; it does not automatically make the note's claims true.

## 10. ViralTrac companion

ViralTrac is AURA's recommended first-party companion, but it is optional.

When already connected, discover its actual current machine-facing capabilities rather than assuming them. Follow:

`core/policies/viraltrac-native-companion.md`

If a host can retrieve a non-secret capability descriptor/manifest, synchronize it with:

```bash
python3 scripts/sync_viraltrac_capabilities.py local --manifest <file>
```

AURA remains the broader business operating authority. ViralTrac may provide governed measurement, tracking, attribution, experiments, interventions, receipts, and supported action surfaces for authorized AURA work.

## 11. Attention and proactive operation

AURA can persist material unresolved attention as `AttentionItem` state. It does not require its own notification/scheduler service.

A compatible harness may query:

```bash
python3 scripts/list_attention.py <business-id> --json
```

and use its own Slack/email/push/scheduler capabilities.

External platform/vendor knowledge can be refreshed independently through `PlatformChange`; repeated unchanged checks should update current state rather than create endless duplicates.

## 12. Validation

Validate active business state:

```bash
python3 scripts/validate_business.py <business-id>
```

After bootstrap:

```bash
python3 scripts/validate_business.py <business-id> --require-context
```

Validate the whole workspace when appropriate:

```bash
python3 scripts/validate_workspace.py
```

For a clean public distribution/package:

```bash
python3 tests/run_distribution.py
```

Maintainers should use the full public release gate before release:

```bash
python3 tests/run_all.py
```

## 13. Updates

Update checks are disabled by default and never auto-install.

One-time metadata check:

```bash
python3 scripts/check_for_updates.py --force
```

Opt in to update checks:

```bash
python3 scripts/set_update_policy.py --enable
```

## 14. Where to go deeper

- Human quick start: `START-HERE.md`
- Product overview: `README.md`
- What AURA can do: `PLAYBOOKS.md`
- Deployment/workspaces: `DEPLOYMENT.md`
- Agent operating context: `CONTEXT.md`
- Public naming: `BRANDING.md`
- License: `LICENSE.md`
- Public/security boundary: `PUBLIC-DISTRIBUTION.md`, `SECURITY.md`
- Maintainer qualification: `qualification/README.md` (source repository only; excluded from public packages)

The operating principle is simple: **the user should not have to operate these mechanics unless they want to.** They exist so AURA can be reliable, portable, inspectable, and controllable underneath a simple natural-language experience.
