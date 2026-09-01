# AURA Process Evolution & Innovation Exchange

AURA can preserve strong organization-specific operating improvements without editing canonical AURA product source. Users may also explicitly package/share those improvements with others. Both capabilities are optional.

## Local process evolution

Reusable Learning is ordinary organization-owned memory. Create or update it when the active model/user judges that the evidence supports a durable reusable conclusion; there is no separate Learning-promotion stage.

When that Learning would materially improve a repeatable method:
1. Use `core.learning.playbook-evolution` to decide whether the Learning itself is sufficient, an existing playbook should gain an organization-local extension, a new local playbook is useful, or a canonical AURA product revision is worth proposing.
2. Persist a bounded proposal with:
   `python3 scripts/persist_playbook_evolution.py <business-id> --proposal-file <proposal.json>`
3. If the organization intentionally chooses a business-scoped proposal, adopt it with:
   `python3 scripts/adopt_process_extension.py <business-id> <proposal-id>`
4. Resolve organization-local operating knowledge with:
   `python3 scripts/resolve_effective_contract.py <business-id> <playbook-id> --show`

A `ProcessExtension` is reusable organization-owned operating knowledge, not execution authority. The active model/user may use, adapt, combine, or ignore it when another method is better.

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

## Import and evaluate

Validate a received package:

`python3 scripts/validate_innovation_package.py <innovation-package.zip> --require-export-approval`

Import it for one organization:

`python3 scripts/import_innovation_package.py <business-id> <innovation-package.zip>`

Import preserves the exact contribution as organization-local support data and creates a canonical `SourceRecord` pointing to that evidence. It does **not** manufacture an `Insight`, `Learning`, confidence score, recommendation, or adoption decision.

Browse locally imported support data:

`python3 scripts/list_innovation_exchange.py <business-id> --compatible-only`

If the active organization tests an imported method and has a real `OutcomeEvaluation`, associate that evidence mechanically:

`python3 scripts/record_innovation_outcome.py <business-id> <exchange-entry-id> --outcome supported --evidence-ref eval_...`

The model/user decides what imported and local evidence means. Reported community outcomes and active-organization outcomes remain separate so popularity or repeated contribution cannot masquerade as independent replication.

## Decentralized discovery

Approved packages can be exchanged through ordinary files, repositories, email/file transfer, or an optional future registry/API. A central service is never required.

A curator/community can generate a portable discovery index from a directory of approved packages:

`python3 scripts/build_innovation_exchange_index.py <package-directory> --exchange-id community-name`

Browse an available index without importing anything:

`python3 scripts/browse_innovation_exchange_index.py <innovation-index.json> --query "landing page"`

A configured `exchange_sources` list may help the active model/harness discover indexes. Retrieving remote material remains a host capability; import, interpretation, testing, adoption, and sharing remain explicit local work.
