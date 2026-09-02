# Content QA Defaults

QA is an inspection-and-correction process over a real target, not a pass label.

## Shared execution model

1. Resolve the exact pre-existing target Asset and version. A QA record or Asset created merely to describe the QA cannot be its own target.
2. Determine which checks apply to that medium, destination, audience, claims, and consequence. Record an explicit reason and named `target_component` for every material check marked `not_applicable`; do not pass a check for a feature the target does not contain.
3. Inspect the target and its relevant source/proof/Brand/platform context. Use exact tools where they improve exact checks and AI/human judgment where interpretation is required; record the method only when doing so materially improves auditability.
4. Record criterion-level evidence and findings in the most faithful compact form. For text targets, anchor material semantic findings with a literal `target_excerpt` when a local passage is the evidence, or name a concrete `target_component` when the check concerns structure/whole-asset behavior. For non-text media, identify the concrete component or saved inspection evidence. Claims of automated measurement/scanning require the actual saved tool output; do not describe an exact tool result that was not produced.
5. Correct issues that the user actually asked the model/harness to correct and that the host can legitimately change, or identify the exact proposed correction when execution is outside the current request/capability/real constraint. Preserve before/after or corrected-version evidence when it materially helps later verification or continuity.
6. Recheck affected criteria after correction. Record remaining limitations and blockers; do not convert unknown or untested conditions into passes.
7. Set overall status from the check results. `pass` requires all material applicable checks to pass on the named version and an empty artifact/QA blocker list. A failure or material unresolved artifact condition blocks a claim of publication readiness. Business-fact, actual external authorization, capability, deployment, and measurement state remain separate facts; those gaps may block launch without falsifying a legitimate draft-level QA pass.
8. If an unresolved QA issue needs future organizational follow-up, preserve only the smallest durable meaning that helps continuation—for example a real `WorkRequest` handoff or `AttentionItem` when its semantics actually fit. Do not create a generic execution packet, permission object, or coordination record merely because QA found an issue.

## Auditable QA support

Preserve enough QA support to justify material pass/fail claims and reconstruct important corrections when future work needs it. The smallest useful support may live with the Asset/version, saved inspection evidence, or another appropriate durable result; ordinary QA does not require a separate Run-local record.

Where material, preserve:

- the tested Asset/version and overall status;
- checks performed, with specific criterion, method when relevant, outcome, concrete finding/evidence, and a literal `target_excerpt` or concrete `target_component` as appropriate;
- issue severity, correction, and recheck result when they matter;
- remaining issues, limitations, and blockers;
- references to inspected evidence, actual saved tool output for claimed automated checks, and any corrected Asset/version.

Generic labels such as `compliance_validation` or `quality_assurance`, boilerplate claims that all standards passed, and checks aimed at the QA record itself are not evidence. Absence of detected issues is valid only when the applicable inspection was actually performed.

If an optional AURA playbook conformance receipt is being used, its completion profile may additionally require a compact Run-local QA record. That requirement belongs to the chosen conformance receipt, not to QA itself or ordinary organizational memory.
