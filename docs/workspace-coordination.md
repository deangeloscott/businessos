# Work continuity in Aura

Aura reuses the connected harness's sessions, tools, permissions and execution. The
interface adds small work references, native interaction controls and local file
recovery. It introduces no model router, scheduler, agent messaging service, Git
requirement, database or third-party dependency.

## Find related work without loading every conversation

The shared activity API and CLI list the most recently observed work in the selected
business and workspace, across Aura-connected AI apps. Search titles, assistant
names and existing descriptions; use the chat ID to retrieve its result. The list keeps one
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
| Codex | Native settings; read-only/on-request; workspace-write/on-request; danger-full-access/never | App-server approvals/rules, questions, turn/session permissions, MCP forms and browser steps |
| Claude Code | Native settings; default; acceptEdits; plan; dontAsk; bypassPermissions | Stream-JSON control requests over stdin/stdout |
| Pi | Native settings; extensions retain their own policies | RPC extension UI select, confirm, input and editor |
| OMP | Native settings; always-ask; always-ask-cached; write; yolo | RPC extension UI, including supported ask dialogs |
| Hermes | App-reported modes; explicit native YOLO option | ACP permissions, native options, forms and browser steps |
| Antigravity | App-reported modes; explicit full-access option | ACP permissions, native options, forms and browser steps; explicit auto mode retains the headless transport |
| Custom ACP | App-reported modes | The same ACP client; tools, authentication and supported features come from the configured agent |

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
or connection shutdown expires pending controls. A completed message leaves its live native connection and any later native interaction available. A restarted Aura process cannot answer
an old request. Pending grants/answers are not portable configuration. Secret
answers are not cached in Aura's navigation drafts or saved displays. Native
forms retain their field labels, descriptions, defaults and validation. Browser
steps expose the supplied link; answering never opens it automatically. Native
authentication proofs are never fabricated or auto-approved.

**Send update** appears while Codex, Claude, Pi or OMP is running. It sends the
composer text and selected context to that same native process. Codex uses
`turn/steer` (or a new native turn when only background work remains), Pi/OMP use
their native steering command, and Claude accepts another user message on its
stream. The harness decides when to consume it. Enter keeps an unfinished draft
while work runs; sending an update requires the explicit button. The shared
`POST /api/chat/steer` endpoint takes `business`, `chat_id`, `job_id`, `text` and
optional `files`/`references`; it checks the same live chat/workspace ownership
as `POST /api/chat/answer`.

Stop first requests native interruption on these connections. A five-second
process-tree fallback handles an unresponsive local process. A final parent reply
does not end a Codex connection while known child requests, child work, native
goals or background terminals remain. Claude task and session-state events keep
its stream alive while reported background tasks remain. Pi/OMP use their native
settled state. Closing the browser tab does not stop the server's work. These
connections must remain running; this is not a durable background service after
Aura or the native process exits.
A completed message leaves its native process connected for follow-up messages.
Aura initializes once per live conversation and preserves process-local grants,
extensions and native state. Explicit model, effort, permission or connection
configuration changes reopen the saved native conversation with those settings.
Aura shutdown and explicit Stop close owned work; a disconnected process is not
a guarantee that the native app's own external services stop. Restart never
resends an unconfirmed request or starts a goal automatically. The connection
pool is in the existing Aura server, not a separate service. Archiving a settled
chat releases its idle connection. Pending approvals, native requests and provider
work prevent that cleanup; archiving never silently interrupts them.
Automatic updates also wait while a retained connection has pending interactions
or provider work, even after its parent message has finished.

Repeated messages use a compact business/request envelope once the same native
conversation has received the current Aura guidance. Explicitly selected context,
recovery references and assistant instructions remain available. Aura does not
load every business record or copy another chat's transcript into each request.

Selected PNG, JPEG, WebP and GIF files are passed as native image input to Codex,
Claude, Pi, OMP and image-capable ACP agents. Other files remain scoped native file references. Inline
images have a 32 MB per-file bound; the harness may impose smaller limits. Text
requests accept up to 1,048,576 characters, and saved replies retain their full text.
Large references can be attached as files. Aura does not resend the browser's
display transcript to these native sessions on each message.

