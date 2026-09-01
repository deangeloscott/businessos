# Customer Intervention Defaults

- Establish the relevant baseline transition, time-to-value, outcome, or other journey evidence before intervention when doing so can materially improve the decision; do not manufacture measurement ceremony when it cannot.
- State the causal mechanism: what friction is being changed, why that should alter progression/value, and what evidence would show whether the mechanism worked.
- Define customer/business guardrails and recovery/rollback considerations proportionate to the consequence and reversibility of the real change.
- If the intervention requires persuasion, communication, customer research, product, sales, technical, legal, finance, or other expertise, the active model may use the relevant operating knowledge and host capabilities directly. Create a `WorkRequest` only when a real durable handoff across people/models/sessions/teams must survive the current interaction; never use it as AURA domain-to-domain RPC.
- `ChangeEvent`, `Experiment`, `MetricObservation`, `OutcomeEvaluation`, and other durable objects are created only when those meanings actually occur and future work benefits from remembering them. They are not mandatory lifecycle outputs of an intervention playbook.
- The user request and real external-system permissions/constraints govern execution. AURA does not add a generic authorization, approval, or autonomy layer.
