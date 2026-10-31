# Share selected work between AURA workspaces

Use **Settings → Share or import**, or **Share a copy** inside a saved record or file.

Choose information, files, or a project folder. Search and filters help narrow the list;
selected items remain selected while searching. Business information is grouped by
purpose in a few collapsible groups, each with a short description and total count;
files and folders can be narrowed by file type. Groups start closed, render their first
20 items when opened, and offer Show more within that group. Search opens matching
groups and checks beyond the currently displayed rows, using the same loaded saved-record
search as Business & memory. It searches names, saved information and locations, not
the contents of arbitrary documents or media files. **Selected** shows just the
chosen items, and a saved-file entry represents its underlying file once.
Choosing **Start a new selection**, **New selection**, or **Clear selection** resets
the item list and filters. **All** leaves Selected only so you can add more items.
Choose a saved selection, then **Edit saved selection** to change its name or notes;
**Change selected items** returns to the item picker. **Save changes** updates the same
selection without starting a transfer; **Save & review** saves it and prepares a fresh
package. A rename does not create a duplicate, and a
new selection cannot silently replace an existing selection with the same name.
**Current workspace → Copy folder location** appears only on Share selected items
and copies this workspace’s path without a separate Settings menu entry. Import a
package and Import history do not repeat that utility. The panel uses one scroll surface and keeps its heading
and action controls available while scrolling. Continue, choose a destination, review,
then add the work or export the ZIP. Nothing is uploaded and originals stay in place.
Ordinary project folders are shareable. Private settings, caches, credentials and
folder links are intentionally excluded and listed separately from unavailable
locations. AURA's internal `.sharing` folder is expected and does not need attention.

## Find and inspect a package

