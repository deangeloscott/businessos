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

Inline saves preserve the prior file bytes. Canonical JSON replacements preserve
the prior business record. Native work takes bounded before/after observations
of workspace-owned `attachments/<business>`, `knowledge/<business>` and
`instances/<business>` files. Observations compare timestamps/sizes before
reading unchanged files, do not make model calls, and do not run continuously.
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

## Deferred topics

Voice input and reusing platform-only features; cloud access/off-device backups;
OSC 7501; DeepSeek Harness integration and plugin framework changes; automatic
model routing; external messaging; creative-production walkthroughs; mentions
for named assistants/files/workflows/playbooks; slash commands; copying prompts,
editing with preserved native branches, native feedback destinations; and linking
Aura's existing business goals to native goal controls remain follow-up topics.
Their inclusion here does not represent an implementation or native capability.

## Native protocol references

- [Codex app-server](https://learn.chatgpt.com/docs/app-server), with schemas generated by the installed CLI.
- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) and [official Agent SDK control protocol](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/_internal/query.py).
- [Pi RPC](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md) and [extension UI](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc-extension-ui.md).
- [OMP RPC](https://github.com/can1357/oh-my-pi/blob/main/docs/rpc.md) and [approval modes](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md).
- [Hermes security](https://hermes-agent.nousresearch.com/docs/user-guide/security).
