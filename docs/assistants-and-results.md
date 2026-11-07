# Agents, scheduled results, and delegated work

Aura organizes native work without running another scheduler or agent service.

## Everyday use

- Open **Scheduled tasks**, choose a task, and use **Results**. The latest result appears first; up to 20 recent results are available. Task settings remain below the results.
- Open **Agents → Create agent**. Give it any name and reusable instructions. Optional AI preferences use the same model picker, favorites, search, and supported effort choices as chats. Changing the AI app clears incompatible preferences; defaults can be restored explicitly. **New chat** starts a separate conversation using those preferences; existing conversations retain their native app and model settings.
- Open an agent to find its recurring tasks and related conversations. **Assign existing task** searches discovered native tasks. Tasks already assigned here are excluded; a task assigned to someone else shows that agent's name and **Move here**. Task details also provide assignment and removal. Each task links to the same results shown under Scheduled tasks.
- **Create scheduled task** from an agent preselects it. A newly created task receives a copy of its agent instructions and its own native schedule. Later profile edits apply to future chat requests and newly created tasks. Existing schedules keep their saved instructions; adjust those through task settings when needed. Assigning an existing task groups it without rewriting its instructions, changing its model or timing, or launching it.
- General conversations are not reassigned from chat details. Use **New chat with [name]** for a dedicated conversation using that agent's saved instructions. Existing conversations and their native histories remain available. Search conversation titles or use **Show more chats** to reach older work.
- Removing an agent removes its saved profile and task grouping. Native schedules, conversations, reports, and produced files remain available in their usual places.

Profiles are business-specific, customizable JSON in `.businessos/view.json`. They travel with workspace backups. They contain names, instructions, model preferences, and task references; credentials and native histories remain separate. Restoring profiles does not activate schedules. A native task unavailable on another computer is shown as an unavailable link.

## Native agents and model assignments

**Agents → Native agents & delegation** opens native definitions for Codex, OMP, Pi, Claude Code, and Antigravity, plus Hermes profiles. OMP also reports its current built-in and plugin-provided task agents; these are shown without copying their definitions or shadowing native updates. Create an agent with a name, a concise description of when to use it, instructions, and optional model settings. Choose project or personal scope. Creating a saved Aura agent can also make it available as a native subagent. Registration makes an agent available; the native harness decides when to invoke it.

The editor changes the native file directly, preserves unfamiliar fields, and checks its revision before saving. The full native definition remains editable for supported settings such as tools, memory, skills, or native delegation policy. Existing native identifiers remain stable in the structured editor. A missing, unreadable, or externally changed file produces an explanation rather than replacing it. Closing the editor does not remove the definition.

**Use instructions in Aura** links a saved agent to that native definition. Future chat requests read its current instructions, rather than a competing saved copy. The lead chat retains its selected model and permissions. Claude Code and Antigravity select the linked native primary agent through `--agent` when supported by its definition. A Hermes link selects its native profile, including its SOUL, memory, tools, and connections. Existing Hermes chats keep their original profile even if the Aura agent is later relinked or removed. Codex, OMP, and Pi lead chats reuse instructions; native subagent-only settings are not claimed to apply to the parent. Native specialist settings apply when the harness delegates to the definition. Existing chats remain separate assignments. Unchanged instructions are not resent on every ordinary turn. Removing the Aura profile preserves native definitions, memory, chats, files, and schedules.

**Delegation settings** reads native defaults and verifies writes through the same readers used for cache/context settings. OMP exposes its native model-role map and named-agent overrides; Codex exposes subagent defaults and concurrency; Claude exposes its native model default; Hermes exposes delegation model/provider defaults. The screen identifies shared app/profile scope and project overrides. Supported ACP connections can report their own delegation controls without an Aura model catalog. Pi requires its compatible subagent extension; Antigravity agent models use its native tiers.

Hermes profiles can be created and edited from the native agent browser. Saving uses its gateway and checks native readback. Skills, toolsets, and MCP servers use the native lists; unchanged choices retain native defaults. Creation includes bundled skills by default and does not copy credentials. Profile-specific model choices and context/delegation settings use that profile, rather than a different connection’s defaults.

