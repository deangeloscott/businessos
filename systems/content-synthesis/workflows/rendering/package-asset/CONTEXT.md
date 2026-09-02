---
id: content.rendering.package-asset
type: workflow
owner_system: content-synthesis
reads:
- Asset
- WorkRequest
writes:
- Asset
- VerificationRecord
context:
- Brand
---
# Render & Package Content Asset

## Purpose
Turn approved source content/design instructions into the final deliverable formats required by the target medium/platform.

## Business Outcome
Create or improve render & package content asset so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
After content/creative QA passes and renderable source components exist.

## Process
1. [DETERMINISTIC] Resolve target platform/media specifications: dimensions, aspect ratio, duration, file type, codec/compression, safe areas, captions, accessibility, metadata, and size constraints.
2. [INTEGRATION] Render/export each required variant using the appropriate capability or create a human render packet.
3. [DETERMINISTIC] Validate file existence, dimensions/duration, encoding, naming/version, and required metadata.
4. [HYBRID] Visually/audibly inspect rendered output for clipping, legibility, timing, sync, missing fonts/media, artifacts, and content drift.
5. [HYBRID] Confirm accessibility requirements such as captions/transcript/alt text where applicable.
6. [DETERMINISTIC] Update Asset versions and persist VerificationRecord for packaging quality.
