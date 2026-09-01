---
id: content.production.article
type: playbook
owner_system: content-synthesis
artifact_role: customer_facing_production_root
reads:
- WorkRequest
- Opportunity
- Insight
- SourceRecord
- Asset
- ProofRecord
writes:
- Asset
- Observation
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - creative.image.generate
  - creative.image.edit
  - creative.audio.generate
  - creative.video.generate
  - creative.animation.generate
  - video.render
  - presentation.render
  - document.render
context:
- AudienceSegment
- Brand
subcontracts:
  required:
  - content.intake.content-brief
  - content.strategy.core-message
  - content.strategy.narrative-structure
  - content.strategy.evidence-proof-plan
  - content.production.outline
  - content.qa.pre-publish
---
# Article Production

## Purpose
Produce a useful, evidence-backed article with appropriate depth, structure, and reader progression.

## Business Outcome
Create or improve article production so the source idea is communicated effectively for the intended audience, objective, platform, and consumption context.

## Run When
Run when an Opportunity or WorkRequest requires article production and existing Assets do not already satisfy the communication need.

## Process
1. [AI] Define reader task, promised outcome, scope, required evidence, and what should be excluded.
2. [AI] Build an information architecture that answers the reader in logical order rather than padding to a target length.
3. [HYBRID] Gather/resolve source evidence and original examples/data/expert input required by the brief.
4. [AI] Draft for clarity, specificity, natural language, and evidence-linked claims; distinguish fact from interpretation.
5. [AI] Add examples, visuals/tables/checklists only where they improve comprehension.
6. [HYBRID] Apply Brand voice and audience terminology without forcing brand phrases that reduce clarity.
7. [HYBRID] Fact-check claims, test internal consistency, remove unsupported filler/repetition, and satisfy upstream SEO/Marketing requirements where delegated.
8. [DETERMINISTIC] Produce versioned Asset metadata and route to editorial/brand/fact QA.

## Completion Evidence
When this production work is executed in a Run, execute and record every required subcontract. Customer-facing article Assets must use the claim-manifest flow in `core/policies/context-provenance-and-claims.md`; `content.qa.pre-publish` must leave a JSON pass record and the Run must be completed with `scripts/complete_run.py` before reporting the workflow complete.
