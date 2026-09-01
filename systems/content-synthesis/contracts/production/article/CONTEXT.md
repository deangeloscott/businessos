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
Use when an article is the useful communication output and existing Assets do not already satisfy the need. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define reader task, promised outcome, scope, required evidence, and what should be excluded.
2. [AI] Build an information architecture that answers the reader in logical order rather than padding to a target length.
3. [HYBRID] Gather/resolve source evidence and original examples/data/expert input required by the brief.
4. [AI] Draft for clarity, specificity, natural language, and evidence-linked claims; distinguish fact from interpretation.
5. [AI] Add examples, visuals/tables/checklists only where they improve comprehension.
6. [HYBRID] Apply Brand voice and audience terminology without forcing brand phrases that reduce clarity.
7. [HYBRID] Fact-check claims, test internal consistency, remove unsupported filler/repetition, and use relevant SEO/Marketing operating knowledge directly when it improves the article.
8. [HYBRID] Preserve the useful versioned Asset and evidence linkage. Use editorial/brand/fact/pre-publish QA methods directly as warranted by the actual artifact and destination; they are operating knowledge, not a required execution ledger.

## Completion Evidence
A high-quality article is complete when the requested artifact exists at useful quality and its material outward claims are evidence-bounded. Customer-facing article Assets use the claim-manifest flow in `core/policies/context-provenance-and-claims.md` when deterministic claim checking is applicable. A Run/work receipt and subcontract-completion ledger are optional and do not determine whether the article itself is valid or complete.
