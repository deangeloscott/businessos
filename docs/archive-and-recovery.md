# Archive and recovery

Use **Archived & deleted** at the bottom of workspace search to find and restore work. Filter by Archived, Deleted or Recovery copies, or search by name. The ordinary workspace lists and automatic context discovery exclude archived items.

| Item | What happens | Restore |
| --- | --- | --- |
| Chat | Leaves current navigation and search; saved native identity stays | Unarchives the same chat |
| Project | Leaves current navigation; files and native work stay in place | Restores the same project identity |
| Agent | Hides the saved profile; native definitions, chats and schedules remain | Restores instructions, native links and task links |
| Saved memory, file, collection or local workflow record | Stores archive metadata on its canonical record; no files move | Removes the archive marker; preserves meaning, identity and links |
| Deleted goal | Leaves current work; retains its status before deletion | Returns as active, paused or completed as it was |
| Record removed with `forget.py` | Removes an unreferenced canonical record after preserving a local recovery copy | Reinstates its original ID and data if its references remain valid |
| Missing workspace file with a saved version | Lists its latest retained copy without assuming why it disappeared | Restores that copy without overwriting a current file |
| Explicitly retired originals from workspace organization | Keeps the selected originals in Aura Recovery | Returns the originals if their original location is still empty |

**Archive does not pause a native schedule, cancel work or restart it on restore.** Manage native work through its task or chat controls. Existing chats and explicitly selected references can still use archived context; archive is not an access restriction. Native-owned tools, plugins, sign-ins, native histories and bundled guidance remain managed by their owner.

Archived records, profiles and projects travel with the workspace and do not expire automatically. Chat archive state remains in Aura's machine-local chat store. File history is also machine-local and bounded to 20 versions per file, 500 entries and 256 MB per business/workspace, with a 32 MB per-file limit. Deleted record recovery shares those bounds: it is not indefinite trash or an OS recycle-bin stage. Later history can evict old copies. Explicitly retired originals follow the retention selected in Aura Recovery; automatic removal there is permanent. Keep normal backups for durable recovery.

The Business identity cannot be archived or forgotten. Goals retain their own lifecycle. Restoring a deleted record validates organization ownership, ID uniqueness and references; it does not overwrite a newer record. Restore missing related records first when necessary. Nothing automatically resumes execution.

## API and CLI

All mutations use `POST /api/archive` with the normal local authentication and selected workspace:

```json
{"business":"my-business","kind":"record","id":"src_example","action":"archive"}
```

Use `action: "restore"` to undo it. Kinds are `chat`, `project`, `goal`, `agent`, `record`, `file`, `collection`, `deleted-file`, `file-version` and `recovery`. Archive file accepts a saved Asset ID or a file reference already accessible in the selected business; it registers a reference when needed and leaves bytes untouched. Collection accepts its stable collection ID or Asset ID. Goals, deleted-file, file-version and recovery only support restore here. Delete goals through their goal controls.

```text
python scripts/workspace_archive.py list --workspace <folder> --business-id <id> --json
python scripts/workspace_archive.py archive --workspace <folder> --business-id <id> --kind agent --id=<agent-id>
python scripts/workspace_archive.py restore --workspace <folder> --business-id <id> --kind record --id=<record-id>
```

These commands use the running local Aura service (`--url` selects another local address). Existing chat, goal, project and agent endpoints remain compatible. Direct `workspace_assistants.py archive/restore` also works offline on the same portable profile state. Product and native files are never deleted by an archive action.