Native extension notices, status/widget text, safe browser links and editor
drafts are visible in their chat. An offered draft requires **Use draft** and does
not replace text already in the composer. Terminal-specific extension layouts
still require their native interface.

### Optional native client callbacks

An app-server/SDK can ask its client to execute a client-owned tool, supply an MCP
callback, refresh externally managed credentials or obtain an attestation. These
are implementations supplied by that client, not ordinary built-in harness tools.
Aura can forward such requests to a trusted local provider command in the
machine-owned `--agent-file`; imported workspace records cannot install one:

```json
{
  "name": "My native client",
  "argv": ["my-client"],
  "native_protocol": "codex",
  "native_options": {"thread": {"dynamicTools": []}},
  "native_requests": {"argv": ["my-native-provider"], "timeout": 120}
}
```

`native_protocol` reuses a supported transport (`codex`, `claude`, `pi`, `omp`,
`hermes`, `antigravity`) with that command. It does not infer a different app's
model catalog or grant capabilities. `native_options.thread` passes native Codex
thread-start/resume options; `native_options.initialize` passes native Codex or
Claude initialization options. Existing Codex/Claude connections can instead
receive these options through `connections.codex` or `connections.claude`
in the same agent file. Native policy remains authoritative.

The provider reads one JSON request (`id`, `method`, `params`) from stdin and
returns one JSON object with `result` or `error` on stdout. It inherits the native
process's working directory/environment; diagnostic output belongs on stderr.
Claude callbacks use the same envelope and are translated to its control response.
Answers go to the original request ID. The command must implement the real
provider operation: returning a fabricated authentication or execution success
is invalid. Without that provider Aura explains what is missing and returns a
native unsupported response. It never silently approves an unknown interaction.

Hermes and Antigravity use their documented ACP connection for interactive chat.
Aura reads native model/configuration and permission choices, waits for native
acknowledgements, and returns the exact offered approval option. ACP v1 serializes
prompts, so it does not offer same-turn steering. Each agent's ACP profile remains
native: Hermes may expose a different toolset from its CLI profile. Aura does not
rewrite global profiles or claim every native UI/CLI feature is available through
every protocol. Antigravity's explicit auto permission setting retains its existing
headless transport because its current ACP catalog does not offer that mode.

A custom harness can use the same client with a machine-owned agent configuration:
`{"name":"My agent","argv":["my-agent","acp"],"native_protocol":"acp"}`.
The command is the complete ACP launch command. No brand-specific Aura adapter is
needed for compatible ACP v1 agents. Agent-owned browser/computer tools remain
agent-owned. A desktop-only service, client tool or authentication callback still
needs its actual native provider; Aura never fabricates access or acknowledgements.
Client filesystem/terminal capabilities are not advertised unless a configured
provider implements them. Adding a terminal alone does not provide a desktop
client's private integrations.

Inline native output images are saved once in the business's ordinary work folder
and opened with the existing file viewer. The display transcript stores the file
reference, not base64 image bytes. Refresh retains images attached to an unchanged
reply and reads inline output images when ACP replays them. Context-window usage remains separate from input
or output billing totals; unsupported measures remain unknown.

## Continue with another AI

Aura's own composer shortcuts use `/aura-new`, `/aura-attach`,
`/aura-assistant` and `/aura-goal`. Native command names such as `/goal` are
not intercepted as Aura actions. They reach the connected harness through its
ordinary send path; supported native commands still depend on that protocol.

Choose **Continue with another AI** in the composer's plus menu. Aura prepares an
unsent draft and opens the existing model picker. It pins the last completed
public reply, preserves the current draft text and project, and carries an active
shared workspace goal when applicable. A chat goal remains with its original
chat. The new AI sees one bounded result reference; no full transcript, private
reasoning, credentials or runtime grants move between harnesses. Changed or missing
source messages require selecting a result again.

