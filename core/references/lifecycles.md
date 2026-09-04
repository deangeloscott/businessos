# Canonical Semantic States

Canonical AURA objects are durable organizational meanings, **not required execution state machines**.

A status or maturity value describes what an object currently means. It does not require the object to traverse every listed value, create downstream objects, trigger work, or follow one universal lifecycle. The capable model/user decides semantic transitions from context and evidence; deterministic AURA validates only the declared state and structural integrity.

## Insight
Possible status values: `candidate`, `supported`, `active`, `stale`, `superseded`, `contradicted`, `archived`.

These describe the current standing of an Insight. They are not a mandatory promotion sequence.

## Opportunity
An Opportunity is something potentially valuable the organization may choose to pursue.

Possible status values: `candidate`, `investigating`, `qualified`, `prioritized`, `blocked`, `rejected`, `superseded`, `reopened`, `closed`.

`qualified` and `prioritized` Opportunities preserve a structural `reasoning_basis`. Actual commitment is separate meaning: use a `DecisionRecord` when the decision matters for future context and an `Initiative` when committed work needs durable coordination. Execution and outcome evaluation are not later Opportunity stages.

## ChangeEvent
Possible status values: `applied`, `partial`, `failed`, `rolled_back`, `unknown`.

A ChangeEvent records a change that actually occurred or was attempted. It is not a `planned → applying → verifying` execution pipeline. Planning belongs in the relevant decision/work context; verification may be preserved separately when useful.

## Learning
Maturity values: `hypothesis`, `experimental`, `emerging`, `validated`, `standard`.

Status values: `active`, `contradicted`, `deprecated`, `superseded`.

Maturity expresses how established/useful the Learning currently is; status expresses whether it remains usable. Neither list is a mandatory promotion ladder.

## AttentionItem
Possible status values: `open`, `acknowledged`, `resolved`, `archived`.

Attention is organizational memory, not a task or permission gate. A resolved condition may genuinely recur and be reopened. Moving resolved Attention to history requires an explicit retention decision; elapsed time does not decide usefulness.

## PlatformChange
Possible status values: `current`, `superseded`, `archived`.

A materially changed platform state may supersede the previous current state. Authoritative evidence that merely re-verifies the same semantic state updates its verification history rather than manufacturing another version. Moving superseded state to history is explicit, not age-driven.

## General rule
Do not add lifecycle stages because they make software feel orderly. Add or preserve a state only when it represents a distinct fact the organization benefits from remembering.
