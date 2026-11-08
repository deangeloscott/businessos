# Start Here — ViralTrac AURA

AURA gives your AI a lasting memory of your organization and proven ways to do business work, so each session builds on the last instead of starting over.

```text
AI model        = the intelligence
AI app          = files, tools, browsing, execution (Codex, Claude Code, Gemini CLI, …)
AURA            = your organization's memory + reusable operating knowledge
```

AURA doesn't replace your AI, choose your model, or control what it does. Your files stay yours: plain folders you can open, back up and move.

## Get started

Pick whichever fits you.

**1. Download with Python included (easiest).** Get the bundled download for your computer from the [official releases](docs/bundled-downloads.md), extract the whole folder, and open **Open AURA.cmd** (Windows), **Open AURA.command** (macOS) or **Open AURA.sh** (Linux). A short setup names your workspace, asks what your business does, and connects your AI app.

**2. Let your AI set it up.** Give your AI app access to the AURA folder and say:

> **Read `SETUP-WITH-AI.md` and set up ViralTrac AURA for me. Ask only for information you actually need, prove that AURA is ready, then start the work I want done.**

**3. Do it yourself.** With Python 3 installed, from the AURA folder:

```bash
python scripts/setup.py --organization "Your Organization" --json
python scripts/workspace_ui.py
```

The first command prepares a workspace and proves that saving and reading memory work. The second opens the optional visual workspace. Commands in these guides use `python`; on macOS or Linux, use `python3` if `python` isn't found.

If you have no AI app yet, see [start with a usable agent](docs/tools-and-services.md#start-with-a-usable-agent).

## Make sure your AI can find AURA

Your AI needs two things:

- **Access** — it can read and write the AURA folder and your workspace.
- **Awareness** — it knows AURA exists and when to use it.

Setup handles both for the apps it connects. For other apps, use the simplest option the app supports:

- **Agent Skills:** install the included `skills/viraltrac-aura/` Skill the way your app normally installs Skills.
- **Persistent instructions:** add the short instruction in [docs/attachment.md](docs/attachment.md).
- **Working inside the AURA folder:** apps that read `AGENTS.md`, `CLAUDE.md` or `GEMINI.md` need nothing extra.

## Then just ask for outcomes

You don't need to pick a Playbook, Workflow, model or tool. For example:

- "Research our competitors and tell me what actually matters."
- "Figure out why qualified visitors aren't converting and improve the page."
- "Use what customers say about this problem to write a landing page."
- "What did we learn the last time we worked on this?"
- "What should we work on next if our goal is profitable growth?"

Browse [PLAYBOOKS.md](PLAYBOOKS.md) for the end-to-end jobs and [WORKFLOW-INDEX.md](WORKFLOW-INDEX.md) for detailed procedures if you're curious. Your AI can also combine them with other Skills or use its own method.

## What AURA remembers

Things a future session would be worse off without: established facts and evidence, customers, competitors, offers and goals, decisions, preferences, useful finished work (as links to the real files), measurements and what you learned.

It is not an activity log: chats, routine tool calls and scratch files aren't kept. Unknown isn't treated as absent, and when something changes, the current truth is updated rather than old facts being kept around.

Finished work stays where it naturally belongs (by default `attachments/<organization>/work/` in your workspace) and AURA remembers where it is and what it's for.

## The visual workspace (optional)

Ask your AI to "open my AURA visual workspace", or run `python scripts/workspace_ui.py`. It shows your business memory, files and media, Workflows, agents and scheduled tasks, and can send requests to your connected AI app. Everything still works without it. You can ask your AI to change its layout or build your own view; see [docs/visual-workspace.md](docs/visual-workspace.md).

## Updating without losing anything

Keep your organization workspace separate from the AURA software folder (setup does this by default). To upgrade, download the new release, give your AI access to both folders, and say:

> Read the new version's `SETUP-WITH-AI.md` and upgrade my existing AURA installation, preserving my organizations and saved work.

Keep the old folder until your AI confirms everything is there. Details: [upgrading](SETUP-WITH-AI.md#upgrading-an-existing-installation) and [deployment](docs/deployment.md).

## Several AI apps, people or computers

The memory belongs to your organization, not to one AI provider. Different apps and models can use the same workspace. Several can read at once; avoid two editing the same record at the same moment. For more than one computer, keep the live workspace on one machine or use a trusted sync method or private Git, and don't sync secrets casually.

## Tools and ViralTrac

AURA doesn't require any particular tool. Your AI uses what it has and can suggest something only when it would clearly help. The [tools, models and services guide](docs/tools-and-services.md) lists options and setup links.

ViralTrac is an optional companion for tracking, attribution and experiments. AURA works fully without it.

## Common problems

**My AI doesn't seem to know AURA exists.** It's either awareness (install the Skill or add the instruction) or access (let the app read the AURA folder and workspace). Working inside the AURA folder often fixes both.

**My AI app can't open local folders.** It can't use AURA's live memory on its own. Use an app with file access, or one of its connector options.

**AURA asks which business I mean.** Your workspace holds more than one organization. Say which one.

**Useful work wasn't remembered.** Ask your AI to save what matters. If it keeps happening, check the Skill or instruction is active.

**Something remembered is wrong.** Tell your AI the correct fact; it updates the current truth.

**`python` or `python3` isn't found.** Use the bundled download, or install Python 3 and try the other name.

More: [troubleshooting](docs/troubleshooting.md).

## Where to go next

- [SETUP-WITH-AI.md](SETUP-WITH-AI.md) — setup and upgrade steps for your AI
- [CONTEXT.md](CONTEXT.md) — how AI should work with AURA
- [docs/operator-guide.md](docs/operator-guide.md) — commands and advanced use
- [docs/deployment.md](docs/deployment.md) — workspaces, storage, teams and multiple computers
- [docs/glossary.md](docs/glossary.md) — terms
