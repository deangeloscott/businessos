# Work continuity in Aura

Aura reuses the connected harness's sessions, tools, permissions and execution. The
interface adds small work references, native interaction controls and local file
recovery. It introduces no model router, scheduler, agent messaging service, Git
requirement, database or third-party dependency.

## Find related work without loading every conversation

**Other work** above the chat lists the most recently observed work in the selected
business and workspace, across Aura-connected AI apps. Search titles, assistant
names and existing descriptions; open a chat for its result. The list keeps one
entry per chat and shows when it was observed. A persisted working status without
a running request in this Aura server is labeled **Last observed working**.
**Needs input** requires a pending request in the matching live job; after a
restart, an old receipt can say **Previously needed input** instead. The CLI
exposes `last_needs_input` as an observation, without claiming that an old request
is still answerable. Direct result lookup searches all retained references,
independently of the activity list's display limit.
Native-only sessions may not appear. Status observations are not exclusive file
locks or canonical business truth.

Models can query the same bounded references through the CLI:

```bash
python scripts/workspace_activity.py --workspace <folder> --business-id <id> --search research --limit 10 --json
python scripts/workspace_activity.py --workspace <folder> --business-id <id> --result <chat-id> --max-chars 6000 --json
```

The second command explicitly retrieves one saved public reply, with a source,
status and truncation flag. It does not reconstruct native model context. No
background model calls generate activity summaries. Use existing description
metadata and retrieve only what is relevant. Models still decide what useful,
established meaning belongs in business memory through the normal memory helpers.

For example, Jeff researches an offer in Pi while another chat drafts copy in
Codex. The drafting agent can search the compact activity list, read Jeff's one
result if relevant, then refer to the actual saved research asset. Neither
conversation automatically consumes the other's transcript or gains authority
over its tools.

## Native permissions and questions

**Permissions** beside the chat model changes that chat's next request. An
existing chat can inherit the Aura default or use its own choice. **Settings → AI
permissions** sets the default for each app on this computer/workspace. Defaults
start at **Use harness settings**. Changes do not alter already running requests,
other native sessions, native global configuration or sign-ins.
Using harness settings inherits the native session's current configuration; it
does not revoke grants previously made in that session. Choose an explicit
restrictive mode when that is the intended change.

| App | Session choices exposed by Aura | Native interaction transport |
| --- | --- | --- |
| Codex | Native settings; read-only/on-request; workspace-write/on-request; danger-full-access/never | App-server, native thread/start or thread/resume, then turn/start |
| Claude Code | Native settings; default; acceptEdits; plan; dontAsk; bypassPermissions | Stream-JSON control requests over stdin/stdout |
| Pi | Native settings; extensions retain their own policies | RPC extension UI select, confirm, input and editor |
| OMP | Native settings; always-ask; always-ask-cached; write; yolo | RPC extension UI, including supported ask dialogs |
| Hermes | Native settings; per-launch --yolo | Existing stream adapter; other approvals/authentication stay in Hermes |
| Antigravity/custom | Native settings | Existing adapter; unsupported interactive flows stay native |

These are native modes, not equivalent isolation guarantees. **dontAsk** denies
operations needing approval; it is not bypass mode. Native managed policy, hard
denies, authentication and installed-version restrictions remain authoritative.
A rejected native option is an error, never a silent successful override.
Codex's effective approval/sandbox fields are shown when its server reports them.
`workspace_permissions.py --app <app> --mode <native-mode> --json` describes the
same mapping used by execution and the API.

Supported native questions and approvals appear **inside their originating chat**.
Free text and single/multiple choices use the native request's options. The answer
returns to the same process and native request ID; it does not send another user
prompt, start another turn or change the composer draft. The bell points to a
chat that needs input. It is not a second approval inbox.

Each request can be answered once. Cancellation, native timeout, Stop, disconnect
or completion expires pending controls. A restarted Aura process cannot answer
an old request. Pending grants/answers are not portable configuration. Secret
answers are not cached in Aura's navigation drafts or saved displays. Native
authentication and unsupported MCP forms/control messages are not reimplemented
or auto-approved; use the owning native app for those flows.

For example, OMP asks which of three deliverables to prioritize. Its actual
question appears below the working chat; answering it leaves an unfinished
composer message intact and continues the waiting OMP task. A command approval
offers an explicit one-operation decision without silently granting future tools.

## Automatic local version history

