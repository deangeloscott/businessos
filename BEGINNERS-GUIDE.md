# ViralTrac AURA — Beginner's Guide

**Alpha · v0.1.0**  
**AURA = Agentic Understanding and Reinforcement Architecture.**

This guide is for anyone who wants to use AURA, including people who are new to AI.

You do not need to understand programming, Git, AI models, agents, or technical file formats before you start.

If you only want to get started, read through **Get started**. The rest of this guide is here when you need it.

## What is AURA?

AURA is a folder that helps AI work with your business over time.

It gives AI a place to find and save useful business information, such as:

- what your business does;
- important facts and evidence;
- customers and competitors;
- goals and priorities;
- decisions you made;
- useful work that was already completed;
- unfinished work that matters later;
- results and measurements;
- lessons learned from previous work;
- useful playbooks for common business jobs.

AURA is not the AI itself. It works with an AI tool that can read and write files.

A simple way to think about it is:

```text
AI = does the thinking and work
AURA = helps the AI understand and remember the organization
Tools = help the AI browse, create, analyze, publish, measure, or do other work
```

The goal is simple:

**understand → retrieve → work → remember → measure → learn → continue**

## If you are new to AI

You may see a few common words when using AURA.

**AI model** — the system that understands your request and produces answers or work. Claude, GPT, Gemini, DeepSeek, and similar systems are examples.

**Agent** — an AI that can do more than answer a question. It may read files, use tools, run commands, browse the web, or complete several steps for you.

**Harness** — the app or program the AI works inside. It gives the AI access to files and tools. In most cases, you can simply think of this as your **AI tool** and ignore the word “harness” unless you need the technical detail.

You do not need to memorize any of these terms. The important part is that the AI tool needs access to the AURA folder if you want it to use AURA.

## What do I need?

For the basic experience, you need only:

1. an AURA folder; and
2. an AI tool that can read and write files in that folder.

You do **not** need Git, Obsidian, cloud storage, ViralTrac, FFmpeg, yt-dlp, a server, or a special database just to use AURA.

Those can be useful later, but they are optional.

## Get started

### 1. Download AURA

Download the current AURA release and unzip it.

If you already use Git, you can clone the repository instead.

### 2. Give your AI access to the AURA folder

Some AI tools automatically read instruction files such as `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` when they work inside a folder.

If your AI does not do that automatically, tell it directly where AURA is.

For example:

> Use the ViralTrac AURA folder at `/path/to/aura` for my business work.

You do not need a special AURA plugin.

### 3. Tell AURA about the business and what you want

For example:

> Use AURA for my business. My company is Acme, our website is acme.com, and I want to increase qualified leads. Use what we already know and help me figure out the highest-value work.

If the business has not been set up yet, the AI can use AURA's setup helpers.

### 4. Talk normally

You do not need to choose a playbook first.

You can ask things like:

- “What should we work on first?”
- “What are our competitors doing better than us?”
- “What are customers saying about us?”
- “Find our biggest SEO opportunities.”
- “Create a campaign from what we learned.”
- “What happened last time we worked on this?”
- “What have we learned so far?”

See `PLAYBOOKS.md` if you want to browse the kinds of work AURA already knows how to help with.

## How does AURA know what to remember?

AURA should **not** save everything you do with AI.

The main question is:

> Would a capable AI working for this organization later be meaningfully better off if it knew this?

AURA should usually remember things like:

- lasting business facts;
- useful evidence and sources;
- important customer or competitor findings;
- real decisions;
- reusable preferences or instructions;
- useful finished work;
- meaningful unfinished work;
- measurements and outcomes;
- lessons supported by evidence.

AURA should usually **not** save:

- every chat message;
- hidden AI reasoning;
- every website the AI opened;
- routine tool calls;
- temporary calculations;
- retries and error chatter;
- temporary files that will not matter later.

AURA is meant to be useful organizational memory, not an activity log.

## Where is my business information stored?

AURA has two kinds of files:

