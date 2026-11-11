# Changelog

## Unreleased

- **A more polished, consistent interface.** One set of design tokens for text, colour, shape, depth and spacing. Personalization → Text size now scales the whole interface, and a new Compact density option fits more on screen. Dark mode is consistent: leftover colours from an older theme are gone, including a purple focus ring, and maps shade to match. Buttons, inputs, chips, empty states and focus rings now share one look, with gentle motion that respects reduced motion. See [Interface design](docs/design.md).
- **Saved items open beside your work.** Results, records, goals, tasks, files and library items open in a side panel next to the page or chat, with **Expand** for the whole work area. Archiving and board moves show **Undo** instead of sending you to Archived & deleted.
- **Find and do things faster.** Ctrl+K searches and also runs actions ("Add goal", "Add scheduled task", any setting). Settings is one page (Ctrl+,) grouped into General, AI & accounts, Workspace and Help, with search. The bell opens **Activity**: work running now, then notifications.
- **Clearer places and words.** Agents moved into the **Library** as a tab, **Share or import** moved to the workspace menu and Settings, and each place has one name everywhere. Empty places explain themselves and offer a first step your AI can take ("Suggest goals", "Suggest a scheduled task").
- **Results say where they came from.** Saved results show the same small marker everywhere: your correction, how many sources and when they were checked, or "No source". After a reply, results the AI saved or checked appear as cards in the chat that open the result.
- **A neutral Modern look.** Backgrounds, panels, borders and text are now true greys in light and dark mode (dark mode is a soft near-black), so the accent is the only colour and Forest, Ocean and Clay each look right. A new **Mono** accent makes the main buttons black in light mode and white in dark.
- **Styles with their own accents.** Personalization → Style offers Modern plus five looks from computing history: **Classic mono**, **90s desktop**, **90s console**, **2000s desktop** and **2000s console**. Each changes type, shape, edges, depth, scrollbars and colour, works in light and dark, and brings its own accents that set the colour and a signature detail of that era (for example 90s desktop's Teal colours the desktop behind the chat home; 90s console's Charcoal adds a dark case and a four-colour stripe). Choices preview as you pick them and only stick when saved. Everything stays where it is and works the same, and every combination meets WCAG AA contrast.
- **No more half-updated AURA.** If AURA's files change while it is open (a Git pull, a synced or copied folder), it now says **AURA was updated. Restart to finish.** with a Restart button, instead of rejecting new settings with confusing errors.
- **Usage shows which account.** The plan-limit popover now names the account its limits belong to (its saved name and shortened email), with **Switch** when another saved Codex or Claude account could take over. Other apps show their own sign-in when they report it.
- **Watches keep knowledge current instead of piling it up.** Any repeated check (research, competitors, prices, grants, local search, opportunities) now folds what it finds into the organization's findings: new evidence supports, challenges, extends or replaces what is already known, and a finding is added only when it is genuinely new. A collection's page shows **What we know** (each finding with its status: Supported, Unverified, Challenged, Needs review or Replaced), what keeps it current, and when its findings were last reviewed. Findings open in a readable panel with their evidence and quoted sources, the same everywhere in AURA. Each watch keeps its sources as links and key quotes, or also as full copies, and always keeps a copy of fragile sources. Upkeep (rechecking findings that are due, merging overlaps) happens inside the watch's own task, so there is nothing extra to schedule. The ten focus-area watch starters use the new method; the method itself is in `core/policies/keeping-knowledge-current.md`.
- **Continue a chat in another app.** A chat's details (⋯) and Ctrl+K offer **Continue in another app**. Where the receiving app can import the original (today OMP, from Codex or Claude Code), the full conversation moves: AURA runs that app's own importer in a built-in terminal, types the chat's exact ID, confirms the copy from the import record, closes the importer and links the new chat. Every other pair gets a handoff that carries where the work stands, the latest exchanges, the goal, project and folder, and asks the new chat to check the current state before acting. Both chats link to each other, the original says that messages there start a separate version, and the dialog says what carries over, what it costs and which permission setting the new chat uses. The plan-limit backup app uses the same richer handoff.
- **Catch up instead of copying again.** A chat that was continued elsewhere offers **Back to Codex, caught up** (or whichever app it came from), and the Continue dialog lists linked chats first: the existing chat receives what happened since, the latest exchanges and a check of the current state, and continues from there, so there is no third version. The plan-limit prompt offers the full conversation when the backup app can import the chat.
- **Open files stay current.** A file open in AURA reloads its preview when your AI or another app changes it, using a cheap size-and-time check; edits in progress are left alone. SVG images now preview (served sandboxed), and web pages open in your own browser from **Open in…**.
- **Sign in where the error is.** When a chat fails because its app needs a sign-in, **Sign in in terminal** runs that app's own sign-in (`claude auth login`, `codex login`, `omp login`, Pi's `/login`, `hermes setup`) right there.
- **A built-in terminal.** Ctrl+` (or Ctrl+K → Open terminal) opens a real terminal on this computer in a dock under the work area, with tabs, that stays while you move around AURA. It uses each system's own pseudo-terminal (Windows' built-in pseudo console; Python's standard support on macOS and Linux), so nothing is installed; the screen is xterm.js, bundled and loaded only when used. **Add to chat** shares the latest output with your AI when you choose. Accounts & backups can run `claude setup-token`, `omp login` and Pi's sign-in in it. Plain terminals get your normal environment, never AURA's saved keys. Drag its top edge to resize it; the height is remembered. All open terminals share one connection to AURA, so many tabs never slow the page. Terminals end when AURA stops. The window that opens AURA now shows a short header: version, workspace and address.
- **Only real changes ring the bell.** When a watch run finds material changes, the bell says so once ("3 changes in Grants") and the collection shows a dot until you open it; opening the notice goes straight to its changes. Routine checks stay quiet.
- **Reading across workspaces.** Settings → Reading across workspaces lets your other workspaces on this computer use what this one knows, such as research findings, when relevant. It is off by default and set per workspace; reading never copies or changes anything, and the AI says where context came from.
- Saved monitoring plans now link to the watch they belong to, and a watch lists the sources it remembers. `workspace_collections.py instructions` prints the run instructions for a collection, so a task your AI sets up in chat gets the same method as one made through the scheduled-task form.
- Fixed: opening a deadline or goal notification no longer also says "Open your AI app to review this request."
- Fixed: about 1 in 64 chats got an ID starting with "-", which command-line tools such as `workspace_goals.py link-chat --chat <id>` read as an option and rejected. New IDs never start with "-", and the tools accept existing ones.
- Quick setup asks less: after choosing an AI app, **Continue** uses its recommended model, and choosing a model is optional. Open pages refresh themselves when you come back to AURA after a while.

## v0.4.0 — 2026-11-09

- Boards work as pipelines: a `status` or `stage` field gives a board from the first result, and cards move between columns by drag-and-drop or **Move to…** (including a new stage), saved as your correction with the original kept. The bell reminds you once when a saved result's deadline is within 14 days, skipping seen or finished items. The grant workflows flag slow government registrations early, and donor stewardship includes gift receipts.
- New **Funding & Impact** area with four Playbooks: **Grant Funding** (case for support and grant-ready facts saved for reuse, grant prospecting and fit, applications that record each decision and funder feedback, award management and reporting), **Supporter Fundraising** (appeals, donor stewardship and retention, volunteer recruitment and retention), **Impact Measurement and Reporting**, and **Investor Fundraising**. Also **Client Proposal and RFP Response** (Marketing) and **Evidence Synthesis and Literature Review** (Industry Intelligence). The Grants, Nonprofit, Services & B2B, Startup and Research focus areas now point to them.
- **Focus and focus areas.** An organization's focus is its description plus focus areas it chooses (Local business, Multiple locations, E-commerce, Services & B2B, Nonprofit, Grants, Membership & community, Startup, Research, Creative & content), combined freely. Focus changes emphasis, never capability: chats get a short note once per chat, `enter.py` includes it, the home screen offers up to three quick starts (one-time or ongoing watches set up with the app's own scheduler), new goals offer suggestions, the library shows "For your focus", and collections open in a fitting view. Choose or change it in Business & memory, with suggestions from the description; your own or imported areas live in `knowledge/focus-areas/` and never get overwritten by updates. `scripts/workspace_focus.py` and `/api/focus` do the same outside the interface.
- Workspace goals can track a number with a target. The goal shows the latest value, a **Reached** badge when the target is met, and the bell says so once; completing it or setting a new target stays your choice.
- Saved results can be shown as a **Map**, **Chart** or **Board** (Show as, beside the result filter), offered only when the results suit them. The map uses Leaflet with OpenStreetMap imagery, keeps viewed areas so it still shows offline, numbers pins by `rank`, marks `yours: true`, and colours by any small-set field; addresses without coordinates are found through OpenStreetMap's lookup only after you agree, once each. Chart compares results by a number; Board groups them by a status-like field.
- Project pages start with **What's running**: a plain sentence per linked scheduled task (when, which app, where results go and how many wait for review, the goal it serves, and whether it is working), built from saved links rather than a model, with **Change in chat**. Workspace goals use the same sentences and show **Progress** from recorded measurements with their source and date.
- The map shows what changed (a ring on results new in the latest check, ▲/▼ for rank moves, faded pins for results no longer listed), colours or sizes pins by any number, hides groups from the legend, gives each place an **Open in Maps** link and its distance from your business, draws territories (`area` GeoJSON) and service areas (`radius_km`/`radius_miles`), and groups nearby pins once a map has 40 or more (Leaflet.markercluster). Charts show rank movement and, with **Over time**, each result's numbers across checks, from a short per-result trail that never creates a change to review. What's running lists tasks needing attention first.
- `scripts/workspace_views.py` (`rows`, `place`, `running`, `progress`) and matching API routes return the same data to the CLI and harnesses. Collection instructions and the local monitoring workflow ask producers to save places with address, coordinates and rank.
- Make the everyday save cheaper for any AI: workspace and per-request guidance point straight at `CONTEXT.md`, which now carries a one-line `remember.py` example; JSON helpers accept a file, `-` for stdin, or inline JSON and tolerate the UTF-8 BOM Windows PowerShell writes. `Business` gains an optional `description` that retrieval shows inline. A Codex "remember this" request fell from 9 tool calls and ~296K tokens to 4 and ~135K.
- `setup.py` accepts the `--allow-state-switch` flag its own workspace-switch message recommends.
- Setup asks what the business does (optional) and saves it as the business description; Business & memory can edit it later.
- Add any Agent Client Protocol agent from setup (**Add an ACP agent**: name plus launch command). It is saved on this computer outside the product folder, so upgrades keep it, and can be removed from the same place.
- When a native scheduled task stops at its app's plan limit (read from the app's own run records every 10 minutes), the bell says so once and offers to run its instructions now on another account, now in the backup app, or when the limit resets. The task itself stays in its app. Bell items for limits are labelled as such.
- Several accounts and backups (Settings → Accounts & backups). Claude Code chats can run on any added account through Claude Code's own `setup-token` (verified with one tiny request when added); Codex switches by swapping its saved sign-in, keeping chats, after saving the current one. OMP, Hermes and Pi keep their native multi-account handling; Pi's extension can be installed through Pi on request. When a plan limit is near or reached, a short bar under the message box offers another account, a backup app (a new chat carrying the latest result) or continuing the same chat when the limit resets; Ask (default), Automatically or Don't switch, separately for chats and goals. Continuing at reset runs while AURA is open, or through the system scheduler even when it is closed. Secrets stay in OS-protected storage.
- Opted-in usage alerts (plan limit at 90%, monthly budget at 80% and 100%) are checked after every reply instead of only while Usage & spend is open, and say which limit and when it resets.
- A small usage gauge beside the model shows the chat's app plan limit (or context, when the app reports no limits) and changes color as it fills. Hover lists each window, its reset and when it was observed; click shows this chat's context, tokens and cost (charged or estimated) with a link to Usage & spend. Codex limits refresh in the background through its free account read; Claude's arrive with each request. Claude and Codex chats now record context size during live runs.
- Plan limits: when the connected app's 5-hour, weekly or other window is at 90% or more (or reached), a note under the message box says so and when it resets. Claude reports every window (5-hour and weekly) with readable names, attached to the signed-in account in Usage & spend and kept as last known; Codex limit updates during a request are used the same way. Claude's "limit reached" refusals show the usage-limit message.
- Claude goals record Claude Code's own verdict (completed, reason, tokens, time) from its session transcript when the live stream omits it, instead of always asking for review.
- Claude usage reports the turn's final totals; per-message snapshots had shown only a few output tokens.
- Claude activity is labelled by what each step did (command, file, search pattern, sub-agent) with parent and child steps kept apart, and a finished request no longer says background work is running. Plan-mode approvals show the plan.
- Claude Code can read AURA's own guidance and helpers without asking at the start of every chat (`--add-dir` for the product folder); commands and edits still follow its permission mode.
- Apps that do not report a default effort (such as Claude Code) offer **App default** and send no override, instead of silently choosing Low.
- Approval cards show the exact command, file or address an app wants to use, open while waiting; AURA's own setup messages are no longer replaced by a generic error. Model names stay readable after a reload.
- `CONTEXT.md` advises a file for non-English text: Windows PowerShell 5.1 turns such characters into `?` when piping.
- On Windows, npm-installed AI apps that ship a native program (current Claude Code) launch it directly instead of through a PowerShell script that execution policy can block.
- Codex connections default to the effort configured in Codex instead of the model's built-in default. Model names display as the app reports them.
- While a request runs, its status appears once; command activity is labelled with the command it ran and its exit code when it fails.
- `enter.py` prints a compact result by default (about a third of the previous size) and states its boundary once; `--verbose` keeps the full form. Script hints name the helper rather than guessing a `python3` interpreter, and guides use `python`.
- Docs: `BEGINNERS-GUIDE.md` is merged into `START-HERE.md`; the operator guide, deployment, attachment, glossary, branding, public-distribution and Innovation Exchange guides move under `docs/`. Tests no longer pin guidance wording.
- A started chat request now runs as an explicit `ChatRun` (`scripts/workspace_chat_run.py`) instead of closures over twenty captured locals, halving `_start_chat`.
- The visual workspace's HTTP layer moves to `scripts/workspace_http.py`. When the server runs as a script, helpers share the running module instead of loading a second copy.
- Keep covered chat controls out of keyboard and screen-reader navigation on workspace pages, and send Skip to content to the visible page. Describe unclassified native failures without incorrectly claiming the app never connected.
- Connect to Hermes’s native desktop/TUI gateway where available, with native commands, approvals, evaluator-owned goal continuation and confirmed completion. Keep ACP available for older installations and explicit ACP-only settings.
- Preserve normalized native goal assignments and completion contracts without storing AURA’s context as the goal. Reject control through an older assignment when native criteria change.
- Discover native commands in the composer and expose additional ACP select settings in the existing model picker, using exact native IDs and acknowledgements before work.
- Release settled native processes after ten idle minutes while retaining goals, background commands, provider work and pending input; resume saved native conversations on demand.
- Support connection-specific environments for native profiles and account configuration. Add opt-in standard ACP client file and command services without another runtime dependency.
- Check native client portability in the six-platform download workflow, and document supported execution paths and remaining native-service boundaries.
- Keep native account/profile environments consistent during refresh, discovery, usage and task operations. Preserve the selected Hermes profile for saved goal controls and guard changed native criteria before work starts.
- Count Hermes cumulative usage once across replies and reconnections, and close client terminals safely when cancellation races with process creation.
- Apply Hermes provider/model choices through its native model selector, then apply effort, so new chats do not send qualified IDs to the wrong provider or lose their reasoning choice.
- Keep the model picker beside Send at desktop and phone widths. Show the source/current workspace directly under the Share or import title on every tab.
- Honor custom ACP permission modes named full or yolo, and handle native configuration notifications arriving before session loading completes.
- Preserve native output images when refreshing history and read inline images reported by ACP history.
- Release settled native connections when their chats are archived, while preserving pending native work.
- Delay automatic updates while an idle native connection has a pending interaction or provider work.
- Observe idle OMP goal changes and prevent an older saved goal from controlling a replacement native assignment.
- Namespace AURA composer shortcuts with /aura- so native command names are not intercepted as AURA actions.
- Explain unsupported native steps in plain language and keep protocol details in troubleshooting diagnostics.

## v0.3.0 — 2026-11-05

- Keep native conversation processes connected between messages, preserving process-local state and grants. Preserve native background-work settlement, scoped cancellation, and clean shutdown without adding an Aura execution loop.
- Use native ACP for interactive Hermes and Antigravity chats: app-reported models and permission choices, exact approvals, forms, safe sign-in links and output images. Compatible custom ACP agents use the same transport. Explicit Antigravity auto mode retains its existing headless route.
- Add Continue with another AI through the existing composer and model picker. Prepare an unsent draft with one pinned public reply, current text, project and eligible shared goal; preserve native conversation and permission boundaries. The API and CLI share the same operation.
- Avoid repeating unchanged Aura setup guidance on every native message. Use linked project folders for new chats while preserving existing chats' native directories. Keep the current layout and display native output images through the existing file viewer.
- Fix Pi startup settlement ordering, permit native Hermes model changes, retain idle native interactions, redact native display metadata, and distinguish context-window usage from billed tokens.
- Validate real two-message, same-process file-tool workflows on installed Codex, OMP, Pi, Hermes and Antigravity. Claude lifecycle is covered by subprocess fixtures; Claude is not installed on the validation machine. Native profile, protocol and desktop-provider differences remain explicit in the continuity guide.

## v0.2.6 — 2026-11-05

- Add native chat goal execution through supported harness connections, separate from shared workspace outcomes. Codex and OMP report native goal status and budgets; Claude and Antigravity use native goal commands with completion review. Custom harnesses can provide a goal adapter. Pi and Hermes retain goal context when their current connection cannot control native goal mode.
- Add chat pins, persistent projects (including empty projects), optional project folder shortcuts, and one searchable project picker in chat details and the composer. Keep Pinned, Projects and Recents collapsible; preserve the compact sidebar rail in smaller desktop windows.
- Unify workspace search into a labeled, filterable result list with preserved search navigation, activity dates, shared favorites, and separate archive/recovery access. Keep tools and plugins discoverable in the Library without presenting unusable search actions.
- Make chat permissions and model choices use nearby popovers, simplify user-facing language, align favorites and goal actions, and show readable errors while retaining troubleshooting details.
- Repair native transcript refresh and conversation recovery, synchronize shared goal lifecycle operations, and harden memory persistence, workspace isolation and portability. Reuse one dedicated business-context chat instead of placing context requests into an unrelated conversation.

- Preserve the current file and source workspace when opening sharing from Assets, file lists, or linked folders; retain preselection during refresh and reuse saved linked-file selections. Put Share or import beside Preview/Edit, move the copyable path beneath the title, and use Cancel for discarding edits across file types.

- Simplify file actions with one external-editor selector, general Download copy beside Save, reviewed imports, separate sharing, and a single clickable location row. Export pending edits without changing workspace files.

- Use a consistent Edit action and show original-file availability in the save picker, including an explicit read-only option for protected sources.

- Add one local file panel for text/Markdown and CSV/TSV editing, image crop/rotate/resize, PDF viewing/search and streamed media. Share conflict-aware file saves, tracked versions and copies between API and CLI; preserve managed originals and navigation drafts.
- Offer default-app/optional LibreOffice opening and a clear manual Google editing handoff with imported versions. Document bundled components and licenses through Settings and the component manifest. Bundle browser widgets locally and load only the editor in use; exclude development dependencies from distributions.

- Reconnect active chats, history and browser drafts automatically after a verified workspace relocation or explicit missing-folder repair. Preserve independent workspaces and external native projects; offer in-place reconnection for older copied chat settings.
- Scope recovery displays by workspace so retained originals and relocated copies cannot overwrite each other. Continue Pi history through its native project fork when needed, honor native project folders for execution/usage, override Hermes/OMP's saved-folder restoration, and reject unexpected Codex resume IDs.

- Simplify chat details into a single metadata line, group Archive beside Open chat, and remove redundant helper text. Show the full saved latest request when no summary exists, retaining compact list previews without native or model requests.

- Keep message drafts editable when a saved chat belongs to an older workspace folder; explain blocked sending and carry the draft into a new chat here. Preserve prepared skill drafts across reloads and remove misleading wait cursors on disabled controls.
- Add reversible chat archiving through sidebar chat options, with Recent and Archived lists. Preserve native history, saved displays, drafts and usage; working requests cannot be archived.

- Move workspace selection into the sidebar header beside its collapse control. Make Add existing easier to find and keep recent-chat actions visible while scrolling.

- Submit selected feedback through the Aura website using the existing ViralTrac account. Review public feature text and keep diagnostics/attachments private; no email, download or separate account service.
- Add a compact existing-native-chat picker beside Recent chats, with up to five unregistered sessions, exact-ID lookup, source/destination preview and duplicate-safe registration. Preserve native session ownership and project routing.
- Check idle chats for cheap local transcript changes when returning or foregrounding the tab. Refresh only when changed, retain drafts/scroll, and keep manual refresh for remote or unsupported stores.

- Simplify Settings and report preparation: one technical-details choice, attachments below the description, a Submit action, workspace reload beside the version, quick setup first, and profile/name fields side by side. Remove the Help entry and redundant explanatory copy.

- Reuse formatted conversation history during live progress, and reuse unchanged saved records through metadata revision checks. Keep explicit reloads and completed-work inventory refreshes able to pick up external edits.
- Reuse recent file/library discovery, read file inventories outside the chat-control lock, and remove the fixed discovery cutoffs. Render saved files progressively with Load more; search covers the full discovered metadata. Offer bounded file API pages for custom clients.
- Add bounded local request/render performance summaries and an on-demand Settings report form for troubleshooting or feature requests. Include reviewed computer/app/connection details, optional capability names and explicitly selected attachments. Submit currently prepares a local report only; no email, issue submission or download flow is enabled.

- Keep Usage & spend on the selected chat while marking every running chat. Show reported in-flight totals without recording provisional receipts; preserve unknown values and label partial totals.
- Protect usage/history refreshes from workspace changes and newer chat activity. Read native chat history outside the UI lock, retain fast cached browsing, persist refreshed usage, and reuse one Codex account connection per refresh.
- Reduce idle/background polling, coalesce sidebar and usage reads, refresh live usage only while visible, and wake selected-chat polling when returning to the tab. Retain active-work progress, notifications and update edit guards through the existing local API.

- Show shared model favorites first in the compact chat picker. Search the owning app’s full model list, star/unstar from results, and share those choices with the existing AI settings picker.
- Keep personalization requests in one reusable, business/workspace-scoped chat. Opening prepares a draft without submitting AI work or changing an ordinary chat’s draft.
- Align chat status and Usage & spend, keep Aura beside the workspace name with the sidebar collapsed, and give all modal surfaces the same subtle darkened/blurred backdrop. Keep tool pages and contextual panes nonmodal.

- Refine the conversational UI with text-only Aura branding, reversible sidebar controls, aligned tool pages, consistent close/back controls, and full-page sharing and updates. Keep sharing actions and a copyable workspace location in a stable footer.
- Consolidate profile, personal pictures, appearance and custom-layout guidance under Settings. Place notifications beside the profile, keep Usage & spend at the bottom right, and distinguish saved-data reload from native chat refresh.
- Restore saved chat displays immediately and refresh native history only when requested. Cache successful native refreshes and hide Windows metadata/cleanup subprocesses.
- Add per-chat model and effort selection without changing other chats or global defaults. Keep the owning app fixed, protect pending choices, and require a new Hermes session where its CLI cannot change startup options. Treat stopped Hermes gateway outcomes as needing a check before continuing.

## v0.2.5 — 2026-10-31

- Make the standard interface a conversational workspace with a persistent sidebar, readable chat area, contextual file/memory panels and responsive navigation. Use restrained warm surfaces, clear typography and coordinated light/dark themes.
- Run independent conversations concurrently through the existing native adapters. Pin each request to its workspace, business, connection, model, effort and Stop handle; retain background progress while navigating.
- Preserve per-chat drafts and scroll position, restore live requests without resending, and require an explicit outcome check after an interrupted process. Keep restart, relocation and updates guarded during work.
- Add workspace search, selected file references, optional personal greetings, appearance preferences, keyboard navigation and safe diagnostics. Keep custom views on the same local API and preserve standard-view recovery.

## v0.2.4 — 2026-10-31

- Add local preparation for the Aura Innovation Exchange: selected reusable files and methods, portable public metadata, and attached community terms/source notices. Keep business records private and publication separate from local export.
- Open the hosted community catalog from Sharing and the library. Discover/import both existing package families, choose a subset with required supporting materials, and use the existing review, local-copy, conflict and undo behavior.
- Clarify community rights: free sharing/adaptation and business use with credit; paid services remain allowed; contribution access/resale fees require separate permission. Preserve Aura's source-available runtime restrictions.

- Add stable, editable AURA chat titles and short evolving descriptions with current progress and next steps. Descriptions use native metadata or the existing AI reply, with no separate automatic summarization call.
- Order chats by recent activity; show description freshness, saved status and app/model details. Refresh native history without changing the active conversation, and keep older descriptions visibly uncertain when later activity is not summarized.
- Keep chat metadata in machine-local settings, separate from business memory. Preserve user-chosen titles and hide bounded description metadata from the AURA conversation display.

## v0.2.3 — 2026-10-30

- Added separate Workflows, Recipes, Skills, Tools, and Plugins in one searchable library. Include existing Playbooks as complete guides under Workflows; group shared skills and service actions while retaining their actual versions, requirements, and native app connections.
- Discover capabilities through known local files, installed package metadata, and supported native catalogs. Distinguish installed, configured, reported, and locally found items; retain earlier results marked Needs refresh when a catalog check fails. Keep distinct non-English service names separate.
- Save business-specific library favorites and recently chosen items with portable workspace preferences. Prepare a request uses readable titles and instruction locations, preserves unsent drafts, and never sends automatically or silently installs, changes apps, or tests a paid service.
- Improve home and full-view search for business memory, saved files, and recurring tasks. Keep media-type filters, consistent Open labels, bounded collections, compact schedule rows, frequency labels, and pause visibility controls.
- Create and adjust recurring tasks through an isolated operation so the main conversation and selected model remain intact. Read back native tasks before confirming saves; show native last-run information and Hermes saved results where available.
- Protect the current workspace from late state, conversation, file, and library responses. Improve shared layout alignment and scrolling while preserving local-first files, direct native-app/CLI use, and the existing customizable interface.

## v0.2.2 — 2026-10-29

- Added quiet version notices, release notes, Update now, Later, and Skip this version through the existing local interface. Notify me is the default; automatic updates are optional and wait until idle.
- Combine startup and update preferences in Settings → Startup & updates. Verified native bundles install separately, reopen the same workspace, preserve customizations, and retain the previous app for recovery.
- Keep credentials, business data, custom views, and native AI apps separate from product updates. Source/customized installations and incompatible workspace changes use manual guidance.

## v0.2.1 — 2026-10-28

- Added a compact Usage & spend panel with subscription quota windows, masked account history, API balances/allowances where available, and Chat/Today/Month token and cost totals. Distinguish recorded workspace activity from account-wide provider reporting and keep unknown values unavailable.
- Reconcile confirmed provider identities across apps without double-counting shared accounts. Keep distinct accounts separate and offer reversible, user-confirmed account links when a native connection omits identity.
- Show cache reuse and estimated context for the main chat plus up to four recent chats. Prefer observed retention; clearly label fallback OpenAI/Gemini cache windows as reference estimates with their assumptions. Add optional manual Keep warm attempts in the same native chat without automatic pings or model/account switching.
- Add optional quiet quota/budget alerts through the existing notification bell. Keep receipts, masked account snapshots, alert preferences and cache estimates local to the machine, outside portable business memory and credentials.
- Give subscription providers, APIs, cache/context and token costs consistent expanded and compact views. Show all three usage periods together, keep budget controls compact, and place Keep warm beside the chat details without disturbing metric alignment.
- Preserve portable workspaces, native-app/CLI use, provider choice and customizable visual files. Availability of quotas, balances, pricing and retention metadata still depends on each native app/provider; estimates are not a complete billing ledger or a cache-retention guarantee.

## v0.2.0 — 2026-10-28

- Find existing AURA work in recent and common locations, preview older folders, and reuse the last workspace across product downloads. New visual workspaces default to Documents/AURA Workspaces, with a choice of another location.
- Bring scattered workspaces and project folders together through a review, a verified copy, and an explicit choice to keep businesses separate or combine them. Preserve current business information, source records, conflicting versions, project structure, and file references without deleting originals.
- Added optional cleanup through AURA Recovery, restore controls, and opt-in retention. Changed files, exclusions, unresolved dependencies, and an unavailable or altered result block unsafe removal. Recovery keeps originals until the user chooses otherwise by default.
- Carry portable appearance, model favorites, linked locations, and workspace-owned custom views across copying and backups. Include permitted linked files when requested, repair relocated references, and leave native chats, account keys, and scheduler ownership with their apps.
- Added optional Start AURA when I sign in, reuse of the running visual workspace, and guarded restart/quit controls. Added schedule discovery for supported Pi schedule-prompt jobs and Google Antigravity sidecars alongside Codex and Hermes inventories; direct edits remain limited by each host.
- Improved natural-language labels, shared form spacing, expanded-section layout, checkbox/button spacing, sticky navigation, and workspace dropdown colors in light, dark, and system appearance.
- Keep native-app and CLI use available through the same file-based guidance and organization helpers. Bundled downloads retain private Python and required libraries for all six OS/processor targets.

## v0.1.17 — 2026-10-27

- Added app-specific installation/sign-in guidance to the existing connection screen. Existing working connections continue normally; setup never installs a provider or sends an AI request silently.
- Drain bounded native error output for all six adapters and redact credentials before display. Failed requests show a simple remedy, optional details, and Edit & retry without automatic resubmission.
- Save each visible request before starting its native process; keep a local recovery display across restart, including Codex failures before a native conversation exists. Native history/context remains authoritative.
- Added Open existing workspace, recent workspace locations, and Back up or restore in Settings. Opening an older installation follows its existing workspace pointer and checks readiness before switching. ZIP backups verify file hashes; restore stages and verifies bytes before copying into a new/empty folder. Originals stay in place.
- Added macOS Keychain and available Linux Secret Service keyring support for optional saved API keys. Session-only storage stays available when protected storage is unavailable or locked. Keys remain outside business files and prompts.
- Prepare scoped AURA instruction pointers for Claude Code, Pi, OMP, and Hermes while preserving existing instructions. Unknown attachment mechanisms retain explicit request guidance. Apple signing/notarization and unsupported scheduler APIs remain separate limitations.

## v0.1.16 — 2026-10-27

- Added native bundled downloads for Windows x64/ARM64, macOS Intel/Apple Silicon, and Linux x64/ARM64, with private Python, required libraries, retained third-party notices, and an Open AURA launcher. The lightweight ZIP and direct native-app/CLI use remain available.
- Pinned runtime archives and platform wheels by SHA-256. Native release builds verify relocated downloads with spaces in their paths, no system Python on PATH, Tcl resources, isolated libraries, and real first-use workspace setup before connecting an AI.
- Added a read-only, manually triggered native build matrix; build tooling and runtime binaries stay outside portable business memory. Account sign-in, models, and optional tools remain user-owned choices.
- Preserved existing AI-app interpreter precedence while making AURA’s private interpreter available as a fallback; helper requests still identify its exact path.

## v0.1.15 — 2026-10-27

- Added an optional local visual workspace for business memory, saved files/media, separate categorized Workflows and recipes, and recurring work. Native AI apps and CLI use remain fully usable without it.
- Added a guided first-use setup with workspace naming/switching, AI app selection, model discovery, provider filters, favorites, remembered per-model efforts, a short tour, and a local welcome credited to DeAngelo Scott. The optional starter asks one question and waits; setup does not automatically send model requests.
- Added native command connections for Codex, Claude Code, Pi, OMP, Hermes, and Google Antigravity, reusing host sign-in, permissions, model metadata, and saved conversation IDs. Native history is reread where exposed; Antigravity uses a labeled display copy while continuing its native conversation. Supported capabilities depend on the installed app/version.
- Added Stop, Stop & send follow-ups, public reply streaming, elapsed time, and compact activity updates. Added plain-language reply guidance and the actual Python executable for helpers; hidden reasoning and raw tool arguments stay out of the activity view.
- Added independent status checks for explicitly connected apps and actionable recovery messages for sign-in, billing, quota, model access, network, service, and file-access failures. Catalogue availability is distinguished from account entitlement.
- Added optional API-key presets and custom services with session-only storage or Windows user-encrypted storage. Credentials and machine-specific connection preferences stay outside portable business memory and release downloads.
- Added a unified view of readable local Codex/Hermes schedules, with supported native editing/pause/resume or an explicit handoff where direct controls are unavailable. Saved plans remain distinct from confirmed schedules; no AURA scheduler is installed.
- Added explicit links to existing local files/folders, organization-scoped file previews, direct workspace-name/goal editing through existing persistence, saved chats, a notification inbox, and System/Light/Dark appearance.
- Kept the interface customizable through an organization-owned copy, separate from product updates. No required cloud service, AURA account, database, frontend build, or background daemon was added.
- Extended release verification to launch the visual workspace from a fresh ZIP with isolated preferences and an external organization workspace. Public-distribution credential checks now include HTML, CSS, and JavaScript assets.

## v0.1.14 — 2026-10-24

- Added an optional tools, models, and services guide with official setup links for agents, intelligence, creative production, hosting, payments, customer work, outreach, and analytics, including Apollo and Instantly.
- Added minimal bootstrap and connection guidance: reuse existing access and preferences, consider native capability combinations, and confirm access through the first useful task where possible.
- Clarified that providers and tools remain user-owned choices, unlisted providers need no AURA registration, and the guide does not claim tested integrations.
- Added concise guidance for optional future referrals; this release includes official links only and no referral links.
- Updated the human, agent, Workflow, attachment, and distribution entry points to use the guide without adding runtime, provider, or registry machinery.

## v0.1.13 — 2026-10-24

- Respect each canonical schema's timestamp fields in generic saves, including PlatformProfile's observation-time contract.
- Validate declared source digests independently of reference route and descriptive access labels. Add optional explicit access classification and text/payload/file-byte hash targets, with warnings rather than guessed migrations for ambiguous historical evidence.
- Roll back newly created research records and evidence snapshots when bundle validation fails; preserve existing records and caller-owned files.
- Reuse shared weighted lexical discovery for saved work, including filenames and ordinary purposes; add bounded pagination and readable version/location metadata.
- Preserve linked correction impacts as existing ChangeEvents, expose pending semantic review during entry, and report generated-view freshness from canonical content rather than counts.
- Derive native knowledge sections from schema ownership; stage and verify UTF-8 views before Windows-safe replacement with rollback. Preserve human notes and authored history.
- Report unreadable canonical files alongside usable retrieval results, without treating unrelated support files as canonical records.
- Align human-note, initialization, explicit-onboarding and contribution-import sources with the shared evidence contract. Preserve exact captures, declare digest targets, accept historical bare SHA-256 hex, and allow unchanged native notes to gain missing capture metadata without changing identity.
- Document evidence-aware workspace upgrades: retain original hashes/history, recapture changed files, repair only supported metadata, and refresh generated views without automatically promoting supplied statements to verified truth.

## v0.1.12 — 2026-10-21

- Correct three existing regression assertions to expect portable forward-slash references on Windows; native path input coverage remains intact.

- Resolve explicit saved-record requests without selecting a Workflow; report unresolved IDs and retrieval errors instead of silent readiness. Entry also offers bounded literal saved-work candidates with readable titles, status and artifact pointers, and accepts the usual `--json` flag.
- Use explicit UTF-8 on shared setup, retrieval and persistence paths and portable paths in generated navigation. Improve save examples, error context and the stated scope of validation.
- Make useful progress under incomplete information the normal guidance: investigate decision-relevant unknowns, recommend with explicit assumptions, use available fallbacks, and separate delivery, implementation and later outcome measurement. Clarify representative onboarding, diagnosis and retention workflows without adding a mode, controller or required records.

## 0.1.11 — Alpha

Adds adaptable visual craft references and makes AURA's optional navigation and selective context retrieval clearer and lighter without changing AURA's operating model.

### What changed

- Added optional [conceptual and editorial image](recipes/creative/conceptual-editorial-image.md), [annotated detail and mechanism](recipes/creative/information-design/09-annotated-detail-and-mechanism.md), and [thumbnail and cover](recipes/creative/thumbnail-cover-concepts.md) references. They remain borrowable starting points for expressive, explanatory, and browse-scale visual work rather than required templates or production paths.
- Improved Playbook/Workflow discovery with deterministic lexical normalization, document-frequency weighting, complete-word matching, explicit matched terms, authored source paths, and bounded results. Discovery remains navigation help; semantic applicability, method choice, and execution remain with the active model/user/harness.
- Added one installed-aware optional recipe-menu pointer, separated primary organizational context from supporting policy/schema/authored-reference pointers, kept applicable preferences primary, and stopped bulk-loading multiple BusinessClaims when the model/user has not selected one.
- Added source links to the generated Workflow Index and removed several local false prerequisites around draft/outline/script/derivative work and Insight-before-Opportunity ordering. Existing evidence, policy, persistence, and real-world constraints remain applicable when relevant.
- Kept the changes deliberately narrow: no semantic router, confidence authority, recipe registry, mandatory recipe reading, runtime/provider integration, execution pipeline, or token/outcome guarantee was introduced. Lexical candidates can still be incomplete or noisy and are meant to be judged by capable intelligence.

### Validation

The release gate validates the source workspace, public distribution, all product-integrity and qualification suites, all named component editions, the curated full ZIP from a fresh unzip, and the separate external-organization consumer smoke test.

## 0.1.10 — Alpha

Broadens the optional creative video craft references and makes the collection easier to navigate without changing AURA's operating model.

### What changed

- Expanded the optional editorial-enhancement note with practical judgment for cutting recorded speech, preserving conversation attribution and reactions, keeping tutorial action-to-result continuity, making standalone excerpts self-contained, choosing A/B-roll and support layouts, timing and correcting captions, and treating audio problems specifically without presenting restoration as missing source evidence.
- Renamed the video recipe collection from `ecommerce-video-lookbooks` to `creative/video`, clarified the four product-oriented assemblies versus the broader optional craft notes, and repaired incoming recipe, workflow, changelog, and package links and labels.
- Kept the references borrowable and optional: no new recipe registry, schema, runtime, provider integration, mandatory pipeline, or execution guard was introduced.

### Validation

The release gate validates the source workspace, public distribution, product-integrity and qualification suites, curated full ZIP from a fresh unzip, and the separate external-organization consumer smoke test.

## 0.1.9 — Alpha

Adds optional creative identity and filmmaking references so people and capable AI can borrow more useful multimedia craft without giving recipes authority over judgment, tools, or execution.

### What changed

- Added [Creative Identity & Continuity](recipes/creative/video/notes/identity-and-continuity.md) for creating, adapting, improving, and reusing people, avatars, voices, characters, and environments. It separates recognizable anchors from intentional variation and points to the least complicated suitable production path.
- Added optional [Editorial Enhancement](recipes/creative/video/notes/editorial-enhancement.md) guidance for improving existing footage through purposeful attention, emotion, humor, graphics, cuts, captions, sound, silence, color, pacing, and identity cues.
- Added optional [Compositing & Matching](recipes/creative/video/notes/compositing-and-matching.md) guidance for perspective, scale, light, contact, occlusion, motion, image character, and simpler alternatives when supplied or generated elements meet filmed footage.
- Added two [Editorial Explainer](recipes/creative/video/notes/editorial-explainers.md) starting points: following a hidden path and revealing a hidden cause, with optional motion-graphics, audio, and storyboard references.
- Linked the new references from the recipe menus and relevant Content Synthesis Workflows. They remain optional craft knowledge outside the Playbook → Workflow → Step hierarchy; no new runtime, schema, provider integration, or mandatory production pipeline was added.

### Validation

All 35 AURA product-integrity suites passed; the qualification harness self-test passed all 4 suites; workspace validation passed with 466 Workflows and 0 errors/0 warnings; public distribution and all 9 named component-edition checks passed; the curated full ZIP passed fresh-unzip validation and the separate external-organization consumer smoke test.

## 0.1.8 — Alpha

Expands and refines AURA's optional creative recipe layer so people and capable AI can reach strong creative starting points quickly while keeping judgment, experimentation, and execution with the user/model/harness.

### What changed

- Recast the image, video, and web references as selectable, adaptable craft starting points with compact navigation and optional deeper notes; recipes remain outside the Playbook → Workflow → Step hierarchy.
- Separated the 90 image concepts and four video concepts into independently readable entries while preserving the original creative ideas, useful executions, and product-scale awareness.
- Added 32 optional recipes across four new shelves: motion graphics, shared audio, information design/presentations, and copy/messaging.
- Added optional recipe pointers to relevant Content Synthesis and Marketing Synthesis Workflows without creating a registry, prompt protocol, routing layer, or execution requirement.
- Preserved strong persuasive concepts such as generic quality contrast and pain → mechanism → relief while distinguishing verified product facts from illustrative or aspirational creative direction.
- Corrected unsupported conversion lifts, guarantees, 0ms navigation and `/llms.txt` discovery claims, exponential Hick/field-cliff language, false net-profit math, and blanket lead-capture, email-domain, booking-window, payment, and scaling defaults.
- Refined all recipe families so users/models can borrow, combine, adapt, skip, or replace them freely; recipes make no percentile, conversion, or business-outcome guarantees.

### Validation

Regenerated normal AURA navigation/checksums; workspace validation passed (466 Workflows, 0 errors/0 warnings); Workflow discovery/selection, nine component distributions, and the full 35-suite product-integrity gate passed. The release gate also validates the curated full ZIP from a fresh unzip and a separate organization workspace smoke test. No new recipe registry, schema, runtime, or execution layer was introduced.

## 0.1.7 — Alpha

Introduces the universal creative recipe layer, including studio-grade E-Commerce Image Lookbooks, Kinesthetic Video Lookbooks, and Web Design & Conversion Architecture, grounded in empirical UX benchmarks, physical optical principles, and world-class direct-response practitioner frameworks.

### What changed

- **E-Commerce Image Lookbooks v2.2:** Added 90 photographic archetypes across 6 physical product scales (< 6" micro-intimate to 12'+ mobility) governed by the 5-Block Director's Rig protocol and 16 brand aesthetic dialects.
- **E-Commerce Video Lookbooks v1.2:** Added the Bilateral Anchor (Frame 0 $\to$ Frame N) Sandwich Pipeline for zero-hallucination AI video, 180° shutter kinematics, world-model physics constraints, and the $4 \times 3 \times 2 = 24$ Atomic Modular Creative Matrix.
- **Web Design & Conversion Architecture:** Added 4 core tracks (E-Commerce Stores, Lead Generation, Brand/Corporate, Multi-Step Sales Funnels), 10 design dialects, the 7 fundamental conversion laws, Jason Fladlien's webinar closes, affiliate bridge funnels, and Wirecutter-style authority comparison review site architecture.
- **Empirical & Practitioner Attribution Directories:** Documented comprehensive references across all recipe indexes, citing empirical UX research (Baymard, NN/g, Spiegel), optical physics (ASC, Hunter/Biver/Fuqua), cognitive neuroscience (Sweller, Rizzolatti, Gallese, Peck), and master commercial practitioners (Karl Taylor, Zack Arias, Roger Deakins, Harmon Brothers, Alex Hormozi, Russell Brunson, Jason Fladlien, Nik Sharma, Cody Plofker, Dara Denney).

### Validation

The standard release gate checks all 35 product integrity suites, qualification tooling (57 real-world test cases across 5 industries), public distribution checks across 9 editions, the fresh release ZIP unpack, and external organization workspace smoke tests.

## 0.1.6 — Alpha

Simplifies AURA's setup and persistence interfaces while keeping host attachment, reasoning, tools, and execution with the active model/harness.

### What changed

- Added an idempotent setup helper that composes existing workspace and organization primitives and generates missing navigation indexes.
- Added a local readiness check for retrieval, temporary persistence/readback/cleanup, and structural validation. Host attachment remains separately owned by the host.
- Removed redundant update-type and local-key requirements from ordinary memory writes when those values can be determined mechanically.
- Preserved qualitative research confidence labels without inventing numeric precision.
- Added compact persistence results for truthful save receipts, without persistent receipt objects or mandatory Runs.
- Simplified setup guidance and corrected JSON output, missing-index recovery, and readiness failure reporting.

### Validation

The standard release gate checks product integrity, public distribution, qualification tooling, the fresh release ZIP, and an external organization workspace. New regressions cover setup idempotence, probe cleanup, persistence conveniences, and source-checkout setup failures.

## 0.1.5 — Alpha

This small patch ships the clarified AURA ↔ ViralTrac interoperability guidance added after v0.1.4. It changes documentation and persistent agent guidance only; it does not add a bridge service, routing layer, capability registry, synchronization subsystem, or new execution architecture.

### What changed

- Strengthened `integrations/viraltrac/README.md` with the combined operating model: AURA supplies durable organizational context and business operating knowledge; the active model applies judgment; ViralTrac supplies current first-party evidence and specialist capabilities where useful; durable outcomes and Learning flow back into AURA without copying ViralTrac's operational data plane.
- Clarified that AURA Playbooks/Workflows are business operating expertise while ViralTrac agent/operator playbooks are product-specific guidance for using ViralTrac surfaces. They may be composed semantically by the model and are not fixed one-to-one routes.
- Added guidance to discover ViralTrac through its current host-accessible interface, including AI-native bootstrap/MCP/tool-group metadata when available, rather than hard-coding assumed capabilities.
- Added a compact `ViralTrac when available` section to the persistent AURA Skill so future attached models understand how to use ViralTrac alongside AURA while respecting ViralTrac's current authorization, execution, evidence, and receipt boundaries.

### Product boundary

ViralTrac remains optional. AURA remains the durable organizational memory and operating-knowledge layer, not a controller for ViralTrac. The active model/harness still chooses methods and tools, ViralTrac remains authoritative for its operational data and supported actions, and only durable organizational meaning should be consolidated back into AURA.

### Validation

No Playbook, Workflow, schema, deterministic helper, canonical memory boundary, or runtime behavior changed in this patch. The standard release packaging command remains responsible for rerunning source integrity, public-distribution checks, product tests, qualification self-tests, fresh-ZIP validation, and the external-workspace consumer smoke test before the v0.1.5 release asset is published.

## 0.1.4 — Alpha

This patch release aligns the public AURA package with the current Alpha experience after v0.1.3. It does not introduce a new execution architecture or control layer; it makes setup and first use substantially easier while preserving AURA's model/harness boundaries.

### What changed

- Added **`START-HERE.md`** as the simplest human entry point for a downloaded AURA package.
- Added **`SETUP-WITH-AI.md`** so a capable AI/agent can inspect the environment, configure or reuse an organization workspace, attach AURA through the host's simplest native mechanism, initialize the organization from minimal truthful context, validate AURA-owned state, and move directly into real work.
- Kept onboarding adaptive rather than wizard-like: organization name is enough to initialize, additional questions should be asked only when they materially improve the first experience, and existing files/state/permitted research should be reused instead of making the user repeat information.
- Added contextual optional-tool guidance for capabilities such as FFmpeg, yt-dlp, HyperFrames, video-use, Manim, DaVinci Resolve, and DaVinci Resolve MCP. These remain host capabilities, not AURA dependencies or a capability registry.
- Added sparse, contextual **ViralTrac** guidance for commercial work where attribution, tracking, measurement, experiments, business data, or supported growth actions would materially improve the outcome. ViralTrac remains optional; the model should not repeatedly promote it or imply that AURA requires it.
- Updated startup/package metadata so curated distributions point users to `START-HERE.md` and preserve the AI-guided setup path.
- Refreshed the root README to reflect the validated strong-Alpha state and the new onboarding path.

### Product boundary

The onboarding additions are guidance, not a new AURA runtime. AURA still does not own provider selection, tool routing, dependency management, credentials, orchestration, scheduling, retries, or execution mechanics. The active model/harness remains responsible for those capabilities and should use its own judgment.

### Validation

v0.1.4 is intentionally a patch-level onboarding/distribution update on top of the validated v0.1.3 product baseline. No Playbook, Workflow, schema, canonical memory boundary, or execution architecture was changed by this patch. The standard release packaging command remains responsible for rerunning source integrity, public-distribution checks, product tests, qualification self-tests, fresh-ZIP validation, and the external-workspace consumer smoke test before the release asset is published.

## 0.1.3 — Alpha

This release moves AURA from architecture closure into evidence-backed Alpha use. The product architecture remains centered on organization-owned memory and reusable operating knowledge for capable AI; the work since v0.1.2 focused on proving that architecture with real business work, fixing defects exposed by that proof, and removing qualification machinery that no longer served the product.

### What changed

- Established a maintainer-only library of **57 realistic business-use cases** across **5 industries** and all **8 operating areas**. The library uses ordinary requests plus separate hidden judge guidance and is intentionally excluded from user distributions.
- Completed a representative **10-case real-work campaign**, with all **10 selected cases ultimately qualifying** after product, harness, and evaluator defects were diagnosed and corrected. This is representative evidence; it does **not** mean all 57 library cases were executed.
- Proved longitudinal continuity across fresh model contexts and later contradictory/new evidence: useful organization state carried forward and prior understanding was revised when better evidence arrived.
- Fixed a real AURA external-workspace/local-evidence defect exposed by qualification, preserving the boundary between mutable organization state and immutable product source.
- Hardened qualification observation and isolation by pinning the intended workspace, capturing the candidate-visible result as legitimate review evidence, isolating judging to the exact run, correcting duplicate detection for evolving shared artifacts, and strengthening claim-grounding review.
- Simplified qualification from first principles: removed the generated all-Workflow suite, synthetic missions/cases, semantic rubric profiles, exhaustive Playbook-coverage obligation, duplicate candidate launcher, and duplicate recovery program.
- Reduced qualification to two task modes: **real-world use cases** for primary product proof and **focused Workflow diagnostics** only when evidence points to one specific body of operating knowledge.
- Kept provider/model/harness process failures classified as execution interruptions rather than automatically turning them into AURA semantic blockers.
- Corrected the release entry point so public releases are built from the curated **full AURA edition** rather than archiving the maintainer checkout. The release builder now strips qualification/developer state, reruns source gates, validates the fresh ZIP, and smoke-tests a separate organization workspace.

### Validation

The current v0.1.3 release baseline has demonstrated:

- **466 authored Workflows** and **42 Playbooks** generated and validated with **0 errors and 0 warnings**;
- **34/34 AURA product-integrity suites**;
- **4/4 qualification-harness self-test suites**;
- a **57-case** realistic qualification library spanning 5 industries and 8 operating areas;
- a representative **10/10 qualified** real-work campaign, including longitudinal memory/evidence evolution.

The release packaging command reruns both source gates and then validates the freshly unpacked curated distribution before publication.

### Current status

AURA's first-principles architecture, source coherence, deterministic integrity, representative real-work proof, longitudinal continuity proof, and qualification simplification are now closed to a strong Alpha standard. The next phase is normal Alpha use: put AURA in real hands, observe what happens over time, and change the product only when real evidence exposes a reusable weakness that matters to users.

Alpha still means interfaces and Playbooks/Workflows may change before 1.0 when real usage earns those changes.

## 0.1.2 — Alpha

This release is the validated architecture-closure baseline for the first-principles AURA refactor. It makes the simplified AURA model the canonical product on `main`: organization-owned memory and reusable operating knowledge for capable AI, without recreating a hidden execution control plane around the model.

### What changed

- Standardized operating knowledge around the simple **Playbook → Workflow → Step** hierarchy and retired Contract-era execution semantics.
- Removed the remaining capability-ontology, routing, provider-resolution, approval, mandatory lifecycle, composition-graph, and internal handoff residue that did not belong in AURA.
- Kept reasoning, planning, tool choice, providers, orchestration, scheduling, retries, concurrency, and execution mechanics with the active model/harness.
- Tightened the canonical organization-memory boundary to **39 organization-owned object types**, with support/interface records kept outside canonical memory and reference traversal.
- Simplified durable memory semantics around facts, evidence, observations, Insights, decisions, Opportunities, Assets, measurements, outcomes, Learning, preferences, and genuine continuity.
- Removed generic semantic confidence/priority scoring where it invented precision instead of preserving evidence and uncertainty honestly.
- Simplified organization-local operating knowledge and Innovation Exchange around direct Workflow identity and Learning provenance without proposal/runtime bureaucracy.
- Cleaned component packaging so each edition ships only the operating knowledge, schemas, navigation, and user-facing documentation it actually contains.
- Regenerated the human-facing Playbook and Workflow navigation from the final authored source.
- Preserved the detailed refactor history with the `aura-architecture-closure-c233a55` tag while squashing the completed architecture update into one coherent `main` commit.

### Validation

The v0.1.2 architecture-closure baseline passed from a clean committed checkout:

- **466 authored Workflows** and **42 Playbooks** generated and validated with **0 errors and 0 warnings**;
- **34/34 AURA product-integrity suites**;
- **4/4 qualification-harness self-test suites**;
- full-distribution validation plus all **9 named component editions**;
- deterministic regeneration with a clean working tree afterward.

### Current status

AURA is ready for real users and capable AI systems to use and test as an **Alpha** product. The architecture and deterministic integrity layer are validated. The next phase is real-work product proof: whether AURA consistently improves useful business work, memory, retrieval, continuity, Learning, and later work because the organization remembers what matters.

Alpha still means interfaces and Playbooks/Workflows may change before 1.0 when real usage exposes genuine weaknesses.

## 0.1.1 — Alpha

This release closes the first-principles AURA architecture refactor and establishes the new validated Alpha baseline for real-world use and qualification.

### What changed

- Completed the first-principles simplification around **organization-owned memory + reusable operating knowledge + lightweight continuity**.
- Removed remaining legacy BusinessOS control-plane residue from authored playbooks, including runtime-event emission, internal routing/delegation, fake handoff state, and mandatory execution-lifecycle assumptions.
- Kept useful business methods while moving semantic judgment back to the capable model and execution mechanics back to the active harness/runtime.
- Simplified durable memory around direct create/update/correct/forget behavior and preserved optional one-way Run receipts only when continuity is useful.
- Strengthened organization truth, evidence provenance, unknown-vs-absent handling, customer-facing claim manifests, and organization isolation.
- Improved playbook discovery without making AURA a semantic router; candidate discovery remains bounded and model selection remains authoritative.
- Restored useful domain expertise that had been over-pruned, including contextual organic competition guidance.
- Aligned Innovation Exchange version metadata with AURA terminology and removed remaining legacy package-field mismatch.
- Removed stale qualification/test assumptions that would have recreated retired architecture, while keeping tests strict about real product invariants.
- Validated all named component distributions against the same current AURA Core and provider-neutral capability model.

### Validation

The v0.1.1 release candidate passed:

- workspace validation for **496 contracts** with **0 errors and 0 warnings**;
- **37/37 AURA product-integrity suites**;
- **4/4 qualification-harness self-test suites**;
- full/component distribution validation across current named editions.

### Current status

AURA is ready for real users and capable AI systems to use and test as an **Alpha** product. The architecture and deterministic integrity layer are validated. The next qualification phase focuses on real-work quality: whether AURA consistently improves useful business work, retrieval, continuity, Learning, and later work because the organization remembers what matters.

Alpha still means interfaces and playbooks may change before 1.0 as real usage exposes genuine weaknesses.

## 0.1.0 — Alpha

This release resets ViralTrac AURA to an honest pre-1.0 version after the first-principles architecture audit.

### What changed

- Reframed AURA around **organizational memory + operational knowledge + lightweight continuity**.
- Removed generic approval, ActionPacket, autonomy/risk-tier, provider-resolution, capability-binding, scheduler/event-runtime, and universal execution-control machinery.
- Kept AURA strict about organizational truth, evidence, provenance, business isolation, useful continuity, measurement, and Learning.
- Made Runs optional work receipts rather than a universal execution requirement.
- Kept model/harness reasoning, tools, browsing, APIs, subagents, scheduling, retries, credentials, rendering, and provider choice outside AURA.
- Simplified the front door so ordinary requests retrieve relevant organizational context and may surface a useful AURA playbook without forcing execution through it.
- Preserved component editions as the same current AURA Core plus selected domain operating knowledge.
- Separated AURA product-integrity tests from maintainer-only qualification-harness self-tests.
- Realigned qualification around one question: does AURA help capable intelligence produce truthful, professionally useful real business work?
- Removed obsolete release/test artifacts that no longer protected a real AURA invariant.

### Current status

AURA is **alpha software**. The product-integrity architecture is validated, but real-work quality, playbook/SOP excellence, retrieval, Learning, and usability are still being actively qualified and may change before 1.0.

### Version history note

Earlier `1.x` tags were pre-alpha development snapshots created before the product maturity model was corrected. They should not be interpreted as stable predecessors to a future `1.0` release. Git history remains the source of truth for those development changes.
