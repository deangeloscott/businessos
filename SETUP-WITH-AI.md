# Set Up ViralTrac AURA With AI

This file is primarily for the **AI/agent doing setup**. A human should be able to give a capable agent access to the AURA folder and say:

> Read `SETUP-WITH-AI.md` and set up ViralTrac AURA for me.

The goal is simple: connect AURA to a usable organization workspace, establish the smallest truthful organization identity, prove that retrieval/persistence work, and then start real work.

Do not turn setup into a capability registry, dependency manager, questionnaire, host framework, or execution system.

## Preferred setup path

AURA now has one product-owned setup entry point:

```bash
python3 scripts/setup.py --organization "Organization Name" --json
```

That command is idempotent. It reuses existing configured state, initializes the organization only when needed, and runs AURA's readiness proof.

For a separate organization-owned workspace, supply the path:

```bash
python3 scripts/setup.py \
  --workspace /path/to/aura-workspace \
  --organization "Organization Name" \
  --json
```

When a new external workspace is explicitly selected and no profile already exists, AURA uses the existing `power_user` profile. Existing workspace/profile choices are preserved unless the caller explicitly changes them.

If setup/readiness is already configured and you only need to verify it:

```bash
python3 scripts/doctor.py --business-id <business-id> --json
```

## What `setup.py` owns

`setup.py` is a thin composition layer over existing AURA primitives. It may:

- resolve or configure the AURA organization workspace;
- reuse an existing exact-name organization or initialize the smallest truthful identity;
- derive a stable readable organization ID when that is mechanically safe;
- expose the bundled AURA Skill location;
- run `doctor.py` to prove readiness.

It does **not** create another setup subsystem. The existing workspace, organization initialization, retrieval, persistence, and validation helpers remain authoritative.

## What `doctor.py` proves

Doctor verifies AURA's local mechanics in the executing process. It does not verify that the host has loaded the Skill, that future sessions can locate AURA, or that the model will perform business work well. Confirm host attachment separately through the host when needed.

Readiness means more than "the files exist." The doctor checks that AURA can:

1. resolve the intended organization;
2. retrieve bounded organization context through the normal AURA entry path;
3. create a temporary canonical probe through the ordinary persistence interface;
4. read the probe back;
5. remove it cleanly;
6. validate the organization afterward; and
7. pass product/workspace validation.

The probe is temporary and must not remain as organization knowledge. Doctor does not create a Run or claim anything about business strategy, research quality, host tools, or model capability.

## Host attachment remains host-native

AURA needs both:

- **awareness** — the model knows AURA exists and when it is relevant;
- **access** — the harness can actually read/write the AURA product and organization workspace.

AURA ships a portable Skill at:

```text
skills/viraltrac-aura/
```

`setup.py` reports that source path, but it deliberately does not guess how every harness installs Skills or persistent instructions.

If the host supports Agent Skills, install/copy the bundled Skill using that host's normal personal/global Skill mechanism. If Skills are unavailable, use the minimal persistent instruction from `AURA-ATTACHMENT.md` through the host's normal instruction mechanism.

If the model is already working inside the AURA folder and the harness automatically honors project instructions such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`, do not add redundant configuration just to say attachment occurred.

Do not build an AURA daemon, MCP server, provider router, tool registry, or host adapter framework to solve attachment.

## Rules for the setup agent

1. **Use the setup/doctor entry points first.** Do not manually reconstruct the whole setup sequence unless the supported entry point reports a real problem.
2. **Ask only for missing truth.** An organization name is enough to initialize AURA. Do not force a large business questionnaire before useful work can begin.
3. **Never invent organization context.** Unknown remains unknown. Do not guess industry, services, goals, audience, claims, integrations, or other facts merely to make setup look complete.
4. **Reuse existing state.** Do not duplicate an organization because a chat or harness session is new.
5. **Keep product and organization state separate when useful.** A separate workspace is often preferable for regular use, but one-folder use remains valid and requires less setup.
6. **Use host-native capabilities normally.** AURA does not need to own the browser, shell, code runtime, connectors, MCPs, rendering, scheduling, or provider selection.
7. **Do not install unrelated software during ordinary AURA setup.** Optional tools should be considered only when they materially help the user's actual work, with normal host/user approval.
8. **Finish with real work.** Once readiness is proven, move immediately to the organization's requested outcome.

## Small initial context, progressively learned

After setup, AURA may still know only the organization name. That is correct.

Learn more progressively from:

- explicit user answers;
- supplied files and first-party materials;
- permitted public/first-party research;
- connected tools and business systems available through the host; and
- actual work performed for the organization.

Preserve durable organizational meaning with provenance when it will materially help a future model. Do not ingest every source, tool result, temporary note, or runtime trace simply because AURA is available.

For ordinary durable create/update work, use:

```bash
python3 scripts/remember.py <business-id> --input <json-file>
```

The persistence interface handles mechanical identity, update, and local-reference details where they can be safely inferred. New canonical objects still name their semantic `object_type`. Specialized helpers remain appropriate when their semantics genuinely matter.

After material persistence, report only a small truthful receipt from the actual persistence result, for example:

> Saved to Oregon Tilth: competitor profiles and research report. Validation passed.

Do not create a Run, receipt object, or extra history merely to say a save occurred.

## Manual fallback only when needed

If the setup entry point identifies a real issue, the existing lower-level helpers remain available for diagnosis and repair:

```bash
python3 scripts/workspace_status.py
python3 scripts/configure_workspace.py /path/to/workspace --profile power_user
python3 scripts/list_businesses.py --json
python3 scripts/init_business.py <business-id> --name "Organization Name"
python3 scripts/doctor.py --business-id <business-id>
python3 scripts/validate_business.py <business-id> --require-context
python3 scripts/validate_workspace.py
```

Use those helpers to resolve the specific problem. Do not treat the fallback sequence as the normal onboarding experience.

If existing organization state must move between workspaces, use the supported migration path documented in `BEGINNERS-GUIDE.md` / `OPERATOR-GUIDE.md`; do not copy only selected folders or bypass the migration guards.

## Completion

A successful setup should let the agent tell the user, briefly:

- which organization is active;
- where its AURA workspace lives;
- whether readiness passed;
- where the bundled AURA Skill is located if host attachment still needs to be completed.

Then start the user's first real task.

The normal operating invariant remains:

**identify → retrieve little → work normally → remember what matters → measure/learn → continue**

Setup only makes the first and last mechanical edges more reliable; it does not expand AURA's role.
