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
Render, inspect, refine, and package creative assets for their intended use, preserving useful editable sources while leaving execution machinery to the active host.

## Business Outcome
Produce usable final media that preserves the intended message, quality, accessibility, and destination requirements without making AURA a rendering runtime or fallback system.

## Run When
Use when renderable source components exist and the task calls for final media, corrections to a rendered asset, or an editable source package for continued work.

## Process
1. [HYBRID] Resolve the intended level of finish, exact source Asset/version, and destination requirements that materially affect the output: dimensions, aspect ratio, duration, file type, codec/compression, safe areas, captions, accessibility, metadata, and size constraints. Judge a rough concept, expressive piece, faithful representation, or finished instructional asset by its actual requested use.
2. [INTEGRATION] Use the active harness's best available rendering/export method to create the required variants. If the host cannot produce the requested medium, preserve the highest-fidelity useful source package and explain the concrete missing execution capability or genuine handoff need; do not manufacture an AURA render packet or fallback lifecycle.
3. [DETERMINISTIC] Check mechanically observable output properties such as file existence, dimensions/duration, encoding, naming/version, and required metadata where applicable.
4. [HYBRID] Inspect the actual rendered output visually or audibly for the intended effect, clipping, legibility, timing, sync, missing fonts/media, artifacts, content drift, and other relevant quality failures. Do not substitute metadata or sidecars for inspection. When a material defect prevents the requested result, locate and diagnose it, use a suitable correction while preserving successful parts, and compare the revision with the best prior result. Recheck affected relationships for new defects. If improvement stalls, change approach or explain the concrete limitation within the user's time/cost constraints; the host owns iteration and execution. State any material inspection coverage limit.
5. [HYBRID] Confirm applicable accessibility requirements such as captions, transcript, alt text, contrast, or readable text at the level the medium requires.
6. [HYBRID] Preserve useful final Asset versions and source/version lineage. When continuation matters, retain editable source and required media/dependencies in a durable location with selected references and material unresolved issues; native project structure can remain native. Use existing Asset references and useful preference/handoff memory rather than retaining every intermediate attempt. Persist a VerificationRecord only when independent durable verification materially helps future work; routine successful rendering does not require a receipt object.

## Verification
- The final artifact itself is inspected at the level needed for the medium, not merely inferred from source files or metadata.
- Mechanical checks remain mechanical; substantive visual, audio, editorial, and claim quality are judged from the actual output.
- AURA preserves useful organizational artifacts and evidence without owning the renderer or inventing fallback execution machinery.

## Completion Criteria
- The requested final deliverable exists at useful quality in the required format, or the specific real host limitation preventing that result is explicit and the best reusable source state has been preserved.
