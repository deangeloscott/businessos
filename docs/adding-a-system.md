# Adding an Operating System

Add a system only when it contributes reusable operating knowledge or durable organization state that is not already represented cleanly elsewhere.

1. Confirm the new domain answers a materially distinct business question and does not duplicate an existing system or Core responsibility.
2. Create `systems/<id>/CONTEXT.md` and `DEFAULTS.md` only when domain-level guidance is genuinely useful. Keep universal behavior in root/Core guidance instead of copying it into every system.
3. Reuse existing canonical objects. Add a domain object/schema only when future organizational work materially benefits from durable state with independent semantics/lifecycle that existing objects cannot represent cleanly.
4. Author the smallest useful playbook set. Each playbook should describe reusable operating knowledge: when it helps, evidence/context it needs, the method, outputs worth preserving, and quality/verification criteria. Do not add wrappers, dispatchers, generic approval/fallback machinery, or lifecycle stages merely for structural symmetry.
5. Keep semantic judgment with the capable model/user and runtime mechanics with the active harness. A system must not create its own provider resolver, tool inventory, scheduler, event bus, retry loop, generic delegation layer, permission framework, or cross-domain relevance router. Cross-domain evidence may be read directly when relevant; durable handoffs use ordinary organization-owned state only when they genuinely need to survive the current session/runtime.
6. Add domain-specific Learning or policy only when the domain has genuinely distinct reusable evidence/quality semantics. Prefer shared Core evidence/truth principles otherwise.
7. Regenerate registries and validate product integrity, canonical references/business isolation, candidate discoverability where relevant, distribution packaging, and realistic work quality. Tests should protect the useful responsibility/invariant rather than freeze prose or obsolete architecture.
8. Change Core only for a genuinely universal organizational-memory or operating-knowledge need, never to make one domain easier to implement.

A good new system should make AURA more useful without making AURA more controlling. If the model/harness can already perform a generic responsibility well, leave that responsibility with the model/harness and give it better organizational context or operating knowledge instead.
