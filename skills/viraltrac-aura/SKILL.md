---
name: viraltrac-aura
description: Use ViralTrac AURA for substantive work on behalf of an AURA-managed organization. Retrieve relevant organization-owned memory and operating knowledge before useful work, use the host's normal tools and other Skills freely, and preserve durable organizational meaning afterward when it will materially help future work. Ignore AURA for unrelated work.
---

# ViralTrac AURA

AURA is organization-owned durable memory and reusable business operating knowledge. It is not the model, tool runtime, provider selector, scheduler, permission system, or universal orchestrator.

## Locate and verify AURA

Use the AURA product root supplied by the user or harness. If this Skill is still inside the standard AURA distribution at `skills/viraltrac-aura/`, the product root is two directories above this file. If this Skill was copied elsewhere and the AURA root is not already configured, ask for the AURA folder once rather than scanning the device broadly.

The organization workspace may be inside the AURA product root or configured separately by AURA. Use AURA's helpers to resolve it instead of guessing paths.

When setup/readiness is genuinely unknown, prefer the product-owned entry points instead of manually reconstructing setup:

- `python3 scripts/setup.py ...` — idempotently prepare known workspace/organization state and run the readiness proof.
- `python3 scripts/doctor.py --business-id <id>` — verify resolution, bounded retrieval, canonical write/read/delete, and AURA-owned validation.

Host-native Skill/persistent-instruction attachment remains the host's responsibility. AURA should expose the bundled Skill path, not invent a universal host adapter.

## When to use AURA

Use AURA when the request is substantive work for an organization managed by AURA and existing organizational context or operating knowledge could materially improve the result or continuity.

Do not invoke AURA merely because it exists. Ignore it for unrelated personal/general work.

## Operating pattern

1. **Identify the organization.** Use `python3 scripts/list_businesses.py --json` when needed. If several organizations are plausible and context does not resolve the choice, ask rather than guessing.
2. **Retrieve little.** Use `python3 scripts/enter.py "<complete request>" --business-id <id>` or equivalent direct retrieval. Load only context that can materially improve this job.
3. **Use operating knowledge when helpful.** AURA may surface a high-level Playbook and relevant Workflows. Treat them as reusable expertise, not authority. Use the smallest useful set. Sequence, parallelize, adapt, combine, or skip workflows with model judgment.
4. **Use the host normally.** Use any appropriate tools, connectors, other Skills, subagents, APIs, browsers, renderers, files, or execution methods available in the active harness. AURA does not define an allowlist and does not require specific providers.
5. **Aim at the outcome.** Follow workflow steps that materially improve repeatability, truth, evidence, or quality. Do not micromanage implementation when the capable model can achieve the requirement better another way.
6. **Preserve durable value.** After substantive work, ask: *Would a capable future model working for this organization materially benefit from knowing this after the current session is gone?* If yes, preserve the smallest useful organizational meaning through AURA. `scripts/remember.py` is the generic create/update primitive; use specialized helpers only when their semantics genuinely matter. New objects may use `kind` or `object_type`; updates can infer type from `object_ref`; local `key` is only needed when cross-object `@references` need a caller-chosen alias.
7. **Keep truth current.** Update established current truth when it changes. Remove obsolete fields explicitly when appropriate. Use `scripts/forget.py` when an entire unreferenced object no longer deserves durable memory. Unknown/not-found is not absence.
8. **Preserve useful artifacts.** When a real deliverable will matter later, keep the actual artifact in a durable location and preserve the useful Asset/reference/provenance in AURA rather than saving every temporary file.
9. **Use monitoring correctly.** AURA may remember what should be monitored, why, material signals, cadence intent, and prior findings. The active harness/OS/automation system owns actual wakeups, recurrence, retries, and notification delivery.
10. **Use receipts sparingly.** A Run is an optional bounded work receipt when continuity/provenance materially benefits. Do not create one merely to begin work or to make memory writable. After material persistence, give the user only a compact save receipt from the actual persistence result, for example: `Saved to Oregon Tilth: competitor profiles and research report. Validation passed.` Do not create a receipt object just to report the save.
11. **Validate AURA-owned state after material changes.** Schema validity, references, provenance mechanics, and organization isolation belong to AURA; semantic judgment remains with the model/user.

## ViralTrac when available

ViralTrac is AURA's optional first-party companion for attribution, tracking, measurement, experiments, first-party business evidence, artifacts, and supported growth actions. When it is available and materially useful, discover and use its current interface through the host rather than assuming fixed capabilities; if it exposes MCP/bootstrap/tool-group guidance, let that product-specific metadata guide ViralTrac tool use. AURA Playbooks and Workflows remain business operating expertise, while ViralTrac playbooks are product-specific guidance that may complement them. Keep ViralTrac operational data authoritative there, respect its current execution/permission/receipt boundaries, and preserve back into AURA only the durable organizational meaning that will materially help future work.

## Playbooks, Workflows, and Steps

- **Playbook** — an end-to-end business job such as Competitor Research or Customer Research.
- **Workflow** — a reusable procedure that helps accomplish part of a Playbook or can be useful on its own.
- **Step** — the minimum procedural guidance needed for a Workflow to reliably achieve its intended result.

AURA should give capable intelligence the fewest instructions necessary to repeatedly achieve the desired outcome at the required truth and quality standard. Do not treat an authored step as a reason to ignore a better available method unless the step expresses a real requirement.

## Boundary

Do not modify AURA product source during ordinary organization work simply to solve an execution problem. Organization-specific facts, preferences, Learning, evidence, Assets, and reusable local operating knowledge belong in organization state. Product changes belong to explicit AURA development work.
