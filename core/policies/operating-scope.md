# BusinessOS Operating-Scope & System-Integrity Policy

BusinessOS should keep the user-facing experience simple: users describe what they want in ordinary language. The agent infers the task scope internally.

## Default scope
For normal business work, the BusinessOS product itself is **protected infrastructure**. Operate through the installed contracts, deterministic helpers, active business instance, runtime state, and designated artifact/output locations.

Normal business-operation work may write to:
- `instances/<active-business-id>/...` when the selected contract/policy authorizes that business state or artifact;
- `runtime/runs/<active-business-id>/...` for bounded working/recovery state;
- other explicitly designated business-output locations named by an installed contract or directly requested by the user.

Normal business-operation work must **not** create, edit, patch, replace, or delete BusinessOS product files such as:
- `scripts/`
- `core/`
- `systems/`
- `tests/`
- `generated/`
- root operating contracts/policies/manifests
- schemas, registries, packaging, or release metadata

This protection is about task scope, not technical impossibility. When the user's request explicitly concerns developing, repairing, configuring, customizing, testing, or upgrading BusinessOS itself, product-file changes may be appropriate under the ordinary change/verification process.

## Supported-path integrity
1. A failed deterministic helper is not permission to bypass it. Correct ordinary invocation mistakes using `--help`, documented examples, or the helper's error guidance.
2. During normal business work, do not replace a failed helper with a custom script, hand-author canonical objects to imitate its output, or stamp self-created state as trusted/explicit-user truth.
3. If the documented supported path genuinely cannot complete the requested operation, preserve state and report the BusinessOS blocker simply. Do not redesign the operating system inside the business task.
4. Schema-valid is not the same as trusted business truth. Canonical objects claiming explicit-user authority must satisfy provenance/grounding validation.

## User experience
Do not expose technical "modes" to ordinary users. Infer whether the request is business operation or BusinessOS development from the request itself. Do not ask nontechnical users to approve architecture changes merely because the agent made a routine CLI mistake.
