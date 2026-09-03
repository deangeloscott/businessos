---
id: content.rendering.package-asset
type: workflow
owner_system: content-synthesis
reads:
- Asset
- WorkRequest
writes:
- Asset
context:
- Brand
---
# Render & Package Content Asset

## Purpose
Turn ready source content/design instructions into the final deliverable formats required by the target medium or destination while leaving rendering machinery to the active host.

## Business Outcome
Produce usable final media that preserves the intended message, quality, accessibility, and destination requirements without making AURA a rendering runtime or fallback system.

## Run When
Use when renderable source components exist and the task calls for final media files or destination-ready variants.

## Process
1. [HYBRID] Resolve the exact source Asset/version plus the destination requirements that materially affect the output: dimensions, aspect ratio, duration, file type, codec/compression, safe areas, captions, accessibility, metadata, and size constraints.
2. [INTEGRATION] Use the active harness's best available rendering/export method to create the required variants. If the host cannot produce the requested medium, preserve the highest-fidelity useful source package and explain the concrete missing execution capability or genuine handoff need; do not manufacture an AURA render packet or fallback lifecycle.
3. [DETERMINISTIC] Check mechanically observable output properties such as file existence, dimensions/duration, encoding, naming/version, and required metadata where applicable.
4. [HYBRID] Inspect the actual rendered output visually or audibly for clipping, legibility, timing, sync, missing fonts/media, artifacts, content drift, and other medium-specific quality failures. Do not substitute metadata or sidecars for inspection of the real artifact.
5. [HYBRID] Confirm applicable accessibility requirements such as captions, transcript, alt text, contrast, or readable text at the level the medium requires.
6. [HYBRID] Preserve the useful final Asset versions and their source/version lineage. Persist a VerificationRecord only when independent durable verification will materially help future truth, troubleshooting, handoff, or auditability; routine successful rendering does not require a receipt object.

## Verification
- The final artifact itself is inspected at the level needed for the medium, not merely inferred from source files or metadata.
- Mechanical checks remain mechanical; substantive visual, audio, editorial, and claim quality are judged from the actual output.
- AURA preserves useful organizational artifacts and evidence without owning the renderer or inventing fallback execution machinery.

## Completion Criteria
- The requested final deliverable exists at useful quality in the required format, or the specific real host limitation preventing that result is explicit and the best reusable source state has been preserved.