The same preparation is available through authenticated
`GET /api/chats/handoff?business=<id>&id=<chat-id>` and
`python scripts/workspace_context.py handoff --workspace <folder> --business-id <id> --chat <chat-id> --json`.
Neither operation creates a chat or starts a model request. Normal chat creation
and send APIs consume the returned draft.

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

## Reconnect interrupted work

Aura checks the selected unfinished chat when it opens or when you return to it.
The usual experience stays unchanged. When attention is needed, a small message
appears below the composer with **Check again** and, when appropriate,
**Continue chat**. An uncertain gateway outcome asks you to review recent work
before continuing. Neither action submits an assignment automatically.

Local work receipts retain the existing request reference and the exact native
process incarnation. A surviving process blocks a second request to that chat,
even after Aura restarts. Aura does not adopt or kill an unowned process. Check
again reads its saved display; once that process ends, supported native history
readers can retrieve the latest result. If the native app does not expose live
progress to this new connection, Aura does not pretend to stream it.

A saved final reply for the matching request, or an explicit matching native
final outcome, can recover a completed chat. An earlier reply, an intermediate
tool response, or an absent process alone does not prove completion. A process
check that cannot establish identity remains uncertain. Separate gateways can
outlive their local connection, so their unfinished outcome requires review.

Continue prepares a short request to inspect existing work and finish only what
remains. An existing draft is kept. You review and send deliberately. The API
restores the original assignment and selected references for review if the first
connection ended before its native session could be saved; it cannot resume a
native session whose identity is unknown. The API
checks the latest recovery revision and process state again; a second tab cannot
use an old recovery decision to bypass live work. Deliberate Stop stays stopped,
and previous approvals are never replayed. Existing supported native retries
remain owned by their harness; these checks do not add crash-restart loops,
quota-reset wakeups, task replay, another scheduler, or a background model.

Checks happen at interaction boundaries, share a small short-lived metadata
cache, and keep slow native reads outside the UI lock. They use the portable
product's existing helpers and OS process information, with no workstation-tools,
tmux, cloud account, extra database, or third-party dependency. If Aura's optional
start-at-login setting is enabled, the same checks apply on reopening the chat;
this does not itself restart an interrupted assignment. Native recurring tasks
continue to refresh through their existing task/result inventory.

Custom clients use GET `/api/chats/recovery?business=<id>&id=<chat-id>` or POST
to that endpoint with `action: "check"`. POST `action: "prepare"` includes the
returned `revision` and, for an uncertain result, `reviewed: true`. It returns an
unsent draft and the current conversation. The same operations are available
through the running local Aura instance:

```bash
python scripts/workspace_recovery.py check --workspace <folder> --business-id <id> --chat <chat-id> --url http://127.0.0.1:4187 --json
python scripts/workspace_recovery.py prepare --workspace <folder> --business-id <id> --chat <chat-id> --revision <reviewed-revision> --reviewed --json
```

## Reuse messages and select context

The copy icon on each user prompt copies its original text, including Markdown.
The composer **+** menu contains **Add files or context**, **Goal**, and
**Make a reusable skill**. Skill creation prepares a request for review without
sending it. Permissions sit beside the plus; the model picker sits beside Send.
Creating a chat goal asks for the outcome and links it to this chat. New goals
start active. An optional workspace-goal connection provides broader direction.
**Use a workspace goal only** explicitly connects an existing shared outcome.
Recurring work continues to use the native recurring-task setup.

**Refresh chat** reads saved history from the owning app without sending a model
prompt. It shows progress and a completion or failure message. Draft editing and
scrolling remain available, and a late read cannot replace a newer turn. Slow or
unavailable native apps leave the saved conversation usable.

Type **@** or use **Add files or context** to find workspace files, saved business context,
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
Enter select a visible option; Escape dismisses it. Other slash-prefixed messages
are passed without Aura's contextual envelope. Codex `/compact` invokes native
compaction; `/review` invokes native review of uncommitted changes, with optional
review instructions after the command. Other commands depend on the connected
native interface; desktop menus are not automatically app-server commands. Email
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

