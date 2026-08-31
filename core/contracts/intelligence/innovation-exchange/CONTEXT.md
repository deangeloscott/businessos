---
id: core.intelligence.innovation-exchange
type: playbook
version: 1.1.0
owner_system: core
reads:
- ProcessExtension
- Learning
- Insight
- SourceRecord
writes:
- SourceRecord
- Insight
capabilities:
  required:
  - none
  optional:
  - research.web.read
  - document.read
subcontracts:
  required:
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: core.intelligence.community-evidence-review
    when: imported/community evidence is decision-relevant
  - id: core.learning.playbook-evolution
    when: community evidence supports a reusable process improvement
---
# AURA Innovation Exchange

## Purpose
Prepare, import, discover, and evaluate portable AURA process improvements without making a hosted exchange, telemetry, or automatic sharing part of the required runtime or canonical organization model.

## Business Outcome
Let users learn from useful AURA innovations created elsewhere while retaining local ownership, privacy, portability, and evidence standards.

## Run When
Run when a user wants to share a local improvement, import a contributed InnovationPackage, browse locally available contributions, or evaluate a community-developed workflow.

## Process
1. [DETERMINISTIC] Resolve `instances/<business-id>/config/innovation-sharing.json` when present. Treat it as prompting/default configuration only, never standing disclosure authorization.
2. [HYBRID] When preparing a contribution, keep detail level (`workflow_only`, `anonymized_evidence`, `full_case_study`) separate from identity (`anonymous`, `pseudonymous`, `named`).
3. [DETERMINISTIC] Build a draft with `scripts/prepare_innovation_package.py`; never copy canonical business state wholesale.
4. [HUMAN] Export/share only through `scripts/export_innovation_package.py ... --approve` or an equivalent explicit current-task instruction. No background upload or automatic submission is allowed.
5. [DETERMINISTIC] Validate imported JSON/ZIP packages with `scripts/validate_innovation_package.py`, then use `scripts/import_innovation_package.py`. Import tooling may maintain local package/index/exchange-entry support files, but canonical organizational meaning from the contribution is persisted as SourceRecord and candidate Insight objects.
6. [AI] Treat the contribution as a discovery signal. Apply Core evidence triangulation to reported outcomes, provenance, novelty, contradictions, freshness, and applicability; popularity does not prove effectiveness.
7. [DETERMINISTIC] Use `scripts/build_innovation_exchange_index.py` to publish an approved folder/repository manifest and `scripts/browse_innovation_exchange_index.py` to search a downloaded index before importing. Use `scripts/list_innovation_exchange.py` for locally imported support data when useful. Any hosted registry/API is only another discovery transport.
8. [HYBRID] When the active business tests an imported innovation, preserve the OutcomeEvaluation and record the local result through `scripts/record_innovation_outcome.py`; route durable findings into canonical Learning when warranted.
9. [HYBRID] Route sufficiently strong accumulated evidence to `core.intelligence.community-evidence-review`; route reusable validated improvements to `core.learning.playbook-evolution`.

## Verification
- No external submission occurred without an explicit current-task instruction.
- Workflow detail and identity choices remain independent.
- Known secret/credential fields are rejected from packages.
- Imported reported evidence is not counted as independent local corroboration.
- Exchange/index/cache records remain support/interface data rather than canonical organizational truth.
- The exchange can be unused/disconnected without breaking AURA.

## Completion Criteria
- Sharing/import/discovery evidence is inspectable and portable, canonical meaning is preserved through normal AURA evidence/Learning objects, and any adopted process remains optional organization-owned operational knowledge.
