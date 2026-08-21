---
id: content.production.infographic
type: playbook
version: 1.2.0
owner_system: content-synthesis
risk: low
autonomy_ceiling: 4
reads:
- Insight
- ProofRecord
- Asset
- WorkRequest
- PlatformProfile
writes:
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.image.generate
  - creative.image.edit
  - document.render
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
Run when a Content Opportunity or WorkRequest calls for an infographic or when visual structure communicates the idea materially better than prose alone.

## Process
1. [AI] Identify the single communication job, audience knowledge level, evidence/proof that must remain exact, and what the viewer should understand after scanning.
2. [AI] Choose the appropriate visual logic: process, comparison, timeline, hierarchy, anatomy, before/after, data story, checklist, map, or other structure.
3. [DETERMINISTIC] Verify numbers, labels, claims, source/proof permissions, and required citation/attribution before visual compression.
4. [AI] Build the information hierarchy with a concise title, visual path, grouped sections, explanatory labels, and only the detail needed to support comprehension.
5. [INTEGRATION] Generate/edit/render the visual components using available capabilities or prepare a production-ready Manual Action Package.
6. [HYBRID] QA legibility, factual fidelity, brand fit, accessibility/contrast/text size, and whether the visual can be understood without hidden explanatory context.
7. [DETERMINISTIC] Save the final Asset and lineage to the originating Insight/ProofRecord/WorkRequest.