**AURA product files** are the software, playbooks, instructions, and helpers that make AURA work.

**Organization files** are the information AURA remembers about your business.

For a quick trial, both can live in the same AURA folder.

For regular use, it is safer to keep your organization files in a separate **workspace**. A workspace is simply the folder where AURA keeps your organization's information.

Keeping it separate makes upgrades, backups, several computers, and team use easier.

```text
AURA software folder
        │
        │ reads and writes
        ▼
Your organization workspace
├── business memory
├── work history
├── knowledge
└── attachments
```

To create a separate workspace:

```bash
python3 scripts/configure_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

If your current AURA folder already contains business information, **do not just switch folders**. Move it safely with:

```bash
python3 scripts/migrate_workspace.py ~/My-AURA-Workspace --profile power_user
python3 scripts/workspace_status.py
```

The migration helper checks for conflicts, copies the organization files, verifies the copied files, and leaves the old copy untouched.

## How do I update AURA without losing my business memory?

The safest regular setup keeps AURA software and organization memory separate.

```text
old AURA version ─┐
                  ├── same organization workspace
new AURA version ─┘
```

When a new AURA version is released:

1. keep your organization workspace;
2. download or clone the new AURA version;
3. point the new AURA copy at the same workspace;
4. read the release notes for any special move or update step;
5. check that the workspace works before deleting an older copy.

AURA does not run its own automatic updater. Software updates are handled through normal file, Git, GitHub, or other software-management methods.

A future release may sometimes need to change how stored records are formatted. When that happens, the release should provide a safe way to move the old information forward. A normal upgrade should not require starting your business memory from scratch.

## Can I use more than one AI with the same AURA?

Yes.

AURA memory belongs to the organization, not to one AI company or model.

For example, the same workspace could be used by Claude, Codex, Hermes, OpenClaw, a Gemini-based agent, or another AI tool that can access the files.

```text
                 Claude
                    │
Codex ───── organization workspace ───── Hermes
                    │
               another AI