For reusable public methods/designs/starters, **Explore community setups** opens the
[Innovation Exchange](https://viraltrac.com/aura/community/). **Create a package →
Prepare for community sharing** prepares a clean public-format selection locally;
it never uploads automatically. See [the exchange guide](../INNOVATION-EXCHANGE.md)
for contribution review, source notices, rights and publication.

**Import a package** lists sharing ZIPs found in recent package locations, this
business's files, its linked folders, and Downloads. Exports and successfully opened
packages remember their location; the archive is not duplicated. Discovery is bounded,
reads package metadata only, and never imports anything automatically. **Find in folder**
searches another chosen folder. Search filters every discovered result, including
rows beyond **Show more**. **Choose file** and **Enter a package location** remain available.

**View package** verifies the ZIP and displays its actual contents and setup notes
before asking for a destination. Back returns to the package list and preserves the
search. Changing the destination from the final review retains the form's values.
Missing recent files can be selected again at their new location. Ordinary ZIPs,
workspace backups, and unreadable packages are not offered as sharing packages.

Use the checkboxes in that preview to choose what to bring across. Required supporting
items and source notices follow the selected content. Clearing every item disables
the destination action. Both existing selected-share ZIPs and exported workflow
InnovationPackages are supported by discovery and import; workflow packages become
readable, attributed source/method files, not active canonical business knowledge.

A **saved selection** is an editable list of source items, not an archive. A ZIP is
a fixed snapshot: edit the saved selection and export a new ZIP to share changes.

## Destinations

- **An existing workspace:** choose a known workspace or browse to its folder, then
  choose the business receiving the copy. This also supports separate businesses in
  the same workspace folder.
- **A new workspace:** provide the new business/project name and a new or empty
  folder. AURA creates an independent identity; other local details remain unknown.
- **An export file:** choose a folder and a new ZIP filename. The recipient uses
  **Import a package**, then chooses this workspace, another workspace, or a new one.

For upgrades, keep using the same workspace through **Startup & updates**. For a
complete recoverable copy, use **Back up or restore**. For combining scattered folders,
use **Bring existing work together**. Sharing does not replace those operations.

## What travels

Selected business records arrive as attributed source material. They do not overwrite
the receiving business's identity or silently become its established facts, completed
work, or measured results. Files receive ordinary local Asset registrations so they
appear in **Saved files & media**. The original evidence is retained separately from
editable local copies; adapting a local file does not rewrite its source evidence.

Referenced canonical records and files belonging to selected Assets are included as
supporting material, labeled in the review. Read that preview: a selected record can
refer to other business information you may not intend to disclose. Narrow the
selection before sharing if needed. Known credential paths/fields, app configuration,
native chats and schedules are excluded. This is not an automatic content-redaction
service; review your selected business documents before giving them to someone else.

Choose a project folder to keep its internal directory structure and relative file
links together. Arbitrary absolute paths, external services, optional tools and links
outside the selection are not automatically made portable. Missing, unreadable or
excluded linked material appears in the review. Packages are currently bounded to
10,000 items and 2 GB of uncompressed content.

**Create package** opens a naming and setup-notes form with the selected item names
below the notes. **Save selection for reuse** sits beside **Review package** and is
optional. Review package prepares a snapshot and continues to export by default;
another workspace remains available as a destination. Contents, including supporting
material, appear below the destination controls and in the final review. Long lists
show 20 items at a time with **Show more**, using the panel's normal scrolling.
For a franchise starter, explain
what is ready to use, what needs local details, and which guidance permits local adaptation. These
are ordinary authored notes, not a new policy engine or template language. Recipients
can read them in **Import history → View work** and prepare a request for their AI.
That action preserves an unsent draft and does not send automatically. Imported
instructions remain source material, not permission to execute commands or change accounts.

## Reuse, updates and disagreements

**Save selection for reuse** remembers the selected items and notes. A fresh
sharing review reads their current contents. An exported package remains an exact
snapshot. To share changes, select the saved selection and send a fresh copy, or
import a newer ZIP. There is no automatic background synchronization.

AURA matches origin and original item identity, rather than names:

- **Already added:** the same source version exists; no duplicate is created.
- **Source has an update:** an incoming version changed and the local copy is untouched.
  Explicitly select **Include source updates** to replace those untouched copies.
- **Changed here:** the local copy differs, while the source version is unchanged.
  AURA keeps local work.
- **Changed in both places:** AURA keeps local work and saves the incoming alternative
  for comparison. Open the import's **View work** to inspect either version or ask the AI
  to compare them. A timestamp does not decide which meaning is correct.

Copies remain independent. A change in one workspace never silently edits another.

## Undo and interrupted work

**Import history → Review undo** checks the actual files and saved references. Untouched
additions can be removed and untouched replaced copies can be restored. Locally edited,
subsequently updated, or referenced work is kept for review. Undo does not delete a
newly created workspace's business identity or unrelated work.

Transfers recheck source and destination hashes before applying, verify copied bytes,
use atomic file replacement and a local OS writer lock, and roll back handled errors.
A process interruption leaves an import receipt: use **Import history → Review undo**
to recover untouched partial work, then retry from a fresh review. The OS releases
the writer lock when the process exits; no lock service or scheduler is added.

## CLI and custom interfaces

`scripts/workspace_sharing.py` supplies the same operations used by the visual view:

```sh
python scripts/workspace_sharing.py list /path/to/source business-id
python scripts/workspace_sharing.py prepare /path/to/source business-id --select record:OBJECT_ID --name "Location starter" --note "Add local hours and address."
python scripts/workspace_sharing.py save-selection /path/to/source business-id --select record:OBJECT_ID --name "Location starter"
python scripts/workspace_sharing.py export REVIEW_ID /path/to/Location-starter.zip
python scripts/workspace_sharing.py import /path/to/Location-starter.zip
python scripts/workspace_exchange.py prepare /path/to/source business-id --select file:KEY_FROM_LIST --name "Reusable starter" --kind starter --description "A useful blank starting point" --author "Public pseudonym"
python scripts/workspace_sharing.py select REVIEW_ID --select file:ITEM_FROM_PACKAGE
python scripts/workspace_sharing.py review REVIEW_ID /path/to/recipient --business recipient-id
python scripts/workspace_sharing.py review REVIEW_ID /path/to/new-location --new-name "New location"
python scripts/workspace_sharing.py apply REVIEW_ID
python scripts/workspace_sharing.py apply REVIEW_ID --include-updates
python scripts/workspace_sharing.py history /path/to/recipient recipient-id
python scripts/workspace_sharing.py discover /path/to/workspace business-id
python scripts/workspace_sharing.py discover /path/to/workspace business-id --folder /path/to/packages
python scripts/workspace_sharing.py save-selection /path/to/workspace business-id --id SELECTION_ID --name "Updated starter" --select record:ASSET_ID --note "Local setup guidance"
python scripts/workspace_sharing.py detail /path/to/recipient recipient-id RECEIPT_ID
python scripts/workspace_sharing.py undo /path/to/recipient recipient-id RECEIPT_ID
python scripts/workspace_sharing.py undo /path/to/recipient recipient-id RECEIPT_ID --apply
```

Use `--select` repeatedly with exact keys returned by `list`. `history` returns saved
selections; `prepare` creates a new snapshot. An optional global `--store` selects a local
review store. CLI functions use explicit workspace arguments and do not switch the
active workspace. Filesystem/shared-storage access remains controlled by the host;
workspace structure is not a multi-user access-control system.

Custom views can use the existing token-protected local JSON API. `GET /api/sharing?business=ID`
returns selectable items, saved selections, known destinations, and recent imports.
`POST /api/sharing/{prepare,prepare-public,selection,package,select,discover,destination,review,apply,export,detail,undo,file-key}`
uses the same helpers. Every mutation includes `business`, the launch token, and the
current `X-Aura-Workspace` header. Prepare/package reviews are scoped to that business
and workspace. `prepare` takes `keys`, `name`, `note`; `selection` takes the same fields
and an optional `selection_id` to update the existing selection. Omitting the ID creates
a new selection. `discover` accepts an optional folder `path`; `package` takes the ZIP `path`;
`prepare-public` adds `kind` (`starter|workflow|layout`), optional `description`, `author`
and `based_on` to ordinary preparation fields and uses `workspace_exchange.prepare`.
`select` takes an imported package `id` and nonempty `keys`, returning a separate
verified subset review with required supporting items. CLI import uses the same
`workspace_exchange.import_package` adapter for both package families.
`review` takes `id`, destination `path`, `target_business` or `new_name`; `apply` takes
`id` and optional `include_updates`; `export` takes `id` and output `path`;
`detail`/`undo` take `receipt`, with `apply: true` for confirmed undo. `destination`
previews a workspace's businesses from `path`. `file-key` resolves an existing file-view
`ref` to its selectable sharing key. UI styling and layout are replaceable; package
semantics do not depend on the bundled interface.
Custom frontends should call these helpers or API operations rather than reimplement
validation, file handling or selection persistence. CSS can change freely; changes to
the bundled markup must retain its control IDs/data attributes or bind replacement
controls to the same operations.

Workspace-owned transfer history, source snapshots, and undo data live under
`attachments/<business>/.sharing/` and `attachments/<business>/shared/`, so the existing
full-workspace backup carries recovery information. Temporary preparation/review data
stays in the local AURA state folder. No cloud service or new runtime dependency is needed.
