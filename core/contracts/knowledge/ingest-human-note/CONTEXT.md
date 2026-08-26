---
id: core.knowledge.ingest-human-note
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 3
reads:
- SourceRecord
- Observation
- Insight
- Business
- Brand
writes:
- SourceRecord
capabilities:
  required:
  - none
  optional:
  - none
subcontracts:
  conditional:
  - id: core.intelligence.publish-observation
    when: the note contains a directly supported decision-relevant statement worth preserving as an Observation
---
# Ingest Human Knowledge Note

## Purpose
Bring a human-authored Markdown/text note into BusinessOS as provenance-backed source material without assuming the note is verified canonical business truth.

## Business Outcome
Let humans contribute knowledge naturally through an Obsidian/Markdown-style workspace while preserving BusinessOS evidence, truth, and interpretation boundaries.

## Run When
Run when a human asks BusinessOS to use, review, incorporate, or learn from a note stored under `knowledge/<business-id>/notes/`.

## Process
1. [DETERMINISTIC] Confirm the note is inside the active business's `knowledge/<business-id>/notes/` directory and belongs to the active workspace; reject arbitrary path traversal or unsupported file types.
2. [DETERMINISTIC] Run `scripts/register_human_note.py <business-id> <note>` to persist a content-hashed SourceRecord whose source reference is workspace-relative and whose metadata explicitly says the note is noncanonical source material.
3. [AI] Read the note and separate direct statements, opinions, hypotheses, requested decisions, interpretations, and unknowns. Do not convert the entire note into factual Business context merely because a human wrote it.
4. [HYBRID] For directly supported decision-relevant statements that should become reusable evidence, route to `core.intelligence.publish-observation` with the registered SourceRecord. Use the appropriate context/claim workflow when stronger authority is actually established through supported evidence or current explicit user instruction.
5. [AI] Route interpretations/questions to the canonical domain owner for Insight, investigation, or work rather than duplicating domain semantics in Core.
6. [DETERMINISTIC] Keep the original human note unchanged and preserve its SourceRecord/hash even if later canonical objects supersede or contradict its contents.
7. [HYBRID] Refresh the human knowledge layer when canonical state changed; do not rewrite the source note to make it appear that the human originally said something different.

## Verification
- The SourceRecord resolves to the exact note and content hash.
- The note remains under `notes/` and is not overwritten.
- Registration alone creates no Business/Observation/Insight/Learning truth claim.
- Any canonical object derived from the note has normal source/lineage governance.

## Completion Criteria
- The note is traceable as noncanonical source material and any useful statements/interpretations are routed through the correct BusinessOS evidence/context/domain process.