**History** in a workspace file's viewer shows earlier versions. **Settings →
Version history** groups them by path with search and collapsed file groups.
Review a saved version, then restore it. Current bytes are retained before a
restore; a changed current-file revision rejects the operation and asks for a
fresh review. Missing ordinary files can be recreated from a retained version.
Business-record restores use the existing memory persistence and integrity
validation; identity changes, deleted records and specialized record semantics
may require the normal business editor instead.
Restoring a business record replaces its saved semantic extension fields as well
as ordinary content, while preserving identity and normal integrity validation.
If the file restores successfully but its subsequent history update fails, the
UI and shared API/CLI report success with a warning; they do not invite a repeat
restore under the original revision.

Inline saves preserve the prior file bytes. Canonical JSON replacements preserve
the prior business record. Native work takes bounded before/after observations
of workspace-owned `attachments/<business>`, `knowledge/<business>` and
`instances/<business>` files. Observations compare timestamps/sizes before
reading unchanged files, do not make model calls, and do not run continuously.
Small, bounded observation markers remain independent of retained versions, so
expiring a snapshot does not make an unchanged file appear new. Changed snapshots
are committed in bounded batches with one index update/retention pass per batch.
Welcome/cache-warming requests do not trigger file scans. A native-only edit is
observed at the next work boundary, not at every keystroke; unobserved intermediate
versions cannot be recovered.

History is separate machine-local recovery data under Aura's state directory,
keyed by workspace path and business. It is not Git, shared workspace truth, a
portable package, an off-device backup or an undo system for external actions.
It excludes linked/external paths, hidden/private directories, common secret
files, native runtime databases and files over 32 MB. Retention is at most 20
versions per file, 500 entries and 256 MB per business. A boundary observation
checks at most 2,000 files/64 MB; limits and read failures are surfaced rather than
promised as a complete backup.

For example, editing a Markdown plan and choosing Save keeps its previous bytes.
If a native agent later changes it, the observed resulting file is retained too.
Restore one chosen plan version without resetting unrelated files, Git branches,
the Git index, chat history or external publishing actions.

```bash
python scripts/workspace_history.py list --workspace <folder> --business-id <id> --json
python scripts/workspace_history.py show --workspace <folder> --business-id <id> --id <version-id> --json
python scripts/workspace_history.py restore --workspace <folder> --business-id <id> --id <version-id> --expected-revision <reviewed-current-revision> --json
```

The UI and CLI call the same inventory, review, restore and revision checks.
Local HTTP equivalents are `/api/activity`, `/api/activity/result`,
`/api/permissions`, `/api/chat/answer`, `/api/history`, `/api/history/version` and
`/api/history/restore`, protected by Aura's existing local token, origin and
workspace checks. Custom interfaces should call these operations rather than
implement native grants or file writes themselves. Imported assistant/workspace
packages cannot carry sign-ins, permission overrides, grants or live requests.

## Reuse messages and select context

**Copy** copies a message's original text, including Markdown. **Reuse prompt**
puts an earlier user message and its selected references in the composer.
**Use in new chat** opens an unsent draft with the original connection and goal.
An existing draft is preserved; adding to it requires a deliberate choice. A
message originally sent under a different goal offers a new chat with that goal
or reuse under the current chat's goal. Reuse never submits model work.

Type **@** or use **Add context** to find workspace files, saved business context,
goals, library skills/workflows/playbooks and saved public results. Select a
specific library version when several exist. A named assistant opens its saved
results; mentioning it does not dispatch work or create agent messaging.
Selected references appear as removable chips. Saved results pin a particular
reply, so another turn in the source chat does not silently replace it.
Files and business context resolve their current contents when the request is
sent. A message's **Context used** receipt records the selected identities and
revisions; it does not claim that a native app actually read every reference or
freeze a copy of each file. Native history refresh preserves matching receipts.

The picker searches source labels and existing descriptions, without model
calls. It is not a semantic search service. It limits suggestions and sends only
explicit references: at most 12 selected items plus the chat's primary goal,
with a 24,000-character context-guidance ceiling. Other conversations are never
loaded wholesale. Source instructions remain source material, not authorization.

Type **/** to choose **/new**, **/attach**, **/assistant** or **/goal**. These call
the existing new-chat, context, assistant and goal operations. Arrow keys and
Enter select a visible option; Escape dismisses it. Unknown slash text and email
addresses stay ordinary text. The composer remains a plain editable textarea.

For example, reuse an earlier research prompt, select a new product brief with
@, review the chips and edit the draft before sending. Or choose Jeff's one
saved result for a writing chat without starting another Jeff session.

