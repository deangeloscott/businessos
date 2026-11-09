# What makes up AURA

AURA consists of a local browser interface, a Python application/API, CLI helpers, file-backed organizational memory, and reusable operating knowledge. The UI and CLI call the same persistence and file-editing functions. Connected AI apps own model execution and their native tools; AURA does not replace them.

## Included runtime

| Component | Role | License |
| --- | --- | --- |
| AURA Python and browser code | Workspace resolution, memory, file access, sharing, conversations and views | AURA source-available license |
| Python standard library | Local HTTP server, file IO, streaming, CSV, processes | Python license |
| PyYAML | YAML configuration and front matter | MIT |
| jsonschema and its runtime dependencies | Canonical record validation | See installed package licenses |
| CodeMirror | Text and Markdown editing | MIT |
| Tabulator | CSV/TSV cell editing | MIT |
| Cropper.js | Raster image crop, rotation and resize | MIT |
| PDF.js, its fonts, character maps and WebAssembly helpers | Local PDF viewing and text search | Apache-2.0 and included resource notices |
| Leaflet | Map view of saved results with places | BSD-2-Clause |
| Browser media controls | Images, audio and video playback | Supplied by the browser |

Exact frontend versions, transitive package identities, registry integrity values and shipped file hashes live in `distribution/ui-components.json`. Included license texts are in `interface/vendor/THIRD-PARTY-NOTICES.md` and PDF resource notices. Python requirements live in `requirements.txt`; installed versions depend on the selected Python environment. Click the version in Settings for the component overview.

## Optional tools stay separate

LibreOffice is an optional installed app for richer documents, spreadsheets and presentations. FFmpeg and other tools listed in [tools and services](tools-and-services.md) remain optional native tools. AI harnesses, models, account credentials and Google editors are not bundled. Listing a tool is not evidence that it is installed, connected, or working for a particular job. Library discovery marks LibreOffice installed only when its executable is found.

The map view is the one included part that uses an internet service: map imagery from OpenStreetMap's tile servers, and, only after you choose **Find them on the map**, address lookups through OpenStreetMap's Nominatim. AURA keeps viewed imagery and looked-up places on this computer and follows both services' usage policies (identified requests, about one lookup a second, no bulk downloads). See [projects and results](projects-and-results.md#seeing-results-as-a-map-chart-or-board).

## Files and editors

`scripts/workspace_documents.py` owns file inspection, conflict checks, atomic replacement, and Asset version/copy tracking. `scripts/workspace_ui.py` applies the selected workspace/business boundary and exposes authenticated document APIs and streamed media. `interface/file-editor.js` is a lazy-loaded view over those operations; changing the view does not replace saving logic. Existing custom interfaces can call the same API. No new file database or document service is required.

Plain text stays UTF-8, preserving an existing BOM and line ending style. CSV/TSV stays a delimited text file. Inline tables do not calculate spreadsheet formulas. Office formats use external editors, preserving their original file format when importing an edited version. See [the visual workspace guide](visual-workspace.md) for limits and behavior.

## Updating the included browser components

Maintainers use `tools/file-ui/package.json` and its lockfile. Run `npm ci --ignore-scripts`, then `npm run build` in that directory. Review upstream changes and licenses, regenerate the vendor files/manifest, and exercise the affected editor. Node/npm and `node_modules` are not needed by users and `node_modules` is excluded from distributions. The shipped assets load locally, only when a file needs them; no CDN or network account is required.

To customize the experience, reuse the document API and its expected revision token. Keep source file permissions, selected workspace/business checks, and copy/version semantics in the shared backend. Replace a browser widget independently when there is a useful reason; avoid creating a separate save implementation.
