# Projects and saved results

Projects connect chats, useful files, goals, guidance and native scheduled work. A project can have a folder, but a folder is not its identity. Project IDs survive renaming; workspace-relative folders survive moving the workspace. Linking work never copies its contents into every chat or changes native permissions.

In a project's menu, **Project work** shows its linked work, saved results and discovered files. **Files & media** has a project filter and **New collection**. Collections keep a current list; dated reports preserve separate installments. Ordinary documents and media keep their existing file/version behavior. Working without a project or an end goal remains supported.

Projects are ordinary portable workspace data in `.businessos/projects.json`. Older project settings migrate on a deliberate write. Workspace backups include the manifest. Removing a project archives its relationships and ungroups its chats, retaining files, collections and native tasks. Restore it in Search → Archive & recovery. External folders and native schedulers remain owned by their original app/device; reconnect their locations after moving to another computer.

## Producing useful work

Aura chat processes receive a scoped producer reference. When a native app deliberately creates an Asset through `remember.py`, the existing helper records known project, chat and goal associations. Later edits preserve the saved associations and respect explicit changes or removals. Existing explicit associations win; project membership remains separate from automatic model context. A raw tool file-change event is not proof of a finished deliverable, so Aura does not promote every temporary file into memory.

For repeated research, choose a maintained collection when the user needs current entries. Choose dated reports when each installment is a historical deliverable. Keep native documents, spreadsheets, databases and media in their useful formats; an Asset or project reference can point to them. The local collection helper is optional and requires no running UI, cloud, database service or additional model.

The model determines relevance, source identity, semantic duplication, materiality and what deserves saving. Stable item IDs identify the same grant, job, story or finding across runs. Syndicated copies are not independent corroboration merely because their URLs differ. A hash or newer publication time does not establish a material change or factual correctness.

## Shared CLI and API

Commands accept `--workspace /path/to/workspace` and `--business-id BUSINESS_ID`. Mutations accept JSON using `--input -` on standard input, or a JSON string as `--input`. Paths below are relative to the Aura product folder. Use the workspace's available Python interpreter.

```sh
python scripts/workspace_projects.py list --workspace /path/to/workspace --business-id example-studio
python scripts/workspace_projects.py create --workspace /path/to/workspace --business-id example-studio --input '{"name":"Funding","folder":"work/funding"}'
python scripts/workspace_projects.py show --workspace /path/to/workspace --business-id example-studio --id PROJECT_ID
python scripts/workspace_collections.py create --workspace /path/to/workspace --business-id example-studio --input '{"key":"funding-shortlist","name":"Funding shortlist","purpose":"Find eligible grants and track deadlines","project_refs":["PROJECT_ID"],"source_refs":["agency-a","agency-b"]}'
python scripts/workspace_collections.py show --workspace /path/to/workspace --business-id example-studio --id COLLECTION_ID --search design --limit 5
python scripts/workspace_collections.py show --workspace /path/to/workspace --business-id example-studio --id COLLECTION_ID --item ITEM_ID
```

Use `configure` with the current `revision` to change a collection’s name, purpose, expected `source_refs`, or `project_refs`. The UI’s **Edit collection** changes its name and purpose. A run cannot silently shrink the configured source coverage; adjust the collection deliberately when its scope changes.

The create result returns a stable collection ID and current revision. Repeating the same create key reuses its existing collection. Before writing, read the latest revision. An apply payload looks like:

```json
{
  "revision": "REVISION_FROM_SHOW",
  "run_id": "ACTUAL_NATIVE_RUN_ID",
  "status": "complete",
  "coverage": {"expected": ["agency-a", "agency-b"], "checked": ["agency-a"], "failed": ["agency-b"]},
  "items": [{
    "id": "agency-a:grant-123",
    "title": "Example design grant",
    "summary": "A producer-authored finding, with evidence and eligibility limits.",
    "fields": {"amount": 5000, "eligibility": "Confirmed source criteria"},
    "source_refs": [{"reference":"https://example.test/grant-123", "published_at":"2026-11-01T10:00:00Z", "data_as_of":"2026-10-01T00:00:00Z", "last_checked_at":"2026-11-07T10:00:00Z"}],
    "expires_at": "2026-12-01T23:59:00Z",
    "review_after": "2026-11-14T10:00:00Z",
    "change_reason": "New eligible opportunity"
  }]
}
```

Send it to `workspace_collections.py apply --id COLLECTION_ID --input -` with the same workspace/business flags. Despite the producer's requested complete status, this example is recorded as partial because one expected source failed. Coverage is producer-reported, not an independent verifier of factual truth. For work without a predefined source list, supply a concise `coverage.scope` and the actual checked sources. Failed/unknown coverage never becomes a successful no-change receipt. Absence from a partial scan does not close or delete an existing entry.