```bash
python scripts/workspace_context.py find --workspace <folder> --business-id <id> --search research --json
python scripts/workspace_context.py resolve --workspace <folder> --business-id <id> --input <references.json> --goal <objective-id> --json
python scripts/workspace_context.py message --workspace <folder> --business-id <id> --chat <chat-id> --index 0 --json
```

Reference input is an array such as
`[{"kind":"file","id":"attachments/<business>/work/brief.md"}]`.
The UI uses `/api/context`, `/api/context/resolve` and `/api/context/message`.
Message reuse verifies the selected text's digest to reject a stale message
index. Custom interfaces use these same shared resolution operations.

## Goals and interrupted work

Aura uses its existing **Objective** records for goals: name, optional outcome
and timeframe, and Active/Paused/Completed status. A chat has one primary goal.
Its goal view groups linked chats and their existing next-step descriptions,
saved Assets and native recurring tasks. Long chat lists are searchable and
initially show 20. Finishing a reply does not complete a goal or invent a progress
percentage. Mark completion when the actual outcome is achieved.

**Work on this goal** creates an unsent draft. **Prepare continuation** checks
what already succeeded before resuming remaining work, without blindly resending
the original assignment or repeating external actions. Useful files, decisions
and concise next steps use Aura's normal durable memory helpers; full transcripts
and private reasoning are not saved as goal memory. An Asset may link to a goal
through `extensions.businessos.goal_ref`.

Goal-linked recurring tasks still belong to their native scheduler. Aura adds a
small goal preflight instruction, then confirms the native task changed before
recording its link. The instruction checks the goal's saved status and original
assignment fingerprint before business work; a paused, completed or materially
changed goal needs review. The task's own model must follow that instruction;
Aura does not intercept independently launched native schedules. Changing or
removing a goal uses the same existing native-task operation, preserving timing,
model and permissions.

**Continuation** defaults to manual. Pi/OMP goal chats may explicitly allow
already-enabled native retries until an expiry within seven days. Aura does not
turn on retries in shared native settings. It uses the native retry event and
abort control, rechecks the goal, permissions and selected context before the
reported retry, and allows only one waiting assignment when funding identity is
unknown. Stop, completion, a new goal assignment or a goal change clears the
authorization. Native retry success clears an earlier transient error.

This is bounded native retry handling, not scheduled quota-reset recovery. The
native app may end a request rather than wait for a reset. Aura and its native
connection must remain running; restarting either does not restart work. Other
connections use the saved chat and manual continuation. A durable goal survives
these interruptions, without a second scheduler, repeated model polling,
automatic model/account switching or a promise to finish unattended.

```bash
python scripts/workspace_goals.py list --workspace <folder> --business-id <id> --json
python scripts/workspace_goals.py show --workspace <folder> --business-id <id> --id <objective-id> --json
python scripts/workspace_goals.py save --workspace <folder> --business-id <id> --input <goal-change.json> --json
python scripts/workspace_goals.py check --workspace <folder> --business-id <id> --id <objective-id> --basis <fingerprint> --json
python scripts/workspace_goals.py link-chat --workspace <folder> --business-id <id> --chat <chat-id> --id <objective-id> --json
python scripts/workspace_goals.py link-asset --workspace <folder> --business-id <id> --asset <asset-id> --id <objective-id> --json
```

Goal changes use the existing canonical memory persistence/schema checks.
Omit `--id` on a link command to remove that association. The `continuation`
command accepts `--chat`, `--mode manual|native` and a Unix-seconds `--until`
expiry, with the same native support and goal checks as the UI.
Chat links and continuation choices go through the running local Aura API
(`--url http://127.0.0.1:<port>`, default 4187), so CLI changes cannot overwrite
live chat settings from a second process. Canonical goal and Asset operations
also work with Aura closed.
`/api/goals` exposes the same goal reads/writes plus chat/task/Asset associations
and machine-local continuation choices. It does not create a universal native
goal-control protocol or replace a harness's own goals.

## Native protocol references

- [Codex app-server](https://learn.chatgpt.com/docs/app-server), with schemas generated by the installed CLI.
- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) and [official Agent SDK control protocol](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/_internal/query.py).
- [Pi RPC](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md) and [extension UI](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc-extension-ui.md).
- [OMP RPC](https://github.com/can1357/oh-my-pi/blob/main/docs/rpc.md) and [approval modes](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md).
- [Hermes security](https://hermes-agent.nousresearch.com/docs/user-guide/security).
