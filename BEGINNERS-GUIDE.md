# ViralTrac AURA — Beginner's Guide

**AURA = Agentic Understanding and Reinforcement Architecture.**

AURA helps capable AI work for an organization with durable context, evidence, memory, reusable operating knowledge, and continuity across sessions, models, and tools.

You do not need to understand Git, agents, schemas, or programming before you start.

## The simple mental model

```text
AI/model = intelligence
AI app/harness = files, tools, Skills, browsing, execution
AURA = organization-owned memory + reusable operating knowledge
```

AURA does not run its own chat, choose your model, select providers, schedule itself, or control the AI. It helps a capable AI know the organization and continue useful work over time.

The useful loop is:

**understand → retrieve → work → remember → measure → learn → continue**

## What AURA can remember

AURA can preserve things future work should still know or reuse, such as:

- established business facts and evidence;
- customers, competitors, markets, offers, and goals;
- important findings and decisions;
- durable preferences and instructions;
- useful finished work and references to real artifacts;
- meaningful unresolved work;
- measurements and outcomes;
- evidence-supported Learning;
- organization-specific reusable Workflow improvements.

It should not become an activity log. Chats, hidden reasoning, routine tool calls, retries, and throwaway files normally do not belong in durable organizational memory.

## Playbooks, Workflows, and Steps

AURA operating knowledge uses a simple hierarchy:

**Playbook → Workflow → Step**

- A **Playbook** is a meaningful end-to-end business job, such as Competitor Research, Customer Research, Landing Page creation, or Presentation production.
- A **Workflow** is a reusable procedure that helps accomplish part of a Playbook and may also be useful independently.
- A **Step** is the minimum procedural guidance needed inside a Workflow to make the intended result reliably achievable.

You do **not** need to choose these manually. Ask for the outcome in normal language. The model can find relevant AURA knowledge, use another installed Skill, combine both, or use another sound method.

AURA describes what good work requires in natural language. It does not maintain a universal tool/capability allowlist. The active model/harness should use the best tools and resources it actually has.

## What kind of AI tool works with AURA?

The normal local-first experience requires an AI tool that can access the AURA files and organization workspace.

Depending on the tool, that may mean:

- opening or mounting the folder;
- granting local filesystem access;
- running the agent locally;
- exposing AURA through a connector/MCP or other host-native file mechanism.

An important distinction:

```text
AURA awareness = the model knows AURA exists and when to use it
AURA access    = the harness can actually read/write the AURA files
```

The included AURA Skill can provide awareness. It cannot bypass your AI tool's filesystem permissions. Both are needed for the normal experience.

## Get started

### 1. Download AURA

Download the current AURA release and unzip it. If you use Git, cloning the repository is also fine.

### 2. Give your AI access to the AURA folder

Use whatever folder/workspace/file-access mechanism your AI tool normally provides.

If the AI cannot read the AURA files, an instruction telling it to use AURA is not enough.

### 3. Make AURA persistently discoverable

You have several valid attachment methods. Use the simplest native mechanism your harness supports.

#### Preferred: install the included Agent Skill

AURA ships an Agent Skill at:

```text
skills/viraltrac-aura/SKILL.md
```

If your harness supports Agent Skills, install/copy the `skills/viraltrac-aura` folder using that harness's normal personal/global Skill mechanism. The Skill gives the model a small persistent rule for when to consult AURA, how to retrieve relevant context, and when durable results should return to AURA.

You do not need to turn every AURA Playbook into a separate Skill. The AURA Skill can discover Playbooks and Workflows progressively when relevant.

#### Alternative: persistent/global instructions

If your harness does not support Skills but supports persistent instructions, add this and replace the path:

> ViralTrac AURA is available at `/path/to/aura`. For substantive work for an AURA-managed organization, consult relevant AURA organizational memory and operating knowledge when it can materially improve the work. Use your normal tools, other Skills, and best judgment freely. After useful work, preserve the smallest durable organizational meaning that will materially help future work. Ignore AURA for unrelated work.

#### Project/folder-native instructions

