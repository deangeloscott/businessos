# Contract Authoring

Atomic contracts are the independently routable SOP units. Keep the procedure complete, but inherit universal rules instead of repeating them.

## Source of truth
Frontmatter is machine-readable and human-readable metadata. The body contains only the job-specific operating logic. Generated registries are derived; never edit them manually.

## Required frontmatter
`id`, `type`, `version`, `owner_system`, `risk`, `autonomy_ceiling`, `reads`, `writes`, and `capabilities`. Add events, schedule, or explicit references only when needed.

## Required body
- `# Name`
- `## Purpose` — exact job.
- `## Business Outcome` — why this job changes a useful decision or result; avoid generic filler.
- `## Run When` — concrete trigger/condition.
- `## Process` — complete ordered SOP with executor labels.

Use optional sections only when they add job-specific value: `Do Not Run When`, `Decision Rules`, `Verification`, `Failure / Fallback`, `Completion Criteria`, `References`. Universal verification/fallback/completion rules are inherited from Core/System/Family defaults.

## Inputs and outputs
`reads` and `writes` in frontmatter are canonical. Do not duplicate them as body lists unless the body must explain a non-obvious semantic requirement.

## Executor labels
Use `[AI]`, `[DETERMINISTIC]`, `[INTEGRATION]`, `[HUMAN]`, or `[HYBRID]` on meaningful process steps.

## Separate contract vs step
Create a contract when work is independently routable/reusable, has materially different context/capability/risk/output/fallback behavior, or is shared by several parents. Keep small mechanical actions as steps or deterministic utilities.
