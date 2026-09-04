---
id: core.knowledge.refresh-human-layer
type: workflow
owner_system: core
reads:
- Business
- Brand
- ProductService
- Offer
- AudienceSegment
- Market
- Objective
- Observation
- Insight
- Opportunity
- Initiative
- WorkRequest
- AttentionItem
- Experiment
- OutcomeEvaluation
- Learning
- SourceRecord
- SourceProfile
writes: []
---
# Refresh Human Knowledge Layer

## Purpose
Generate an easy-to-browse Markdown view of canonical AURA state—including durable tracked subjects/sources—without creating a second source of truth.

## Business Outcome
Let founders, operators, and teams understand current organizational context, priorities, experiments, Learning, evidence, and monitoring intent through ordinary files that work in Obsidian or any Markdown tool.

## Run When
Run after meaningful canonical state changes, when a human wants an updated knowledge view, during onboarding to a shared workspace, or before reviewing AURA knowledge outside an agent interface.

## Process
1. [DETERMINISTIC] Resolve the active workspace/business; stop if the human knowledge layer is disabled.
2. [DETERMINISTIC] Read canonical objects from `instances/<business-id>/` and preserve IDs/source refs in generated output.
3. [DETERMINISTIC] Regenerate only `knowledge/<business-id>/_generated/`; never overwrite `knowledge/<business-id>/notes/` or treat human notes as canonical state.
4. [AI] When a richer narrative view is requested, summarize only what current canonical objects support and keep uncertainty/status/maturity visible.
5. [DETERMINISTIC] Run `scripts/generate_knowledge_layer.py <business-id>`. When SourceProfiles exist, `Tracked-Subjects.md` groups them by subject and shows source/surface, questions/signals, cadence, notification intent and next useful check. It explicitly does not infer external scheduler state.
6. [HYBRID] Humans may browse/edit notes using any Markdown tool. Incorporate note content into canonical state only through an evidence/context process with provenance.
7. [AI] In ordinary completion messages, point the user to the human concept first; raw object paths are secondary operator/debugging detail.
8. [DETERMINISTIC] Re-running the generator must be safe/idempotent for generated pages and must leave human-authored notes unchanged.

## Verification
- Canonical JSON remains authoritative.
- Generated Markdown is marked `aura_generated: true` and `canonical: false`.
- Human notes are physically separated from generated views.
- Source refs remain traceable to canonical AURA state.
- Related SourceProfiles are presented as one understandable subject dossier.
- Monitoring views describe organizational intent without claiming runtime scheduling.
- No editor-specific format is required.

## Completion Criteria
The current human knowledge view is refreshed, traceable, safe to regenerate, and useful with ordinary Markdown tools while canonical AURA state remains unchanged.
