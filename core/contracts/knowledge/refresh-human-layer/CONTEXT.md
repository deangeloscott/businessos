---
id: core.knowledge.refresh-human-layer
type: playbook
version: 1.0.0
owner_system: core
risk: low
autonomy_ceiling: 4
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
writes: []
capabilities:
  required:
  - none
  optional:
  - none
---
# Refresh Human Knowledge Layer

## Purpose
Generate an easy-to-browse Markdown view of canonical BusinessOS state for humans without creating a second source of truth.

## Business Outcome
Let founders, operators, and teams understand current BusinessOS knowledge, priorities, experiments, and Learning through ordinary files that work in Obsidian or other Markdown tools.

## Run When
Run after meaningful canonical state changes, when a human wants an updated second-brain view, during onboarding to a shared workspace, or before reviewing BusinessOS knowledge outside an agent interface.

## Process
1. [DETERMINISTIC] Resolve the active workspace and business; stop if the configured workspace has the human knowledge layer disabled.
2. [DETERMINISTIC] Read canonical objects from `instances/<business-id>/` and preserve their IDs and workspace-relative source refs in generated output.
3. [DETERMINISTIC] Regenerate only `knowledge/<business-id>/_generated/`; never overwrite `knowledge/<business-id>/notes/` or treat human notes as canonical state.
4. [AI] When a richer narrative view is requested, summarize only what current canonical objects support and keep uncertainty/status/maturity visible; do not fill gaps from generic knowledge.
5. [DETERMINISTIC] Run `scripts/generate_knowledge_layer.py <business-id>` for the standard portable view and verify the Home page plus domain/learning/experiment pages exist.
6. [HYBRID] Humans may browse/edit notes through Obsidian, VS Code, a file browser, or any Markdown editor. Incorporate note content into canonical state only through the appropriate BusinessOS evidence/context process.
7. [DETERMINISTIC] Re-running the generator must be idempotent for generated pages and must leave human-authored notes unchanged.

## Verification
- Canonical JSON remains authoritative.
- Generated Markdown is marked `businessos_generated: true` and `canonical: false`.
- Human notes are physically separated from generated views.
- Source refs remain traceable to canonical BusinessOS state.
- No Obsidian/editor-specific format is required.

## Completion Criteria
- The current human knowledge view is refreshed, traceable, safe to regenerate, and usable with ordinary Markdown tools while canonical BusinessOS state remains unchanged.