Retry the identical payload with the same native run ID. Aura returns its receipt without applying it twice. Reusing that run ID for different data fails clearly. Revisions prevent two producers from overwriting one another: reread and reconcile after a conflict. If a runtime does not expose a run ID, establish and retain one identity for that run before writing; do not generate a different identity for each retry. Old receipts are bounded to 500; an older unrecognized retry still needs the current revision.

Only changed meaning creates a change entry. A new `last_checked_at` alone does not reopen a dismissed result. `material_change: false` can record a producer-judged nonmaterial edit without resurfacing it. Set explicit `state: "closed"` or `"superseded"` only with a basis; `supersedes: "ITEM_ID"` links a replacement to its predecessor. Optional `order: ["ITEM_ID", "..."]` sets a curated order without inventing a universal priority score. Dated report series reject replacement of an existing installment unless `amend: true` and a change reason explicitly identify a correction.

## Feedback, time and history

The result view offers Save, Mark seen, Dismiss, Snooze until tomorrow, and Correct. Seen suppresses unchanged entries from **Changes to review**, while retaining them in the current list. Dismiss hides the unchanged entry from the current list. A material change can surface it again with an explanation. Snoozing hides the entry until its chosen time; it does not create a separate notification or scheduled job. **Handled** and **All** retain access. These controls do not silently delete original evidence.

Corrections preserve the reported source value and the user's explanation. Later producer updates retain corrected fields and can flag a new source disagreement for review. A correction to one field does not hide changes to unrelated fields. UI and CLI/API use the same revision checks and persistence operations. `feedback` accepts `item_id`, `revision`, and `action: "save" | "acknowledge" | "dismiss" | "restore" | "snooze" | "correct" | "clear-correction"`; snooze uses `until`, and correct uses `correction` plus `note`.

Report time, publication time, the period described by the data, and actual last verification remain distinct. Explicit expiry makes an entry expired in current views; a review date marks it for reassessment, not automatically false. Native producers should verify relevant time-sensitive claims before important use and choose check cadence based on purpose. A routine recheck belongs in coverage/history; only a genuine recurrence or material change warrants reopening a handled AttentionItem.

Each collection is one JSON file under `attachments/BUSINESS_ID/collections/`, referenced by one canonical Asset. Rows do not each become separate permanent business records. Existing bounded local history preserves earlier file versions. Collection check history keeps 50 checks, change receipts keep up to 250 changes, and the UI loads rows in pages with full details and check history on demand (`show --history` for the CLI). The helper permits updates of up to 2,000 rows and a 32 MB collection file. Keep larger datasets in their native tool or split them by purpose; these limits do not constrain native execution. Backups preserve the actual file; local recovery/cache retention is separate. No useful original is automatically purged.

## Scheduled work

Open a scheduled task and choose **Save results to → Apply to scheduled task**. Aura writes the chosen collection instructions through the existing native scheduling path, then reads back the task to confirm them before saving its association. The scheduler continues to own execution, cadence, model, delivery and retries. A confirmed task definition does not prove its scheduler is running. User-selected native delivery remains unchanged. A task without a collection retains its ordinary native results. Tasks created from a saved agent also carry that agent’s selected context references; collections remain retrieval pointers rather than full dataset copies.

Use native run identities and write the collection from the scheduled producer itself. Aura does not require its UI to stay open, invent unattended timers, or claim that selecting a destination alone wires the native task. Native-only activity and arbitrary files written outside these helpers remain discoverable through normal folders/native results; their semantic associations and check coverage are not fabricated. If a native app expires a useful output, save the needed artifact or evidence snapshot deliberately before relying on a temporary reference.

Authenticated API routes:

- `GET /api/projects` lists projects; existing `POST /api/projects` creates/edits/archives them.
- `GET /api/project-resources?business=…&id=…` lists linked work. POST accepts `action: link | unlink | restore`, a project `id`, and a scoped `reference` when linking.
- `GET /api/collections?business=…` lists saved collections; `project=PROJECT_ID` narrows it. Add `id`, `q`, `view`, `offset`, `limit`, `history=1`, or `item` to retrieve a bounded view or one complete result.
- `POST /api/collections` accepts `action: create | configure | apply | feedback`; feedback uses `choice` for the result action. The fields match the CLI payloads above.
- `GET /api/project-binding?business=…&kind=task&id=…` reads a known producer relationship. Selecting a relationship is metadata, not proof of native scheduling.

Custom interfaces use these shared operations. Context references to collections are small retrieval pointers, never automatic injection of the entire dataset. Search explicitly covers saved collection text/fields; linked document bodies and unavailable native-only content are not silently treated as searched.
