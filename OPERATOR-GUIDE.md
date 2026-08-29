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

AURA describes required capabilities independently of providers. Existing visible tools should be discovered first; explicit provider preferences come next; trusted optional local capability packs may then satisfy compatible local mechanics before a generic external-provider/manual fallback.

Inspect optional trusted local packs:

```bash
python3 scripts/manage_local_capabilities.py status
python3 scripts/manage_local_capabilities.py recommend --pack local-media
```

For the local media toolkit, a healthy existing `yt-dlp`, `ffmpeg`, and `ffprobe` installation can be bound without reinstalling it:

```bash
python3 scripts/manage_local_capabilities.py bind --pack local-media
```

On a compatible Homebrew environment, the user may explicitly authorize AURA's fixed trusted setup/update/repair recipe:

```bash
python3 scripts/manage_local_capabilities.py install --pack local-media --approve
python3 scripts/manage_local_capabilities.py upgrade --pack local-media --approve
python3 scripts/manage_local_capabilities.py repair --pack local-media --approve
```

The enhanced Homebrew media setup uses `yt-dlp` plus `ffmpeg-full`; a healthy existing standard FFmpeg installation is still accepted. `yt-dlp` supplies permitted media/subtitle acquisition mechanics, while FFmpeg/ffprobe supplies deterministic processing/inspection mechanics. These tools do **not** mean AURA semantically watched or understood a video; the model/harness must still inspect the relevant evidence.

AURA uses only product-owned/reviewable capability-pack definitions for automatic setup. It does not search for a random installer and execute it. System installation/update/repair, new account signup, connection, credential use, spending, publishing, contacting customers, or other consequential external actions still require appropriate authorization.

The user-facing responsibility note for general-purpose local tools is intentionally short: **Use local tools responsibly and only on content/systems you are allowed to access.**

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

Open `knowledge/` in Obsidian or any Markdown tool if desired. Start with `knowledge/<business-id>/_generated/Home.md`. Tracked sources for the same resolved subject are grouped under `Tracked-Subjects.md` so humans can review one understandable subject dossier instead of navigating many SourceProfile JSON files.

The tracked-subject view also distinguishes:

- default/source cadence and signal-specific cadence;
- notification mode (quiet by default unless the user changes it);
- actual verified automatic scheduler binding;
- reminder-only / paused / planned-but-unbound / manual monitoring;
- next useful check and relevant material-change signals.

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

## 11. Attention, monitoring, and proactive operation

AURA can persist material unresolved attention as `AttentionItem` state. It does not require its own notification/scheduler service.

A compatible harness may query:

```bash
python3 scripts/list_attention.py <business-id> --json
```

and use its own Slack/email/push/scheduler capabilities.

For the normal combined monitoring view, use:

```bash
python3 scripts/monitoring_status.py <business-id>
python3 scripts/monitoring_status.py <business-id> --json
```

This shows what AURA is watching, default/source cadence, signal-specific cadence, notification intent, what is due, pause/block state, and whether automatic execution has an actual verified scheduler binding. Normal users should be able to ask the same thing naturally: **“What are you monitoring for us?”**

AURA's default monitoring notification mode is **material changes only**. An unchanged check should update checkpoints silently rather than generate “nothing changed” messages. Users may explicitly choose `due_and_material_changes`, `all_checks`, or `silent`, including different choices for individual signals. Monitoring/check cadence and notification cadence are separate concerns.

For internal/diagnostic due-state inspection:

```bash
python3 scripts/list_due_monitoring.py <business-id>
python3 scripts/list_due_monitoring.py <business-id> --due-only
```

If no scheduler exists, AURA retains the monitoring plan and can refresh overdue work on a relevant future AURA start. It should not interrupt unrelated work merely to clear a backlog. Manual refresh always remains possible.

When a harness/OS/workflow scheduler really creates and verifies a recurring task or reminder, record the non-secret environment binding only after that external schedule exists:

```bash
python3 scripts/register_scheduler_binding.py local sched_example \
  --business-id <business-id> \
  --target-kind subject \
  --subject-key <subject-key> \
  --executor-kind harness_scheduler \
  --executor-ref <actual-scheduler-reference> \
  --cadence-expression "monthly" \
  --verified-at <ISO-date-time>
```

The binding proves schedule mechanics, not that future AURA work ran successfully. A compatible worker/harness is still required. Optional built-in OS scheduling surfaces can be discovered through the `local-automation` capability pack:

```bash
python3 scripts/manage_local_capabilities.py status --pack local-automation
python3 scripts/manage_local_capabilities.py bind --pack local-automation
```

That pack may discover `launchctl`, `systemctl`/`crontab`, or Windows Task Scheduler as available schedule mechanics. AURA remains scheduler-neutral and does not become a daemon.

Pause a semantic watch without deleting its accumulated intelligence with:

```bash
python3 scripts/set_monitoring_watch_status.py <business-id> paused --subject-key <subject-key>
```

Resume it with `active`. If a real scheduler is attached, change the real host schedule too and then update its scheduler-binding receipt/status. AURA deliberately exposes a mismatch if the semantic watch says paused while the host scheduler is still active.

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

AURA product update checks are disabled by default and never auto-install.

One-time metadata check:

```bash
python3 scripts/check_for_updates.py --force
```

Opt in to update checks:

```bash
python3 scripts/set_update_policy.py --enable
```

Optional local capability-tool updates are separate from AURA product updates and occur only when the user explicitly authorizes the local pack update/repair action.

## 14. Where to go deeper

- Human quick start: `START-HERE.md`
- Product overview: `README.md`
- What AURA can do: `PLAYBOOKS.md`
- Deployment/workspaces: `DEPLOYMENT.md`
- Agent operating context: `CONTEXT.md`
- Monitoring continuity: `core/policies/monitoring-continuity.md`
- Optional local capability packs: `core/policies/local-capability-packs.md`
- Public naming: `BRANDING.md`
- License: `LICENSE.md`
- Public/security boundary: `PUBLIC-DISTRIBUTION.md`, `SECURITY.md`
- Maintainer qualification: `qualification/README.md` (source repository only; excluded from public packages)

The operating principle is simple: **the user should not have to operate these mechanics unless they want to.** They exist so AURA can be reliable, portable, inspectable, and controllable underneath a simple natural-language experience.