When the AI is working directly inside the AURA folder, a harness may automatically read files such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`. If it does, no duplicate global instruction is required for that workspace.

`AURA-ATTACHMENT.md` contains the same attachment model in more detail.

### 4. Tell AURA about the organization

Then talk normally. For example:

> Use AURA for my business. My company is Acme, our website is acme.com, and I want to increase qualified leads. Use what we already know and help me figure out the highest-value work.

If the organization has not been initialized, the AI can use AURA's setup helpers.

### 5. Ask for real work

Examples:

- “Research our competitors and tell me what they're doing better than us.”
- “What are customers saying that we should change?”
- “Find our highest-value SEO/AEO opportunities.”
- “Create a landing page for this offer.”
- “Build a presentation for our sales meeting.”
- “Figure out why qualified traffic isn't converting.”
- “What happened last time we worked on this?”
- “What have we actually learned so far?”

See `PLAYBOOKS.md` if you want to browse the high-level jobs and `WORKFLOW-INDEX.md` if you want the detailed procedures.

## How does the AI know when to use AURA?

The persistent AURA Skill/instruction supplies a small general contract:

1. recognize substantive organization work;
2. identify the correct managed organization;
3. retrieve only context that can materially help;
4. use relevant AURA Playbooks/Workflows when useful;
5. use the host's tools and other Skills normally;
6. do the actual work;
7. preserve durable organizational value afterward when forgetting it would hurt future work.

That same pattern covers Assets, corrected facts, Learning, monitoring intent, and optional work receipts. AURA does not need a separate controller reminding the model about every object type.

## How does AURA know what to remember?

The main test is:

> Would a capable future model working for this organization be materially better off if it knew or could reuse this after the current session is gone?

If yes, preserve the smallest useful durable meaning.

Useful examples include lasting facts, evidence, real decisions, reusable preferences, important research, a finished presentation or website, outcome measurements, and evidence-supported Learning.

Do not automatically preserve every draft or scratch file.

## Where is the real artifact stored?

AURA does not need to copy every binary or external file into canonical JSON.

A real presentation, website, report, design, or other deliverable can remain in the durable location where it naturally belongs. AURA can preserve an `Asset` with the useful identity, location/reference, provenance, status, and relationships future work needs.

## Keeping truth current

AURA follows an important rule:

**Unknown is not absent.**

Not finding something is not proof it does not exist.

When a previously established fact changes, update the current truth. When an entire obsolete object should no longer exist and its references allow removal, use the appropriate forget/correction path. AURA should not keep stale information merely because it was once true.

## Monitoring and reminders

AURA can remember semantic monitoring intent such as:

- what should be watched;
- why it matters;
- material signals;
- cadence intent;
- last meaningful state;
- useful findings.

AURA itself does not wake up on a timer. The active harness, operating system, automation service, scheduler, or webhook mechanism performs actual recurrence and notification delivery.

## Optional work receipts

A `Run` is an optional compact organizational work receipt when continuity or provenance is genuinely useful.

A receipt can truthfully record whether the work materially used an AURA Playbook, AURA Workflow, external Skill, model-created method, or ad-hoc method.

A Run is **not required** to begin work, save organizational memory, create an Asset, prove quality, or authorize execution.

## Organization files versus AURA software

AURA has two kinds of files:

**AURA product files** — operating knowledge, policies, helpers, schemas, and adapter instructions.

**Organization files** — what AURA remembers for the organizations you manage.

For a trial they can live together. For regular use, a separate organization workspace makes upgrades and backups safer.

```text
AURA software folder
        │
        ▼
organization workspace
├── instances/
├── knowledge/
├── attachments/
└── runtime/   (optional continuity/support state)
```

To configure a separate workspace:

```bash
python3 scripts/configure_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

If your current AURA folder already contains organization information, move it safely instead of simply switching paths:

```bash
python3 scripts/migrate_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

## Updating AURA without losing memory

The safest regular setup keeps product source and organization memory separate:

```text
old AURA version ─┐
                  ├── same organization workspace
new AURA version ─┘
```

For an update:

1. keep the organization workspace;
2. obtain the new AURA product version;
3. follow any release-specific migration step;
4. point the new product copy at the same workspace;
5. validate before deleting the older copy.

AURA does not run its own software updater.

## Using several models or computers

AURA memory belongs to the organization, not one AI provider.

The same workspace can be used by different capable models/harnesses as long as each has appropriate access and understands the AURA attachment contract.

Several agents can safely read the same workspace. AURA does not currently promise conflict-free simultaneous writes to the exact same record, so coordinate genuinely overlapping edits.

For multiple computers, you can keep the live workspace on one machine, use private Git where appropriate, or use a trusted sync method. Avoid syncing secrets casually and avoid concurrent edits to the same file.

## Optional local tools

Programs such as browsers, FFmpeg, yt-dlp, document converters, image tools, local search tools, renderers, and other command-line programs may improve particular jobs.

They are not an AURA capability registry. The model/harness should use the best appropriate tools actually available for the requested outcome.

## Do I need ViralTrac?

No. ViralTrac is an optional companion for supported attribution, measurement, experiment, and growth surfaces. AURA remains usable without it.

## Do I need Python?

You do not need to be a Python programmer. Some AURA integrity and persistence helpers are Python scripts, and a capable coding/command-line agent can usually run them for you.

## Common problems

### “My AI does not seem to know AURA exists.”

First separate the two possible problems:

- **Awareness problem:** install the included AURA Skill or add the persistent AURA instruction.
- **Access problem:** grant the harness access to the AURA product/workspace files.

Working inside the AURA folder may solve both for tools that automatically read project instructions.

### “My AI tool cannot open local folders.”

It cannot provide the normal local AURA experience by itself. Expose AURA through another file/connector mechanism the host supports, or use a harness that can access the files. Manual uploads can work for isolated tasks but do not provide the same live shared organizational memory.

### “AURA is asking which business I mean.”

Your workspace may contain multiple managed organizations. Tell the AI which one is active when context cannot resolve it safely.

### “My AI did useful work but AURA did not remember it.”

Ask it to preserve the material organizational meaning. If this happens repeatedly, check that the AURA Skill/persistent instruction is actually active rather than adding another runtime controller.

### “AURA remembered something that is wrong.”

Correct the current truth with evidence. Do not silently preserve the wrong value because it is historical, and do not convert uncertainty into fact.

### “Do I need to choose a Playbook or Workflow?”

No. Tell the AI the outcome. Playbooks and Workflows exist to help the model work well, not to make the user navigate an internal menu.

### “Do I need Git, cloud storage, a notes app, or a special database?”

No. Use extras only when they solve a real need.

## Where to go next

- `PLAYBOOKS.md` — high-level end-to-end business jobs
- `WORKFLOW-INDEX.md` — detailed reusable procedures
- `skills/viraltrac-aura/SKILL.md` — the portable AURA Agent Skill adapter
- `AURA-ATTACHMENT.md` — attachment options and host boundary
- `OPERATOR-GUIDE.md` — advanced use
- `DEPLOYMENT.md` — workspace, storage, upgrades, multi-device, and team details
- `CONTEXT.md` — universal AURA agent contract
- `docs/operating-knowledge.md` — Playbook/Workflow/Step design principle

Start with a real business outcome. Let capable intelligence use AURA when it helps. Keep what matters. Learn from reality. Continue from there.
