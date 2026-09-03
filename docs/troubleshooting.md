# Troubleshooting

Use the smallest diagnostic that matches the problem. AURA owns durable organizational memory, reusable operating knowledge, and their integrity; the active model/harness owns semantic judgment and runtime execution.

1. Run `python3 scripts/generate_registry.py` after changing Workflows, schemas, process maps, or other generated-source inputs.
2. Run `python3 scripts/validate_workspace.py` for product-source, Workflow-metadata, schema, reference, navigation, or retired-architecture integrity problems.
3. Run `python3 tests/run_all.py` for the complete AURA product-integrity regression set.
4. If a useful Playbook is hard to discover, run `python3 scripts/find_playbooks.py "<task>" --top 10`. Treat the results as retrieval hints; the model/user still judges applicability.
5. If a useful Workflow is hard to discover, run `python3 scripts/find_workflows.py "<task>" --top 10` and optionally narrow to the relevant operating area.
6. If an explicitly selected Workflow loads too much or too little organizational context, run `python3 scripts/context_plan.py <business-id> <workflow-id>` and inspect the returned files, object refs, and unresolved selectors.
7. If a canonical object fails validation, use `python3 scripts/validate_object.py <SchemaTitle> <file>` and `python3 scripts/validate_references.py <business-id>` as appropriate. Fix the actual truth/reference problem rather than bypassing validation.
8. If a tool, provider, credential, permission, browser, scheduler, or integration is unavailable, diagnose that in the active harness/system that owns it. AURA does not inventory, authorize, or repair the host runtime.
9. If persisted organizational information is wrong or stale, update, retire, supersede, or forget the incorrect memory through the supported canonical memory path. Do not preserve obsolete truth merely because another file/test depends on it.
10. Never manufacture a Run, WorkRequest, AttentionItem, approval, scheduler binding, provider binding, or other coordination object merely to make ordinary work appear complete.

When a test fails, ask what real product truth the assertion is protecting. Fix AURA when that truth is genuinely AURA-owned; change or remove the assertion when it only preserves retired architecture.