Aura uses its existing **Objective** records with two scopes. Existing goals
without scope metadata remain workspace goals, preserving their current meaning.
Goals created from the chat composer belong to that chat's effort. They may
explicitly connect to one workspace goal; completing the effort does not complete
the broader outcome. **Make workspace goal** is an explicit promotion when a chat
outcome should become shared. No arbitrary nesting or separate planning engine is
introduced.

The composer shows the chat goal and its connected workspace outcome separately.
A chat has one selected goal at a time; earlier goals remain in its goal history.
Chat goals are not offered as reusable context or assignable to other chats.
Only the selected goal and its optional workspace connection are added to goal
guidance, within the existing context-size limit. A newer user instruction takes
precedence over goal guidance.

Business & memory and the composer are views of the same Objective records,
not separate business/workspace goal stores. **All goals** filters by scope and
current/completed/deleted status. It shows each chat goal's workspace connection.
Workspace goal details list connected chat goals and their actual saved completion
count; this is not an inferred percentage or a native execution progress estimate.
Back navigation retains the list's search, filters, and scroll position. Linked
files open the ordinary file editor, with a return to the same goal. Inherited
results name their connected-goal origin; removing a link never deletes its file.

Goal views provide **Complete goal**, **Pause goal**, **Resume/Reopen goal**,
**Edit goal**, and **Remove from this chat**. Completion is deliberate; a finished
reply does not complete the goal or invent a progress percentage. Business &
memory lists active workspace goals. **All goals** provides current, completed,
and deleted goals, including earlier chat efforts.

**Delete goal** requires confirmation and retains the goal for recovery from
**Deleted goals**. It removes the current chat selection, cancels future automatic
continuation, and preserves conversations, saved files and historical links.
Restore recovers the goal without reauthorizing continuation. Linked native
recurring tasks retain their existing preflight instructions and need review;
their settings are changed only through the normal native task controls.
Task goal choices are submitted explicitly with **Update goal instructions**;
selecting an option alone does not start a native update. Goal edits made from
an older open panel are checked against the current record before saving, so
they cannot silently overwrite a newer edit.
Routine goal lifecycle and file-assignment bookkeeping does not generate a
canonical correction-review task. Changed outcomes still preserve actual review
impacts. Older correction receipts remain searchable without filling the everyday
saved-context list with technical change logs.

Ordinary entry context, automatic Workflow context, context pickers, and the
generated knowledge overview use active workspace goals. Chat goals and inactive
goals remain available through deliberate selection/history; they are not bulk
loaded as every conversation's business priorities. Earlier interface goal saves
use the same lifecycle operation as `/api/goals`.

The existing Objective extensions store `businessos.goal.scope`, an optional
owning `chat_id`, and an optional `workspace_goal_ref`. An unsent chat goal binds
to its first real chat. Deletion/recovery and goal edits update the goal's revision
so old continuation approval cannot become valid again after a pause or restore.

Starting a chat toward a workspace goal creates an unsent draft. **Prepare continuation** checks
what already succeeded before resuming remaining work, without blindly resending
the original assignment or repeating external actions. Useful files, decisions
and concise next steps use Aura's normal durable memory helpers; full transcripts
and private reasoning are not saved as goal memory. An Asset may link to a goal
through `extensions.businessos.goal_ref`.

Goal-linked recurring tasks use workspace goals and still belong to their native scheduler. Aura adds a
small goal preflight instruction, then confirms the native task changed before
recording its link. The instruction checks the goal's saved status and original
assignment fingerprint before business work; a paused, completed or materially
changed goal needs review. The task's own model must follow that instruction;
Aura does not intercept independently launched native schedules. Changing or
removing a goal uses the same existing native-task operation, preserving timing,
model and permissions.

