# Content QA Defaults

QA is an inspection-and-correction process over a real target, not a pass label.

## Shared execution model

1. Resolve the exact pre-existing target Asset and version. A QA record or Asset created merely to describe the QA cannot be its own target.
2. Determine which checks apply to that medium, destination, audience, claims, and risk. Record an explicit reason for every material check marked not applicable.
3. Inspect the target and its relevant source/proof/Brand/platform context. Use deterministic tools for exact checks and AI/human judgment for semantic checks; record the method actually used.
4. Record criterion-level evidence and findings, including locations/components inspected, expected versus observed behavior, severity, and confidence where judgment is involved.
5. Correct issues within authority or identify the exact proposed correction. Preserve before/after or corrected-version evidence when a change is made.
6. Recheck affected criteria after correction. Record remaining limitations and blockers; do not convert unknown or untested conditions into passes.
7. Set overall status from the check results. `pass` requires all material applicable checks to pass on the named version and an empty blocker list. A failure or material unresolved condition blocks downstream publication.

## Portable QA record

Save a Run-local JSON record containing:

- `contract_id`, `status`, `tested_asset`, and `tested_version`;
- `checks_performed`, with a specific criterion, method, outcome, concrete finding/evidence, issue severity, correction, and recheck result as applicable;
- `issues_found`, `corrections_made`, `limitations`, and `blockers` (empty arrays are explicit when none remain);
- references to inspected evidence and any corrected Asset/version.

Generic labels such as `compliance_validation` or `quality_assurance`, boilerplate claims that all standards passed, and checks aimed at the QA record itself are not completion evidence. Absence of detected issues is valid only when the applicable inspection and evidence are recorded.
