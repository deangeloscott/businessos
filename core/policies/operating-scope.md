# BusinessOS Operating-Scope & System-Integrity Policy

BusinessOS should keep the user-facing experience simple: users describe what they want in ordinary language. The agent infers the task scope internally.

## Default scope
For normal business work, the BusinessOS product itself is **protected infrastructure**. Operate through the installed contracts, deterministic helpers, active business instance, runtime state, and designated artifact/output locations.

Normal business-operation work may write to:
- `instances/<active-business-id>/...` when the selected contract/policy authorizes that business state or artifact;
- `runtime/runs/<active-business-id>/...` for bounded working/recovery state;
- other explicitly designated business-output locations named by an installed contract or directly requested by the user.

**The entire BusinessOS product root is read-only during normal business operation unless the user's request explicitly concerns developing, repairing, configuring, customizing, testing, or upgrading BusinessOS itself.** Do not use the product root as a working directory for business artifacts or tool scratch state. Build output, generated media, temporary files, browser/user-data profiles, renderer caches, package-manager output, helper scripts, logs, previews, exports, and hidden working directories such as `.build/`, `.tmp/`, or `.cache/` belong under the active organization workspace/runtime when they are business state, or in an external temporary location when they are disposable execution scratch.

Normal business-operation work must **not** create, edit, patch, replace, or delete BusinessOS product files such as:
- `scripts/`
- `core/`
- `systems/`
- `tests/`
- `generated/`
- root operating contracts/policies/manifests
- schemas, registries, packaging, or release metadata
- root-level or nested scratch/build/cache/output directories created by business execution or third-party tools

This protection is about task scope, not technical impossibility. When the user's request explicitly concerns developing, repairing, configuring, customizing, testing, or upgrading BusinessOS itself, product-file changes may be appropriate under the ordinary change/verification process.

## Supported-path integrity
1. A failed deterministic helper is not permission to bypass it. Correct ordinary invocation mistakes using `--help`, documented examples, or the helper's error guidance.
2. During normal business work, do not replace a failed helper with a custom script, hand-author canonical objects to imitate its output, or stamp self-created state as trusted/explicit-user truth.
3. If the documented supported path genuinely cannot complete the requested operation, preserve state and report the BusinessOS blocker simply. Do not redesign the operating system inside the business task.
4. Schema-valid is not the same as trusted business truth. Canonical objects claiming explicit-user authority must satisfy provenance/grounding validation.
5. When a renderer, browser, package manager, compiler, or other tool defaults to the current working directory, redirect its output/profile/cache/temp paths into the active workspace/runtime or an external temporary directory before invocation. Tool defaults do not override the product-root boundary.

## User experience
Do not expose technical "modes" to ordinary users. Infer whether the request is business operation or BusinessOS development from the request itself. Do not ask nontechnical users to approve architecture changes merely because the agent made a routine CLI mistake.
