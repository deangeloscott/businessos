---
id: content.production.infographic
type: workflow
owner_system: content-synthesis
artifact_role: customer_facing_production_root
reads:
- Insight
- ProofRecord
- Asset
- WorkRequest
- PlatformProfile
writes:
- Asset
context:
- AudienceSegment
- Brand
---
# Infographic Production

## Purpose
Turn evidence or a structured idea into a clear visual explanation whose information hierarchy works even when the viewer only scans it.

## Business Outcome
Make complex evidence, processes, comparisons, or results easier to understand and share without sacrificing accuracy for visual simplicity.

## Run When
Use when an infographic is the useful communication output and existing Assets do not already satisfy the need. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Identify the single communication job, audience knowledge level, evidence/proof that must remain exact, and what the viewer should understand after scanning.
2. [AI] Choose the appropriate visual logic: process, comparison, timeline, hierarchy, anatomy, before/after, data story, checklist, map, or other structure.
3. [DETERMINISTIC] Verify numbers, labels, claims, source/proof permissions, and required citation/attribution before visual compression.
4. [AI] Build the information hierarchy with a concise title, visual path, grouped sections, explanatory labels, and only the detail needed to support comprehension.
5. [INTEGRATION] Generate, edit, assemble, or render the visual using the capabilities actually available to the active model/harness. If the requested medium cannot be rendered here, preserve a production-ready design/source specification only when that remains useful and state clearly that the final visual was not produced; do not invent an internal manual-action workflow.
6. [HYBRID] Inspect the actual final visual when one exists for legibility, factual fidelity, brand fit, accessibility/contrast/text size, crop/safe areas, and whether the visual can be understood without hidden explanatory context.
7. [HYBRID] Preserve the useful versioned Asset and evidence/source lineage. Use pre-publish QA operating knowledge directly when the destination or artifact warrants an additional integrated review; a Run or contract-completion ledger is not required.