Hermes can use named model/profile routes through its optional [official Advanced Delegation plugin](https://hermes-agent.nousresearch.com/marketplace/advanced-delegation) on a compatible version. When Hermes reports the plugin as enabled, Delegation settings includes its native mode, named model/profile routes, and optional defaults. Route edits preserve unrelated native settings and keep existing private credentials out of the browser. These are optional native routing settings, not an Aura model allowlist. Aura preserves native slash commands and does not silently install or enable plugins. The installed Hermes version must satisfy the plugin’s requirements (currently 0.22.5 or later). Installed extensions and harness versions determine available features; file discovery alone does not establish that an agent loaded or that a model request succeeded.

The same controls are available through `/api/native-agents` and `/api/delegation-settings`. CLI users can use `workspace_specialists.py` with `--app hermes --scope profile --file <name>`, and `workspace_agent_settings.py` with `--profile <name>`; each also requires the workspace’s business ID.

Native references store app, scope, and relative filename, or a Hermes profile name. Personal definitions stay in the native app’s configuration directory; back them up or transfer them using that app’s normal mechanisms. Project definitions travel with their project. Native credentials and histories are not copied into Aura profiles. Definitions missing on a different machine must be reconnected. Cross-harness execution and model substitution are not inferred from matching names.

## Native results

Hermes results come from its existing timestamped Markdown files, including profile-specific output folders. Aura reads the selected report without moving or changing it.

Codex local desktop tasks and runs are read from known local metadata when available, with existing automation TOML as a fallback. Results show saved findings or archived replies and link to the original conversation. **Open conversation** uses the existing native-chat preview and confirmation before adding it to the selected business. An unsupported database schema or a cloud-only task may require using Codex directly; Aura never migrates native databases.

Read failures are reported separately from an empty history. **Try again** retries a failed result read without changing the task or resubmitting its work. A failed database read leaves any supported file-based task inventory available with a notice.

Pi tasks with a native session link open that conversation; a session is not presented as individual run history. Other apps keep results in their own interfaces until an adapter can read them. An enabled schedule does not establish that a task ran successfully. Produced files stay where the task saved them; report links use Aura's normal file controls and workspace access checks.

## Delegated work

Chats show expandable **Delegated work** when the native stream reports it. Codex collaboration events, Claude task events, and Pi/OMP extension task details can provide assignments, state, models, and results. Hermes delegation tools can appear as delegated work when their stream exposes those details. Installed versions and extensions determine what is available. Missing model or progress information is not invented.

Native refresh can recover Codex collaboration observations and supported tool results from native transcripts. Aura keeps active observations and their parent links, plus the 50 most recently updated finished observations, with its local chat reference. Active work appears first; **Show more agents** expands the display without another native read. Updates from a single native event are published together. These are interface recovery details, not canonical business memory or context automatically replayed into the model. Child text is kept separate from the parent reply and session identity. No hidden reasoning is collected.

Counts reflect reported child tasks; open-ended work has no invented completion percentage. Unknown child outcomes stay unconfirmed when the parent finishes. The existing **Stop** stops the owning Aura request; it is not an independent per-child control. Hermes gateway work may outlive a local connection, as its normal stop notice explains.

Chat-specific subagent defaults use Codex’s native configuration, Claude’s `CLAUDE_CODE_SUBAGENT_MODEL` environment setting, or OMP’s `task` model role. OMP specialists keep their own role assignments and overrides. Other connections retain existing instruction preferences without claiming a native override. Native delegation settings expose supported app/profile defaults separately; Pi models belong to its native agent files and extension. Normal delegation guidance asks the parent to provide workspace context and resolve child questions before involving the user. Native permissions and actual parent-child messaging remain with the harness.

## Shared interfaces

The UI calls the same Python helpers as these JSON commands:

```sh
python scripts/workspace_assistants.py list --business example-studio
python scripts/workspace_assistants.py save --business example-studio --input '{"name":"Jeff","instructions":"Help with research."}'
python scripts/workspace_assistants.py remove --business example-studio --id ASSISTANT_ID
python scripts/workspace_specialists.py list --app omp --business-id example-studio
python scripts/workspace_specialists.py save --app omp --business-id example-studio --input '{"name":"researcher","description":"Research with sources","instructions":"Return evidence and unknowns."}'
python scripts/workspace_agent_settings.py --app omp --business-id example-studio
python scripts/workspace_schedules.py list --workspace /path/to/workspace
python scripts/workspace_schedules.py history --id TASK_ID --workspace /path/to/workspace
python scripts/workspace_schedules.py result --id TASK_ID --run-id RUN_ID --workspace /path/to/workspace
```

Assistant commands use Aura's normal workspace selection (`BUSINESSOS_WORKSPACE` or the selected workspace). `save` accepts `--input -` for JSON on standard input, including `id` to edit a profile and `task_ids` to group native tasks.

Local authenticated API routes:

- `GET /api/agents?business=…` (also `/api/assistants` for existing integrations) returns profiles and associated chat summaries.
- `POST /api/agents` (also `/api/assistants`) saves a profile; `action` can also be `remove`, `assign_task`, or `assign_chat`.
- `POST /api/chat` accepts `assistant_id` for a new conversation. Existing chat identity determines the assistant on continuation.
- `GET /api/schedules/history?id=…` lists available native results; `GET /api/schedules/result?id=…&run_id=…` reads a selected result.
- `GET /api/native-agents?business=…&kind=…` lists native definitions; add `action=read`, `scope`, and `file` to read one. Authenticated `POST /api/native-agents` accepts `action: "save"`, edited fields or full `source`, and the returned `revision` for an existing file.
- `GET /api/delegation-settings?business=…&kind=…` reads native defaults; authenticated POST accepts `changes` and the returned `revision`.
- Normal chat job/conversation responses include reported `subagents` display details. Native execution, history, cancellation, and model permissions retain their existing owners.

Custom interfaces can use these operations without copying their implementation. No new frontend dependency, daemon, scheduler, automatic model router, or hosted connection is required.


## Reuse context across AI apps

Projects and agents have **Saved context** in their editors. Choose existing files, memory, goals, Library guidance, or a saved answer. Aura stores references, resolves their current sources, and lets the native app read what is relevant. It does not make another copy of those instructions or combine every conversation into one memory. Missing references are reported without stopping ordinary chat. Changed sources are mentioned on the next request; unchanged references are not sent repeatedly.

The context picker searches saved public conversations across connected apps in the selected workspace and business. Archived chats stay out of discovery. Historic answers are source material, and corrections to referenced records take priority. Native-only conversations become searchable after Aura opens or refreshes them; this does not crawl private native memory stores. Native memory and skill building continue in the owning harness. **Your profile → Working preferences** holds optional, user-written preferences for Aura chats on this computer; business facts remain in Business & memory.

```sh
python scripts/workspace_context.py recall --business-id example-studio --workspace /path/to/workspace --search "offer research"
python scripts/workspace_context.py result --business-id example-studio --workspace /path/to/workspace --chat CHAT_ID --variant VARIANT
```

Use `--project NAME`, `--assistant AGENT_ID`, or `--exclude-chat CHAT_ID` to narrow recall. `result` retrieves the exact `variant` returned by recall; omitting it chooses the latest completed public answer. `resolve --input -` accepts a JSON reference array from standard input. Agent profiles accept `context_refs`; project CLI create/edit accepts `--context FILE` containing that same reference array. Workspace-relative references and project folders remain relative in portable workspace settings. External/native sources still need to exist on the destination computer.

Shared API operations: `GET /api/recall` takes `business`, `q`, optional `project`, `assistant`, `exclude_chat`, and `limit`. `GET /api/context/result` takes `business`, `chat_id`, and optional `variant` or `request_id`. Both use the same scope and resolver as the CLI and composer.

## See native activity

Chat **Activity** offers **Highlights**, **Full**, and **Off**. Highlights shows reported plans, progress, file changes, delegation, and failures. Full also includes public thinking summaries and tool inputs/results supplied by the connection. Expand a row to load larger details. Each delegated agent has an Activity action when its native identity is available. Off hides optional activity; approvals, questions, failures, and the final reply remain visible. Display choices do not alter model instructions, native permissions, or execution.

Codex exposes plans, commentary, public reasoning summaries, tools, and reported child activity. OMP uses its native full subagent-event subscription. Pi displays parent events and child messages its installed extensions return. ACP connections expose plans, thoughts, and tools they publish. Hermes exposes parent and child gateway events. Claude displays the public events in its stream. Details that a harness does not publish cannot be reconstructed. Encrypted/private reasoning is not displayed.

Activity is local display history, separate from canonical memory and model context. Per request, Aura retains up to 500 recent entries and about 1 million characters, with 24,000 characters per text or input; a notice identifies excerpts. The workspace display cache keeps up to 200 requests within 64 MB, and finished buffers are released from memory. Old history remains in the native app. Large tool details are loaded on demand rather than copied into each chat poll. `GET /api/chat/activity?business=…&chat_id=…&request=…` returns a small index; add `item=ENTRY_ID` for details or `after=REVISION` for an unchanged response. `python scripts/workspace_trace.py --workspace /path/to/workspace --request REQUEST_ID` reads locally saved details.

## Review saved memory

A successful canonical memory save can show a small **Saved to workspace** card after work finishes: **Keep**, **Edit**, or **Undo**. It comes from verified persistence, not an assistant's prose. Keep dismisses the card; the save already happened. Edit asks your current AI to apply the correction through normal memory helpers. Undo uses existing version history and checks that no newer edit would be overwritten. New records can be removed only when no saved work depends on them. The card does not create an approval inbox or notification-bell item. Saves from concurrent work are labeled as workspace saves, not attributed to the open chat.

`python scripts/workspace_memory_feedback.py list --business-id example-studio --workspace /path/to/workspace` lists recent pending feedback. `keep` and `undo` take `--id RECEIPT_ID`. The UI and authenticated `GET/POST /api/memory-feedback` use those same helpers. Local recovery retention applies; this is not a second source of business truth.
