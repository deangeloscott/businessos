# Troubleshooting

Use the smallest diagnostic that matches the problem. AURA owns durable organizational memory, reusable operating knowledge, and their integrity; the active model/harness owns semantic judgment and runtime execution.

1. Run `python3 scripts/generate_registry.py` after changing playbooks, schemas, process maps, or other generated-source inputs.
2. Run `python3 scripts/validate_workspace.py` for product-source, contract, schema, reference, or capability-vocabulary integrity problems.
3. Run `python3 tests/run_all.py` for the complete AURA product-integrity regression set.
4. If a useful playbook is hard to discover, run `python3 scripts/find_playbooks.py "<task>" --top 10`. Treat the results as lexical retrieval hints; the model/user still judges applicability.
5. If an explicitly selected playbook loads too much or too little organizational context, run `python3 scripts/context_plan.py <business> <playbook-id>` and inspect the returned files, object refs, and unresolved selectors.
6. If a canonical object fails validation, use `python3 scripts/validate_object.py <SchemaTitle> <file>` and `python3 scripts/validate_references.py <business-id>` as appropriate. Fix the actual truth/reference problem rather than bypassing validation.
7. If a tool, provider, credential, permission, browser, scheduler, or integration is unavailable, diagnose that in the active harness/system that owns it. AURA capability IDs describe method needs; AURA does not inventory or repair the host runtime.
8. If persisted organizational information is wrong or stale, update, retire, or forget the incorrect memory through the supported canonical memory path. Do not preserve obsolete truth merely because another file/test depends on it.
9. Never manufacture a Run, WorkRequest, AttentionItem, approval, scheduler binding, provider binding, or other coordination object merely to make ordinary work appear complete.

When a test fails, ask what real product truth the assertion is protecting. Fix AURA when that truth is genuinely AURA-owned; change or remove the assertion when it only preserves retired architecture.
