# Troubleshooting

1. Run `python scripts/generate_registry.py`.
2. Run `python scripts/validate_workspace.py` for contract/schema/capability problems.
3. Run `python tests/run_all.py` for lifecycle, ownership, routing, context, scenario, and isolation failures.
4. For a task routing issue, run `python scripts/route_task.py "<task>" --top 10` and inspect the selected semantic owner/contract.
5. For context bloat, run `python scripts/context_plan.py <business> <contract-id>` and inspect files/object resolution.
6. For object errors, run `python scripts/validate_object.py <SchemaTitle> <file>` and `validate_references.py`.
7. For missing tools, compile capabilities for the environment and confirm the contract fallback/manual action.
8. Never fix a failure by copying canonical state into another system or bypassing evidence/authorization.
