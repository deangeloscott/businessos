# BusinessOS Playbook Evolution & Innovation Exchange

BusinessOS can turn strong business Learning into durable local operating improvements without editing the canonical BusinessOS base, and users can optionally package/share those improvements with others.

## Local evolution

1. Promote evidence-backed Learning through `core.learning.promote-learning`.
2. Use `core.learning.playbook-evolution` to create a bounded proposal.
3. Persist it with:
   `python scripts/persist_playbook_evolution.py <business-id> --proposal-file runtime/<proposal>.json`
4. After explicit user approval, adopt a business-scoped extension/local playbook:
   `python scripts/adopt_process_extension.py <business-id> <proposal-id> --approve`
5. Resolve with:
   `python scripts/resolve_effective_contract.py <business-id> <contract-id> --show`

Canonical contracts remain unchanged. Effective behavior is base contract plus active compatible ProcessExtensions.

## Sharing controls

Configure prompting/defaults:
`python scripts/configure_innovation_sharing.py <business-id> --prompt-mode ask_when_noteworthy --detail workflow_only --identity anonymous`

This configuration never grants permission to disclose data.

Detail levels:
- `workflow_only`
- `anonymized_evidence`
- `full_case_study`

Identity levels:
- `anonymous`
- `pseudonymous`
- `named`

These choices are independent.

## Prepare and export

Prepare a local draft:
`python scripts/prepare_innovation_package.py <business-id> <process-extension-id> --detail workflow_only --identity anonymous`

The draft is not approved for sharing.

After the user explicitly approves:
`python scripts/export_innovation_package.py runtime/...draft.json --output runtime/innovation-package.zip --approve`

This creates a portable file only; BusinessOS does not upload it automatically.

## Import and evaluate

Validate:
`python scripts/validate_innovation_package.py innovation-package.zip --require-export-approval`

Import:
`python scripts/import_innovation_package.py <business-id> innovation-package.zip`

Browse the local feed:
`python scripts/list_innovation_exchange.py <business-id> --compatible-only`

Imported packages become external/community evidence candidates, not trusted best practices. They flow through Ecosystem Intelligence triangulation.

After the business tests an innovation and has a canonical OutcomeEvaluation:
`python scripts/record_innovation_outcome.py <business-id> <exchange-entry-id> --outcome supported --evidence-ref eval_...`

Community reports and active-business outcomes remain separate so virality cannot masquerade as replication.

## No central dependency

InnovationPackage JSON/ZIP files can be exchanged manually. A future hosted registry/API may improve discovery, but a local BusinessOS copy remains complete without it.

## Publish or browse a decentralized feed

A curator/community can place approved packages in a folder/repository and generate an index:

`python scripts/build_innovation_exchange_index.py <package-directory> --exchange-id community-name`

Users can browse a downloaded index without importing anything:

`python scripts/browse_innovation_exchange_index.py innovation-index.json --query "landing page"`

A configured `exchange_sources` list may point the active business/harness at approved index locations. Retrieving a remote index/package is still a host capability; import and adoption remain explicit local actions.
