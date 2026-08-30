# Content QA Defaults

QA is an inspection-and-correction process over a real target, not a pass label.

## Shared execution model

1. Resolve the exact pre-existing target Asset and version. A QA record or Asset created merely to describe the QA cannot be its own target.
2. Determine which checks apply to that medium, destination, audience, claims, and risk. Record an explicit reason and named `target_component` for every material check marked `not_applicable`; do not pass a check for a feature the target does not contain.
3. Inspect the target and its relevant source/proof/Brand/platform context. Use deterministic tools for exact checks and AI/human judgment for semantic checks; record the method actually used.
4. Record criterion-level evidence and findings in the most faithful compact form. For text targets, anchor semantic findings with a literal `target_excerpt` when a local passage is the evidence, or name a concrete `target_component` when the check concerns structure/whole-asset behavior. For non-text media, identify the concrete component or saved inspection evidence. Claims of automated measurement/scanning require the saved tool output; do not describe an exact tool result that was not produced.
5. Correct issues within authority or identify the exact proposed correction. Preserve before/after or corrected-version evidence when a change is made.
6. Recheck affected criteria after correction. Record remaining limitations and blockers; do not convert unknown or untested conditions into passes.
7. Set overall status from the check results. `pass` requires all material applicable checks to pass on the named version and an empty artifact/QA blocker list. A failure or material unresolved artifact condition blocks downstream publication. Business-fact, authorization, capability, deployment, and measurement state belongs in the separate Asset production-readiness assessment; those gaps may block launch without falsifying a legitimate draft-level QA pass.
8. Create an `ActionPacket` only when a real issue has a concrete proposed action, resolvable target/evidence references, owner or routing destination, and acceptance/recheck condition. An empty ceremonial action is not a QA result.

## Portable QA record

Save a Run-local JSON record containing:

- `contract_id`, `status`, `tested_asset`, and `tested_version`;
- `checks_performed`, with a specific criterion, method, outcome, concrete finding/evidence, and a literal `target_excerpt` or concrete `target_component` as appropriate; include issue severity, correction, and recheck result when they matter;
- `issues_found`, `corrections_made`, `limitations`, and `blockers` (empty arrays are explicit when none remain);
- references to inspected evidence, saved tool output for claimed automated checks, and any corrected Asset/version.

Generic labels such as `compliance_validation` or `quality_assurance`, boilerplate claims that all standards passed, and checks aimed at the QA record itself are not completion evidence. Absence of detected issues is valid only when the applicable inspection and evidence are recorded.