```

This lets one AI benefit from useful information saved by another AI later.

### One important limit

AURA does not currently promise that two agents can safely change the **same saved record at exactly the same time**.

Several agents can read the same workspace. They can also often create different records safely. If two agents may change the same file or record at once, coordinate the work instead of assuming the changes will merge automatically.

## Can I use AURA on more than one computer?

Yes. There are several ways.

### Option 1: Keep the main workspace on one computer

Other computers can connect to that machine using normal remote-access tools.

This is useful when you want one clear live copy of the workspace.

### Option 2: Use private Git

Git keeps a history of changes to files. A private Git repository can also help move the same workspace between computers.

You do not need Git to use AURA.

Git is useful when you want:

- change history;
- a way to return to an older version;
- several computers;
- controlled collaboration;
- backups of text-based workspace files.

Do not put passwords, API keys, private keys, or sensitive raw customer data into a repository unless you understand and accept the security setup.

### Option 3: Use a trusted synced folder

A cloud-storage or local-sync tool can copy a workspace between computers.

This can be convenient, but be careful when two computers edit the same file at the same time. File-sync tools can create conflicts.

AURA does not require a specific cloud-storage company.

## What is the knowledge folder?

AURA stores its main business records in structured files that are easy for software to check and use.

AURA can also make simpler Markdown pages for people to read.

Run:

```bash
python3 scripts/generate_knowledge_layer.py <business-id>
```

This creates readable pages under `knowledge/<business-id>/`.

You can open these pages in an ordinary text editor, VS Code, Obsidian, or another Markdown notes app.

A notes app is only a way to view and write notes. It is not required, and it does not replace AURA's main structured business records.

Human notes do not automatically become trusted business facts just because they are inside the knowledge folder. Important notes can be brought into AURA's evidence process on purpose when useful.

## What are optional local tools?

Some work becomes easier when your AI can use extra programs already installed on your computer.

Examples include:

- **FFmpeg** for working with audio and video files;
- **yt-dlp** for permitted video, audio, subtitle, or metadata retrieval;
- document converters;
- image tools;
- browsers;
- local search tools;
- other command-line programs.

These tools are optional.

AURA describes the business job that needs to be done. The active AI tool should use the best tools it actually has.

Installing more tools can increase what the AI can do locally, but AURA should not depend on one specific tool when another sound method works.

## Do I need ViralTrac?

No.

AURA works without ViralTrac.

ViralTrac is an optional first-party companion for things such as attribution, measurement, experiments, and supported growth work.

## Do I need the internet?

Not for every AURA task.

AURA itself is local-first. You can read existing memory, use local files, create drafts, and perform other local work without a required AURA cloud service.

Some tasks still need internet access because the work itself needs current outside information, websites, APIs, cloud business systems, or online publishing.

## Do I need Python?

You do not need to be a Python programmer.

Some AURA helpers are Python scripts. A capable coding or command-line AI can often run them for you.

If your AI tool cannot run commands, it may still be able to read AURA files, but some setup, validation, and saving helpers may need to be run another way.

## Common problems

### “My AI does not seem to know AURA exists.”

Make sure the AI can access the AURA folder. Work from inside the folder when your AI tool supports that, or tell the AI directly where the folder is and ask it to use AURA for the business.

### “AURA is asking which business I mean.”

Your workspace may contain more than one business. Tell the AI which business is active. AURA should not guess when the choice is unclear.

### “I downloaded a new AURA version. Where is my old information?”

Do not assume a new product folder contains the organization memory from an older product folder.

If you used a separate workspace, point the new AURA version to that same workspace.

If your business information still lives inside the older AURA folder, keep that folder and use `scripts/migrate_workspace.py` to move the information safely before deleting anything.

### “My AI did useful work but AURA did not remember it.”

Ask the AI to preserve the material business meaning from the work. It should save what would materially help a future AI, not the whole conversation.

### “AURA remembered something that is wrong.”

Check the supporting evidence and correct or replace the bad record through AURA's normal evidence and correction process. Do not silently turn uncertain information into fact.

### “Two AI agents are working at the same time.”

Reading the same workspace is fine. Avoid having both agents change the same saved record at exactly the same time unless you have coordinated how conflicts will be handled.

### “I moved AURA to another computer.”

Move or reconnect the organization workspace too. Product files and organization files may be separate.

### “I see JSON files. Should I edit them by hand?”

Usually no. Let AURA's helpers or a capable AI use AURA's normal save methods. The structured files are meant to stay valid and traceable.

### “Do I need to choose a playbook?”

No. Tell the AI the outcome you want. It may use an AURA playbook when one is useful, adapt one, use another Skill or method, or work another sound way.

### “Do I need Git?”

No. Git is optional.

### “Do I need a notes app?”

No. A notes app is optional.

### “Do I need cloud storage?”

No. AURA can work entirely from local files.

## Simple setup choices

### I just want to try AURA

Use one AURA folder with one AI tool.

No extra setup is required.

### I want to use AURA regularly

Keep AURA software and your organization workspace separate.

This makes upgrades and backups safer.

### I use several computers

Use a shared main computer/server, private Git, or a trusted sync method for the organization workspace.

### I am a power user

Consider a separate workspace, private Git, a Markdown notes app, and useful local tools.

Use only the extras that actually make your work better.

### We are a team

Use an organization-owned shared workspace with appropriate access controls. Coordinate simultaneous edits to the same saved records.

## Where to go next

- `PLAYBOOKS.md` — see what kinds of business work AURA can help with
- `OPERATOR-GUIDE.md` — practical commands and advanced use
- `DEPLOYMENT.md` — workspace, storage, upgrades, multi-device, and team details
- `CONTEXT.md` — the main instructions AURA gives to AI agents
- `LICENSE.md` — source-available license

You do not need to learn all of AURA before using it.

Start with a real business outcome. Let the AI use AURA's memory and operating knowledge. Keep what matters. Learn from what happened. Continue from there.
