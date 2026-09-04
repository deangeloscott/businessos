# AURA Workflow Evolution & Innovation Exchange

AURA can preserve strong organization-specific operating improvements without editing canonical AURA product source. Users may also explicitly package/share those improvements with others. Both capabilities are optional.

## Local Workflow evolution

Reusable `Learning` is ordinary organization-owned memory. A `ProcessExtension` is reusable organization-owned operating knowledge that either augments an installed AURA Workflow or defines an organization-local Workflow.

There is no proposal/adoption lifecycle between them.

When reusable procedural knowledge is worth preserving:

1. Decide whether the useful meaning is already captured by Learning, should augment an installed Workflow, or deserves an organization-local Workflow.
2. Prepare a small ProcessExtension specification containing the Workflow relationship, purpose, applicability, instructions, and useful provenance.
3. Persist it directly:

   `python3 scripts/persist_process_extension.py <business-id> --spec-file <process-extension.json>`

4. Resolve the effective organization-specific Workflow knowledge when useful:

   `python3 scripts/resolve_workflow.py <workflow-id> --business-id <business-id> --show`

A `ProcessExtension` is retrieval context, not execution authority. The active model/user may use, adapt, combine, or ignore it when another method is better.

### Organization-authored procedures

An organization-authored procedure does **not** need fabricated Learning, a proposal, an approval record, or a fake source reference first. Persist the useful procedure directly with `scripts/persist_process_extension.py`.

### Learning-derived procedures

When canonical Learning supports a reusable improvement, preserve the relevant Learning references in the ProcessExtension. The Learning remains evidence-backed organizational memory; the ProcessExtension preserves the reusable procedural consequence.

## What should evolve

Do not convert every successful task into a new rule.

Improve reusable Workflow knowledge only when evidence or repeated use shows that a durable change will materially improve future work. Prefer the smallest change that captures the useful lesson.

Workflow evolution should preserve only what future work benefits from:

- where the Learning/evidence came from when provenance exists;
- when the improvement applies and does not apply;
- the few instructions that materially improve repeatability, truth, evidence, or quality;
- optional verification guidance when it is genuinely useful;
- discoverability in natural language.

Do not add provider/tool bindings, capability vocabularies, schedules, permissions, Workflow `reads`/`writes` contracts, product-system ownership, or AURA version compatibility gates. The active model/harness remains free to use better tools, Skills, resources, sequencing, or implementation methods.

## Optional sharing defaults

Configure contribution defaults and optional discovery sources:

`python3 scripts/configure_innovation_sharing.py <business-id> --detail workflow_only --identity anonymous [--enable-discovery] [--source <index-reference>]`

These settings remember formatting/discovery preferences only. They do not decide when AURA should interrupt the user, prepare a contribution, or disclose anything.

Detail levels:
- `workflow_only`
- `anonymized_evidence`
- `full_case_study`

Identity levels:
- `anonymous`
- `pseudonymous`
- `named`

Detail and identity are independent.

## Prepare and export

For an explicit sharing task, prepare a bounded local draft:

`python3 scripts/prepare_innovation_package.py <business-id> <process-extension-id> --detail workflow_only --identity anonymous`

The draft is not approved for external disclosure.

After the user explicitly authorizes the current export:

`python3 scripts/export_innovation_package.py <draft.json> --output <innovation-package.zip> --approve`

This creates a portable file only. AURA does not upload or publish it automatically.

The package `format_version` describes the portable file format only. It is not an AURA product-version compatibility gate.

## Import and evaluate

Validate a received package:

`python3 scripts/validate_innovation_package.py <innovation-package.zip> --require-export-approval`

Import it for one organization:

`python3 scripts/import_innovation_package.py <business-id> <innovation-package.zip>`

Import preserves the exact contribution as organization-local support data and creates a canonical `SourceRecord` pointing to that evidence. It does **not** manufacture an `Insight`, `Learning`, ProcessExtension, confidence score, recommendation, compatibility judgment, or adoption decision.

Browse locally imported support data:

`python3 scripts/list_innovation_exchange.py <business-id>`

If the active organization tests an imported method and has a real `OutcomeEvaluation`, associate that evidence mechanically:

`python3 scripts/record_innovation_outcome.py <business-id> <exchange-entry-id> --outcome supported --evidence-ref eval_...`

The model/user decides what imported and local evidence means. Reported community outcomes and active-organization outcomes remain separate so popularity or repeated contribution cannot masquerade as independent replication.

## Decentralized discovery

Approved packages can be exchanged through ordinary files, repositories, email/file transfer, or an optional future registry/API. A central service is never required.

A curator/community can generate a portable discovery index from a directory of approved packages:

`python3 scripts/build_innovation_exchange_index.py <package-directory> --exchange-id community-name`

Browse an available index without importing anything:

`python3 scripts/browse_innovation_exchange_index.py <innovation-index.json> --query "landing page"`

A configured `exchange_sources` list may help the active model/harness discover indexes. Retrieving remote material remains a host responsibility; import, interpretation, testing, local persistence, and sharing remain explicit work.
