# Adding an Operating System

1. Confirm the new domain answers a semantic question not already canonically owned.
2. Create `systems/<id>/CONTEXT.md` and `DEFAULTS.md` defining purpose, scope, and explicit non-scope.
3. Reuse Core objects. Add a domain object/schema only when persistent state cannot be represented cleanly with Core objects.
4. Author atomic contracts with unique namespaced IDs, executor-labeled steps, reads/writes, capabilities, fallback, and completion criteria.
5. Declare events consumed/emitted and cross-system delegation needs.
6. Add domain Learning contract and quality/policy only when domain-specific.
7. Generate registries and add routing/context/ownership/scenario tests.
8. Core changes are allowed only for a genuinely universal concept, not to make the new domain convenient.
