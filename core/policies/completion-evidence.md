# Contract-Aware Completion Evidence

AURA distinguishes **work exists** from **the contracted job is complete**.

A Run may be marked complete only when its evidence is appropriate to the root contract and every required subcontract. File existence, a generic template, a self-authored `status: pass`, or a completion statement is not sufficient by itself.

## Rules

1. **The contract defines the job.** Completion evidence must correspond to the actual contract, intended result, and declared writes. Do not substitute an unrelated artifact merely because it is easy to persist.
2. **Use reusable structural evidence profiles, not output-shaped passwords.** `scripts/completion_evidence.py` maps contracts to profiles such as production, QA, detector, publishing, research, measurement, planning, canonical-state, and generic evidence. Deterministic validation should prove truthful artifact/state/evidence shape; it must not turn arbitrary word counts, slide counts, or required phrases into a proxy for business quality.
3. **Structural validation is a minimum, not a quality score.** Passing deterministic completion checks proves only that evidence is of the right structural kind. It does not prove the work is professionally good, competitive, persuasive, correct, or outcome-ready. Contract process, QA, and review still apply.
4. **Production evidence must match the promised medium.** A canonical customer-facing Asset must be bound to the producing Run and its actual root artifact must be supplied. Rendered media must use an appropriate, structurally usable media form rather than relying on a filename extension. Where the contract permits graceful degradation, a truthful production packet/specification may substitute for unavailable rendering. The amount and shape of that fallback should be driven by the requested outcome, audience, and medium—not a universal length/count threshold. A generic outline or description of future work is still not the deliverable.
5. **QA must show real inspection, not merely a verdict.** QA completion requires a matching structured pass record with a specific criterion, actual method, concrete finding/evidence, issue/correction/limitation state, and per-check outcome. Asset QA must name an existing non-self target Asset and its exact version. Text QA should anchor semantic findings to a literal excerpt or concrete target component; automated/scanner claims require saved tool output. Absent features are `not_applicable` with a reason, not fictional passes. `pass` requires no material failed checks or unresolved blockers.
6. **Intelligence must preserve enough analysis to audit material conclusions.** A concise Observation, Insight, or Learning is durable decision state; it is not a substitute for the evidence and reasoning behind it. For material analysis, keep a proportionate Run-local record of the method, inspected item-level evidence with literal support, findings/mechanisms, important limitations, and recommended action. Add scope, comparison/normalization detail, counterexamples, or alternative explanations when they matter to the decision rather than as ceremonial fields.
7. **Research/measurement/planning/state work must leave the declared result.** When a root contract declares canonical writes, completion evidence must include or be bound to at least one declared result type. A note that the workflow ran does not substitute for the state the contract promises.
8. **No-finding is a valid detector outcome when auditable.** A detector need not manufacture an Opportunity or Incident. If no material finding exists, record a structured no-finding result with the checks performed and existing evidence references.
9. **Automation may orchestrate mechanics but may not replace the business work.** Scripts may create Runs, call deterministic helpers, format packets, validate outputs, and move through queues. They may not mass-manufacture generic artifacts, synthetic QA records, fabricated evidence, or qualification paperwork as substitutes for contract-specific reasoning, research, creation, or verification.
10. **Integrated work does not require duplicate paperwork.** Distinct required subcontracts must each be executed and recorded, but one genuine integrated artifact/evidence package may support multiple subcontracts when it actually contains their work. Do not create byte-different copies or artificial files solely to satisfy completion bookkeeping. Independent/qualification review may still reject generic reuse that did not perform the distinct jobs.
11. **Production QA identifies the exact result tested.** A required QA pass for a customer-facing production Run must name the produced canonical Asset and its exact version. A truthful QA record cannot claim that absent components, branches, links, media, or other required behavior were tested successfully.
12. **Failure to satisfy the structural profile keeps the Run incomplete.** Correct the work/evidence or record the appropriate blocker. `complete_run.py` finalizes completion as a local transaction and runs full active-business validation; any remaining schema, reference, provenance, claim, or Run-semantic error restores the prior incomplete state. Do not bypass a deterministic rejection by editing Run manifests or stamping canonical state manually.
13. **Validation rechecks completed Runs.** `validate_run_completion.py` revalidates semantic/structural completion evidence for Run-bound state so direct manifest edits do not become a bypass.

## Graceful degradation

Graceful degradation means preserving the real deliverable at the highest useful fidelity the environment can support. Examples:

- animation: rendered motion, or a complete scene/keyframe/timing/transition specification sized to the requested piece when rendering is unavailable;
- presentation: rendered slides, or a complete slide-by-slide production specification appropriate to the audience, setting, and desired duration;
- short/long video: rendered video, or a complete production packet with visual/audio/scene or beat execution detail appropriate to the requested duration;
- podcast: recorded audio, or a complete recording/edit packet whose script, timing, cues, and packaging are internally consistent.

A generic outline or unrelated Markdown document is not graceful degradation. A fallback also may not claim that media was recorded, mixed, mastered, rendered, or exported when that media does not exist.

Rendered evidence is checked using deterministic container/signature, minimum-size, dimension, frame, or equivalent integrity rules appropriate to the medium. These checks establish that a usable artifact exists; they do not claim that the creative work is professionally excellent.