Native retry policy belongs to Pi/OMP. Linking a goal as context does not abort
their retries or serialize unrelated chats behind an unknown-funding lock.
Pi/OMP goal chats may explicitly apply a bounded continuation expiry within seven
days. Aura does not enable retries in shared native settings. For that explicit
bounded choice only, it rechecks the goal, permissions and selected context before
the reported retry and uses the native abort control if the authorization ended.
Stop, completion, a new goal assignment or a goal change clears that choice.
Native retry success clears an earlier transient error.

This is bounded native retry handling, not scheduled quota-reset recovery. The
native app may end a request rather than wait for a reset. Aura and its native
connection must remain running; restarting either does not restart work. Other
connections use the saved chat and manual continuation. A durable goal survives
these interruptions, without a second scheduler, repeated model polling,
automatic model/account switching or a promise to finish unattended.
Continuation settings are available from the linked goal's **More options**.
Pausing or completing either selected goal disables future automatic continuation;
the current reply keeps running until the user selects **Stop**.
The standard composer keeps the everyday model, permission,
context and goal controls together without a separate continuation setting.

```bash
python scripts/workspace_goals.py list --workspace <folder> --business-id <id> --json
python scripts/workspace_goals.py list --workspace <folder> --business-id <id> --scope all --show current --json
python scripts/workspace_goals.py list --workspace <folder> --business-id <id> --scope all --show deleted --json
python scripts/workspace_goals.py show --workspace <folder> --business-id <id> --id <objective-id> --json
python scripts/workspace_goals.py save --workspace <folder> --business-id <id> --input <goal-change.json> --json
python scripts/workspace_goals.py check --workspace <folder> --business-id <id> --id <objective-id> --basis <fingerprint> --json
python scripts/workspace_goals.py link-chat --workspace <folder> --business-id <id> --chat <chat-id> --id <objective-id> --json
python scripts/workspace_goals.py link-asset --workspace <folder> --business-id <id> --asset <asset-id> --id <objective-id> --json
python scripts/workspace_goals.py delete --workspace <folder> --business-id <id> --id <objective-id> --json
python scripts/workspace_goals.py restore --workspace <folder> --business-id <id> --id <objective-id> --json
```

Goal changes use the existing canonical memory persistence/schema checks.
Omit `--id` on a link command to remove that association. The `continuation`
command accepts `--chat`, `--mode manual|native` and a Unix-seconds `--until`
expiry, with the same native support and goal checks as the UI.
Chat links, deletion/restoration and continuation choices go through the running local Aura API
(`--url http://127.0.0.1:<port>`, default 4187), so CLI changes cannot overwrite
live chat settings from a second process. Canonical goal reads/saves and Asset
operations also work with Aura closed. A later execution rechecks the saved goal
revision before using earlier continuation approval.
`list --chat <chat-id> --scope all --show all` reads that chat's goal history
through the live API too, including the workspace goals it actually used.
`/api/goals` exposes the same goal reads/writes plus chat/task/Asset associations
and machine-local continuation choices. Reads accept `scope=workspace|chat|all`,
`show=active|current|completed|deleted|all`, and an optional `chat_id` for local
goal history. The default is active workspace goals; `show=all` also returns
`deleted_items` separately for recovery views. It does not create a universal native
goal-control protocol or replace a harness's own goals.

## Native protocol references

- [Codex app-server](https://learn.chatgpt.com/docs/app-server), with schemas generated by the installed CLI.
- [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) and [official Agent SDK control protocol](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/_internal/query.py).
- [Pi RPC](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md) and [extension UI](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc-extension-ui.md).
- [OMP RPC](https://github.com/can1357/oh-my-pi/blob/main/docs/rpc.md) and [approval modes](https://github.com/can1357/oh-my-pi/blob/main/docs/approval-mode.md).
- [Hermes security](https://hermes-agent.nousresearch.com/docs/user-guide/security).
- [Hermes ACP](https://hermes-agent.nousresearch.com/docs/user-guide/features/acp) and [Antigravity ACP](https://antigravity.google/docs/cli/acp/).
