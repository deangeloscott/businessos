# Assistants, recurring results, and delegated work

Aura organizes native work without running another scheduler or agent service.

## Everyday use

- Open **Recurring tasks**, choose a task, and use **Results**. The latest result appears first; up to 20 recent results are available. Task settings remain below the results.
- Open **Assistants → Create assistant**. Give it any name and reusable instructions. Optional AI preferences use the same model picker, favorites, search, and supported effort choices as chats. Changing the AI app clears incompatible preferences; defaults can be restored explicitly. **New chat** starts a separate conversation using those preferences; existing conversations retain their native app and model settings.
- Open an assistant to find its chats and recurring tasks. Search chat titles or use **Show more chats** to reach older work. Each task links to the same results shown under Recurring tasks. Assign existing tasks in their details and existing chats in chat details.
- **Add recurring task** from an assistant preselects it. A newly created task receives a copy of its assistant instructions and its own native schedule. Later profile edits apply to future chat requests and newly created tasks. Existing schedules keep their saved instructions; adjust those through task settings when needed. Assigning an existing task groups it without rewriting its instructions.
- Removing an assistant removes its saved profile and task grouping. Native schedules, conversations, reports, and produced files remain available in their usual places.

Profiles are business-specific, customizable JSON in `.businessos/view.json`. They travel with workspace backups. They contain names, instructions, model preferences, and task references; credentials and native histories remain separate. Restoring profiles does not activate schedules. A native task unavailable on another computer is shown as an unavailable link.

## Native results

Hermes results come from its existing timestamped Markdown files, including profile-specific output folders. Aura reads the selected report without moving or changing it.

Codex local desktop tasks and runs are read from known local metadata when available, with existing automation TOML as a fallback. Results show saved findings or archived replies and link to the original conversation. **Open conversation** uses the existing native-chat preview and confirmation before adding it to the selected business. An unsupported database schema or a cloud-only task may require using Codex directly; Aura never migrates native databases.

Read failures are reported separately from an empty history. **Try again** retries a failed result read without changing the task or resubmitting its work. A failed database read leaves any supported file-based task inventory available with a notice.

Pi tasks with a native session link open that conversation; a session is not presented as individual run history. Other apps keep results in their own interfaces until an adapter can read them. An enabled schedule does not establish that a task ran successfully. Produced files stay where the task saved them; report links use Aura's normal file controls and workspace access checks.

## Delegated work

Chats show expandable **Delegated work** when the native stream reports it. Codex collaboration events, Claude task events, and Pi/OMP extension task details can provide assignments, state, models, and results. Hermes delegation tools can appear as delegated work when their stream exposes those details. Installed versions and extensions determine what is available. Missing model or progress information is not invented.

Native refresh can recover Codex collaboration observations and supported tool results from native transcripts. Aura keeps active observations and their parent links, plus the 50 most recently updated finished observations, with its local chat reference. Active work appears first; **Show more agents** expands the display without another native read. Updates from a single native event are published together. These are interface recovery details, not canonical business memory or context automatically replayed into the model. Child text is kept separate from the parent reply and session identity. No hidden reasoning is collected.

Counts reflect reported child tasks; open-ended work has no invented completion percentage. Unknown child outcomes stay unconfirmed when the parent finishes. The existing **Stop** stops the owning Aura request; it is not an independent per-child control. Hermes gateway work may outlive a local connection, as its normal stop notice explains.

Assistant child-model preferences become a per-request native Codex default where applicable. Other harnesses receive the preference in task instructions and use their supported native configuration; Aura does not claim they applied it. Normal delegation guidance asks the parent to provide workspace context and resolve child questions before involving the user. Native permissions and actual parent-child messaging remain with the harness.

## Shared interfaces

The UI calls the same Python helpers as these JSON commands:

```sh
python scripts/workspace_assistants.py list --business example-studio
python scripts/workspace_assistants.py save --business example-studio --input '{"name":"Jeff","instructions":"Help with research."}'
python scripts/workspace_assistants.py remove --business example-studio --id ASSISTANT_ID
python scripts/workspace_schedules.py list --workspace /path/to/workspace
python scripts/workspace_schedules.py history --id TASK_ID --workspace /path/to/workspace
python scripts/workspace_schedules.py result --id TASK_ID --run-id RUN_ID --workspace /path/to/workspace
```

Assistant commands use Aura's normal workspace selection (`BUSINESSOS_WORKSPACE` or the selected workspace). `save` accepts `--input -` for JSON on standard input, including `id` to edit a profile and `task_ids` to group native tasks.

Local authenticated API routes:

- `GET /api/assistants?business=…` returns profiles and associated chat summaries.
- `POST /api/assistants` saves a profile; `action` can also be `remove`, `assign_task`, or `assign_chat`.
- `POST /api/chat` accepts `assistant_id` for a new conversation. Existing chat identity determines the assistant on continuation.
- `GET /api/schedules/history?id=…` lists available native results; `GET /api/schedules/result?id=…&run_id=…` reads a selected result.
- Normal chat job/conversation responses include reported `subagents` display details. Native execution, history, cancellation, and model permissions retain their existing owners.

Custom interfaces can use these operations without copying their implementation. No new frontend dependency, daemon, scheduler, automatic model router, or hosted connection is required.
