---
id: core.intelligence.innovation-exchange
type: workflow
owner_system: core
reads:
- ProcessExtension
- Learning
- SourceRecord
- OutcomeEvaluation
writes:
- SourceRecord
- Learning
---
# AURA Innovation Exchange

## Purpose
Prepare, import, discover, and evaluate portable AURA process improvements without making a hosted exchange, telemetry, prompting subsystem, or automatic sharing part of AURA's required runtime or canonical organization model.

## Business Outcome
Let users learn from useful AURA innovations created elsewhere while retaining local ownership, privacy, portability, and evidence standards.

## Run When
Use when a user wants to share a local improvement, import a contributed `InnovationPackage`, browse locally available contributions, or evaluate a community-developed workflow.

## Process
1. [DETERMINISTIC] Resolve `instances/<business-id>/config/innovation-sharing.json` when present only for contribution defaults and optional discovery sources. It does not decide when sharing work should occur and never grants standing disclosure authorization.
2. [HYBRID] When preparing a contribution, keep detail level (`workflow_only`, `anonymized_evidence`, `full_case_study`) separate from identity (`anonymous`, `pseudonymous`, `named`).
3. [DETERMINISTIC] Build a bounded local draft with `scripts/prepare_innovation_package.py`; never copy canonical organization state wholesale.
4. [HUMAN] Export/share only through `scripts/export_innovation_package.py ... --approve` or an equivalent explicit current-task user instruction. No background upload or automatic submission is allowed.
5. [DETERMINISTIC] Validate imported JSON/ZIP packages with `scripts/validate_innovation_package.py`, then use `scripts/import_innovation_package.py`. Import may maintain local package/index/exchange support files and creates a canonical `SourceRecord` pointing to the exact stored contribution evidence. It does not manufacture an `Insight`, `Learning`, confidence score, or adoption decision.
6. [AI] Interpret the contribution with the organization's other evidence. Judge reported outcomes, provenance, novelty, contradictions, freshness, and applicability; popularity or repetition does not prove effectiveness. Draw on evidence-triangulation or community-evidence-review operating knowledge when those methods materially improve the decision; neither is a mandatory stage.
7. [DETERMINISTIC] Use `scripts/build_innovation_exchange_index.py` to create a folder/repository discovery manifest and `scripts/browse_innovation_exchange_index.py` to search an available index before importing. Use `scripts/list_innovation_exchange.py` for locally imported support data when useful. Retrieving remote material remains a host capability.
8. [HYBRID] When the active organization tests an imported innovation, preserve the real `OutcomeEvaluation` and record its association with the imported support state through `scripts/record_innovation_outcome.py`. The helper records evidence mechanics only; the model/user decides what the result means.
9. [AI] If the accumulated evidence supports a durable organizational conclusion, preserve an `Insight` or `Learning` through normal AURA memory. If a reusable process improvement is warranted, `core.learning.workflow-evolution` may be useful operating knowledge. The model/user decides whether to use it; do not invent an automatic promotion pipeline.

## Verification
- No external submission occurred without an explicit current-task user instruction.
- Workflow detail and identity choices remain independent.
- Known secret/credential fields are rejected from packages.
- Named/anonymous identity metadata truthfully reflects what the package contains.
- Imported reported evidence is not counted as independent local corroboration.
- Import does not manufacture semantic conclusions or confidence scores.
- Exchange/index/cache records remain support/interface data rather than canonical organizational truth.
- The exchange can be unused or disconnected without breaking AURA.

## Completion Criteria
- Sharing/import/discovery evidence is inspectable and portable; canonical organizational meaning is created only when the evidence actually warrants it; and any adopted process remains optional organization-owned operating knowledge.
