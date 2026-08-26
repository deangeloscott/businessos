# Contract-Aware Completion Evidence

AURA distinguishes **work exists** from **the contracted job is complete**.

A Run may be marked complete only when its evidence is appropriate to the root contract and every required subcontract. File existence, a generic template, a self-authored `status: pass`, or a completion statement is not sufficient by itself.

## Rules

1. **The contract defines the job.** Completion evidence must correspond to the actual contract, intended result, and declared writes. Do not substitute an unrelated artifact merely because it is easy to persist.
2. **Use reusable evidence profiles, not bespoke loopholes.** `scripts/completion_evidence.py` maps contracts to structural profiles such as production, QA, detector, publishing, research, measurement, planning, canonical-state, and generic evidence. Individual contracts may add explicit `completion_evidence` metadata when the inferred profile is insufficient.
3. **Structural validation is a minimum, not a quality score.** Passing deterministic completion checks proves only that evidence is of the right structural kind. It does not prove the work is professionally good, competitive, persuasive, correct, or outcome-ready. Contract process, QA, and review still apply.
4. **Production evidence must match the promised medium.** A canonical customer-facing Asset must be bound to the producing Run and its actual root artifact must be supplied. Rendered media must use an appropriate media form. Where the contract explicitly permits graceful degradation, a complete production packet/specification may substitute for unavailable rendering; generic prose may not.
5. **QA must show checks, not merely a verdict.** QA completion requires a matching structured pass record with substantive checks. Strict QA profiles such as `content.qa.pre-publish` additionally require the tested Asset/version and blocker state. A bare JSON object whose only meaningful assertion is `status: pass` is not QA evidence.
6. **Research/measurement/planning/state work must leave the declared result.** When a root contract declares canonical writes, completion evidence must include or be bound to at least one declared result type. A note that the workflow ran does not substitute for the state the contract promises.
7. **No-finding is a valid detector outcome when auditable.** A detector need not manufacture an Opportunity or Incident. If no material finding exists, record a structured no-finding result with the checks performed and existing evidence references.
8. **Automation may orchestrate mechanics but may not replace the business work.** Scripts may create Runs, call deterministic helpers, format packets, validate outputs, and move through queues. They may not mass-manufacture generic artifacts, synthetic QA records, fabricated evidence, or qualification paperwork as substitutes for contract-specific reasoning, research, creation, or verification.
9. **Failure to satisfy the profile keeps the Run incomplete.** Correct the work/evidence or record the appropriate blocker. Do not bypass a deterministic rejection by editing Run manifests or stamping canonical state manually.
10. **Validation rechecks completed Runs.** `validate_run_completion.py` revalidates semantic/structural completion evidence for Run-bound state so direct manifest edits do not become a bypass.

## Graceful degradation

Graceful degradation means preserving the real deliverable at the highest useful fidelity the environment can support. Examples:

- animation: rendered motion, or a complete scene/keyframe/timing/transition specification when rendering is unavailable;
- presentation: rendered slides, or a complete slide-by-slide production specification when the contract permits it;
- short/long video: rendered video, or a complete production packet with visual/audio/duration/scene or beat execution detail when the contract permits it;
- podcast: recorded audio, or a complete recording/edit packet when the contract permits it.

A generic outline or unrelated Markdown document is not graceful degradation.
